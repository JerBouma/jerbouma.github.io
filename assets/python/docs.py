"""
This file generates the Finance Toolkit documentation pages by fetching docstrings
from the controller modules on GitHub and converting them to Jekyll Markdown.
"""

import ast
import base64
import os
import re
import sys
import unicodedata

import requests

# ── Compiled regexes (module-level, compiled once) ────────────────────────────
_RE_URL = re.compile(r"https?://\S+")
_RE_ARG_LABEL = re.compile(r"\w+ \([^)]+\):")
_RE_MULTI_SPACE = re.compile(r" +")
_RE_BLANK_LINE = re.compile(r"\n[ \t]*\n")
# A method without arguments starts its argument block at "Returns:".
# Section headers sit alone on their line, so a wrapped reference such as
# "... in Asset\n Returns: A New Approach." is not read as the Returns section.
_RE_DESCRIPTION = re.compile(
    r"([\s\S]*?)(?:^[ \t]*(?:Args|Returns):[ \t]*$|As an example:|\Z)", re.MULTILINE
)
_RE_ARGUMENTS = re.compile(
    r"((?:^[ \t]*(?:Args|Returns):[ \t]*$)[\s\S]*?)(```python|\Z)", re.MULTILINE
)
_RE_CODE = re.compile(r"```python([\s\S]*?)```", re.DOTALL)
_RE_RESULT = re.compile(r"Which returns:[\s\S]*$", re.DOTALL)
_RE_NUMBERED = re.compile(r"^\d+\. ")
_RE_LIST_ITEM = re.compile(r"^(- |\d+\. )")

# Section headers that get bolded wherever they appear as their own paragraph.
_BOLD_HEADERS = ("Also known as:", "See definition:", "See Definition:")

# ── Formula → LaTeX conversion ────────────────────────────────────────────────
# A bullet paragraph is treated as a set of formulas when the paragraph before
# it ends in a colon and reads like a formula introduction. Each such bullet is
# rendered as a $$ display-math block (kramdown turns those into \[...\] which
# MathJax picks up, see _includes/head/custom.html).
_RE_FORMULA_INTRO = re.compile(
    r"(?<!interpreted as )(formula|follows|translates into the following"
    r"|expresses the conditional variance|must hold|risk decomposition"
    r"|such returns|style options)[^:]*:$",
    re.IGNORECASE,
)

# Greek names spelled out in docstrings, mapped to their LaTeX symbols.
_GREEK = {
    "alpha": r"\alpha", "beta": r"\beta", "gamma": r"\gamma", "delta": r"\delta",
    "Delta": r"\Delta", "sigma": r"\sigma", "Sigma": r"\Sigma", "theta": r"\theta",
    "Theta": r"\Theta", "rho": r"\rho", "epsilon": r"\epsilon", "lambda": r"\lambda",
    "mu": r"\mu", "pi": r"\pi", "Phi": r"\Phi", "phi": r"\phi", "tau": r"\tau",
    "omega": r"\omega", "kappa": r"\kappa", "nu": r"\nu",
    "chi": r"\chi", "xi": r"\xi", "eta": r"\eta", "zeta": r"\zeta", "psi": r"\psi",
}

# Subscripts that contain an operator, protected from the tokenizer as one word.
_SUB_SENTINELS = {"_t-1": "_tminusone", "_t+1": "_tplusone", "_t+dt": "_tplusdt", "_t-dt": "_tminusdt"}
_SUB_RESTORE = {"tminusone": "t-1", "tplusone": "t+1", "tplusdt": "t+dt", "tminusdt": "t-dt"}

# Unicode used in docstring formulas, normalised to ASCII before tokenizing.
_UNICODE_MATH = {
    "σ": "sigma", "β": "beta", "α": "alpha", "Δ": "Delta ", "θ": "theta",
    "ρ": "rho", "ε": "epsilon", "π": "pi", "Φ": "Phi", "μ": "mu", "λ": "lambda",
    "²": "^2", "³": "^3", "−": "-", "×": "*", "·": "*", "≈": " ≈ ",
    "≤": " <= ", "≥": " >= ",
}

# Function-style names that get a proper LaTeX operator instead of \operatorname.
_FUNC_MAP = {
    "log10": r"\log_{10}", "log": r"\log", "ln": r"\ln", "exp": r"\exp",
    "max": r"\max", "Max": r"\max", "MAX": r"\max",
    "min": r"\min", "Min": r"\min", "MIN": r"\min",
}

# Literal indicator names that would otherwise be mangled by the tokenizer
# (leading +/- signs read as operators). Wrapped into opaque text atoms first.
_LITERAL_ATOMS = ("+DI", "-DI")

_RE_MATHY = re.compile(r" = | ≈ | \* | / |\*\*|\^| ~ | != | <= | >= ")


def _text_escape(text: str) -> str:
    """Escape LaTeX specials inside \\text{...} and drop markdown backticks."""
    for char, escaped in (("\\", ""), ("`", ""), ("_", r"\_"), ("%", r"\%"),
                          ("&", r"\&"), ("#", r"\#"), ("{", r"\{"), ("}", r"\}")):
        text = text.replace(char, escaped)
    return text


_BIG_OPERATORS = {"sum": r"\sum", "Sum": r"\sum", "prod": r"\prod", "Prod": r"\prod"}


def _greek_sub(sub: str) -> str | None:
    """Spell a subscript made of Greek names and single letters or digits ("pipi",
    "rpi", "0pi") symbol by symbol; None when it holds no Greek name at all."""
    names = sorted(_GREEK, key=len, reverse=True)
    out, i, greek = [], 0, False
    while i < len(sub):
        name = next((n for n in names if sub.startswith(n, i)), None)
        if name:
            out.append(_GREEK[name])
            i += len(name)
            greek = True
        elif sub[i].isalnum():
            out.append(sub[i])
            i += 1
        else:
            return None
    return " ".join(out) if greek else None


def _format_word(word: str) -> str:
    """Render one identifier token as LaTeX math."""
    if word.startswith("⟦") and word.endswith("⟧"):
        return r"\text{" + _text_escape(word[1:-1]) + "}"
    if word.startswith("⟪") and word.endswith("⟫"):  # LaTeX made before tokenizing (sums)
        return word[1:-1]
    if word in _GREEK:
        return _GREEK[word]
    if word.startswith("d") and word[1:] in _GREEK:  # a differential such as dchi
        return "d" + _GREEK[word[1:]]
    base, sep, sub = word.partition("_")
    if sep and base in _BIG_OPERATORS and "_" not in sub:
        # sum_i, prod_t: the operator with its index underneath
        return _BIG_OPERATORS[base] + "_{" + (_GREEK.get(sub) or _SUB_RESTORE.get(sub, sub)) + "}"
    if sep and len(sub) > 2 and sub[0] == "{" and sub[-1] == "}":
        # an explicit subscript: x_{t-1}
        return f"{_format_word(base)}_{{{sub[1:-1]}}}"
    if sep and re.fullmatch(r"\d+(\.\d+)?", sub):
        # a numeric subscript: VaR_0.995, P_10
        return f"{_format_word(base)}_{{{sub}}}"
    if sep:
        sub = _SUB_RESTORE.get(sub, sub)
        # Single-char suffixes are true subscripts. A short symbol (one letter, or a Greek
        # name) also takes a short or Greek subscript, nested when it has one itself:
        # sigma_chi, F_ij, p_s_t. Longer names are snake_case words such as net_income.
        if len(sub) <= 1 or sub in _SUB_RESTORE.values():
            return f"{_format_word(base)}_{{{sub}}}"
        short_base = base in _GREEK or (base[:1] == "d" and base[1:] in _GREEK) \
            or re.match(r"^d?[A-Za-z]'*$", base)
        head = sub.partition("_")[0]
        greek = _greek_sub(sub) if short_base and "_" not in sub and sub not in _GREEK else None
        if greek:
            return f"{_format_word(base)}_{{{greek}}}"
        if short_base and (head in _GREEK or re.match(r"^[A-Za-z0-9]{1,3}$", head)):
            inner = _format_word(sub) if "_" in sub else (_GREEK.get(sub) or sub)
            return f"{_format_word(base)}_{{{inner}}}"
        if re.match(r"^[A-Za-z]$", base) and re.match(r"^[A-Za-z]+$", sub):
            # one letter with a word label: f_anchor, C_next
            return f"{base}_{{\\text{{{sub}}}}}"
        return r"\text{" + _text_escape(word) + "}"
    match = re.match(r"^([A-Za-z])(\d+)$", word)
    if match:
        return f"{match.group(1)}_{{{match.group(2)}}}"
    if re.match(r"^[A-Za-z]'*(-\d+)?$", word):
        return word
    if word.startswith("%"):
        return r"\%" + _format_word(word[1:]) if len(word) > 1 else r"\%"
    if re.match(r"^[0-9.]+[A-Za-z]?%?$", word):
        return word.replace("%", r"\%")
    return r"\text{" + _text_escape(word) + "}"


def _format_word_run(words: list[str]) -> str:
    """Render a run of space-separated words, merging adjacent prose into \\text."""
    def is_prose(word: str) -> bool:
        return (word not in _GREEK and len(word) > 1 and not word.startswith("⟦")
                and not (word[:1] == "d" and word[1:] in _GREEK)
                and re.match(r"^[A-Za-z][A-Za-z'\-]*$", word) is not None
                and re.match(r"^[A-Za-z]'+$", word) is None)

    # A subscript on the final word applies to the whole phrase before it,
    # e.g. "Cash Flow Projection_t" becomes \text{Cash Flow Projection}_t.
    subscript = ""
    if words and "_" in words[-1]:
        base, _, sub = words[-1].partition("_")
        if is_prose(base) and base not in _BIG_OPERATORS and (len(sub) <= 1 or sub in _SUB_RESTORE):
            words = words[:-1] + [base]
            sub = _SUB_RESTORE.get(sub, sub)
            subscript = f"_{{{sub}}}"

    parts: list[str] = []
    prose_run: list[str] = []
    for word in words:
        if is_prose(word):
            prose_run.append(word)
            continue
        if prose_run:
            # prose after a symbol ("R_i given R_i") gets space on both sides
            pad = r"\;" if parts else ""
            parts.append(pad + r"\text{" + _text_escape(" ".join(prose_run)) + r"}\;")
            prose_run = []
        parts.append(_format_word(word))
    if prose_run:
        pad = r"\;" if parts else ""
        parts.append(pad + r"\text{" + _text_escape(" ".join(prose_run)) + "}")
    return " ".join(parts) + subscript


def _tokenize_formula(text: str, pos: int = 0, closer: str = "") -> tuple[list, int]:
    """Split a formula into atoms, operators and (recursive) paren groups."""
    tokens: list = []
    word = ""

    def flush():
        nonlocal word
        if word:
            tokens.append(("word", word))
            word = ""

    while pos < len(text):
        char = text[pos]
        if char == closer:
            flush()
            return tokens, pos + 1
        if char in "⟦⟪":
            end = text.find("⟧" if char == "⟦" else "⟫", pos)
            word += text[pos:end + 1]
            pos = end + 1
            continue
        if char in "([":
            flush()
            group, pos = _tokenize_formula(text, pos + 1, ")" if char == "(" else "]")
            tokens.append(("group", char, group))
            continue
        # Two-character comparisons first: != <= >=
        if text[pos:pos + 2] in ("!=", "<=", ">="):
            flush()
            tokens.append(("op", text[pos:pos + 2]))
            pos += 2
            continue
        if char in "=+-*/^,|<>≈~":
            # A hyphen glued between word characters is part of the name, not a minus.
            if char == "-" and word and pos + 1 < len(text) and text[pos + 1].isalnum() \
                    and text[pos - 1].isalnum() and word[-1] != " ":
                word += char
                pos += 1
                continue
            flush()
            if text[pos:pos + 2] == "**":
                tokens.append(("op", "^"))
                pos += 2
                continue
            tokens.append(("op", char))
            pos += 1
            continue
        if char == " ":
            if word:
                word += char
            pos += 1
            continue
        word += char
        pos += 1
    flush()
    return tokens, pos


def _render_tokens(tokens: list) -> str:
    """Render a token list to LaTeX, handling word runs, functions and exponents."""
    parts: list[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token[0] == "word":
            words = [w for w in token[1].split(" ") if w]
            trailing_space = token[1].endswith(" ")
            # A single word glued to a following group is a function call.
            if (len(words) == 1 and not trailing_space and i + 1 < len(tokens)
                    and tokens[i + 1][0] == "group" and tokens[i + 1][1] == "("):
                name = words[0]
                group = _render_tokens(tokens[i + 1][2])
                if name in ("sqrt", "SQRT", "√"):
                    parts.append(r"\sqrt{" + group + "}")
                elif name in _FUNC_MAP:
                    parts.append(_FUNC_MAP[name] + "(" + group + ")")
                elif name in _GREEK or re.match(r"^[A-Za-z]'*$", name) \
                        or ("_" in name and _format_word(name) != r"\text{" + _text_escape(name) + "}"):
                    parts.append(_format_word(name) + "(" + group + ")")
                else:
                    parts.append(r"\operatorname{" + _text_escape(name) + "}(" + group + ")")
                i += 2
                continue
            parts.append(_format_word_run(words))
            i += 1
            continue
        if token[0] == "group":
            inner = _render_tokens(token[2])
            parts.append(f"({inner})" if token[1] == "(" else r"\left[" + inner + r"\right]")
            i += 1
            continue
        op = token[1]
        if op == "^":
            exponent = ""
            j = i + 1
            if j < len(tokens) and tokens[j][0] == "op" and tokens[j][1] == "-":
                exponent = "-"
                j += 1
            if j < len(tokens) and tokens[j][0] == "group":
                exponent += _render_tokens(tokens[j][2])
                j += 1
            elif j < len(tokens) and tokens[j][0] == "word":
                first_word = tokens[j][1].split(" ")[0]
                exponent += _format_word(first_word)
                remainder = tokens[j][1][len(first_word):].strip()
                tokens[j] = ("word", remainder)
                if not remainder:
                    j += 1
            parts.append("^{" + exponent + "}")
            i = j
            continue
        parts.append({"*": r"\cdot", "≈": r"\approx", ",": ",\\;", "!=": r"\neq", "<=": r"\leq",
                      ">=": r"\geq", "~": r"\sim"}.get(op, op))
        i += 1
    return " ".join(parts).replace(" ,\\;", ",\\;")


def _sum_limit(text: str) -> str:
    """Render a summation limit such as "t=2", "i<j" or "min(n, lags)"."""
    text = re.sub(r"\s+", "", text).replace("<=", r" \leq ").replace("inf", r"\infty")
    text = re.sub(r"\b(min|max)\(", lambda m: "\\" + m.group(1) + "(", text)
    return re.sub(r"\b(lags|power)\b", r"\\text{\1}", text)


def _sum_to_latex(match: re.Match) -> str:
    low = match.group(1) or match.group(2)
    high = match.group(3) or match.group(4) or match.group(5)
    latex = r"\sum_{" + _sum_limit(low) + "}"
    if high:
        latex += "^{" + _sum_limit(high) + "}"
    return "⟪" + latex + "⟫"


def _formula_to_latex(line: str) -> str:
    """Convert one plain-text formula bullet into a $$ display-math block."""
    formula = line.lstrip("- ").rstrip().rstrip(".")
    formula = formula.replace("&#124;", "|")
    for literal in _LITERAL_ATOMS:
        formula = formula.replace(literal, f"⟦{literal}⟧")
    for char, replacement in _UNICODE_MATH.items():
        formula = formula.replace(char, replacement)
    for literal, sentinel in _SUB_SENTINELS.items():
        formula = formula.replace(literal, sentinel)
    formula = re.sub(r"√\s*([A-Za-z0-9.]+)", r"sqrt(\1)", formula)
    # SUM_{t=2}^{n}, SUM_{i<j} and SUM_i become a summation sign with its limits.
    formula = re.sub(
        r"\bSUM_(?:\{([^{}]*)\}|([A-Za-z0-9]+))(?:\^(?:\{([^{}]*)\}|\(([^()]*)\)|([A-Za-z0-9]+)))?",
        _sum_to_latex,
        formula,
    )

    # A leading "Label: formula" keeps the label as one prose chunk.
    label = ""
    match = re.match(r"^([^=^]+?):\s+(.*)$", formula)
    if match and _RE_MATHY.search(match.group(2)):
        label = r"\text{" + _text_escape(match.group(1)) + r":}\;\; "
        formula = match.group(2)

    # Split into top-level comma segments so trailing prose clauses stay prose.
    segments: list[str] = []
    depth = 0
    current = ""
    for char in formula:
        if char in "([":
            depth += 1
        elif char in ")]":
            depth -= 1
        if char == "," and depth == 0:
            segments.append(current)
            current = ""
        else:
            current += char
    segments.append(current)

    rendered: list[str] = []
    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue
        prefix = ""
        match = re.match(r"^(where|over|for)\s+(.*)$", segment)
        if match and _RE_MATHY.search(match.group(2)):
            prefix = r"\text{" + match.group(1) + r"} \;\; "
            segment = match.group(2)
        if _RE_MATHY.search(segment) or " = " in f" {segment} ":
            tokens, _ = _tokenize_formula(segment)
            latex = _render_tokens(tokens)
            # "u_(t-1)": the bracket is the subscript, not an argument
            latex = re.sub(r"_\{\}\s*\(([^()]*)\)", lambda m: "_{" + m.group(1) + "}", latex)
            rendered.append(prefix + latex)
        else:
            rendered.append(r"\text{" + _text_escape(segment) + "}")
    return "$$\n" + label + ",\\;\\; ".join(rendered) + "\n$$"


def _looks_like_formula(line: str) -> bool:
    return _RE_MATHY.search(line) is not None


# ── Inline formulas ───────────────────────────────────────────────────────────
# A formula inside a sentence ("found by minimizing 1/2 w'Σw - Σ b_i ln(w_i)")
# becomes inline math: $$...$$ inside a paragraph, which kramdown turns into
# \(...\). The docstrings keep plain Unicode, which reads better in help(), IDEs
# and the MCP server, so the conversion happens here. A span is a run of
# symbolic words joined by operators, and it is only converted when it holds a
# real math signal: words, numbers, code and worked numeric examples stay text.

_GREEK_CHARS = {
    "α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "epsilon", "ζ": "zeta",
    "η": "eta", "θ": "theta", "κ": "kappa", "λ": "lambda", "μ": "mu", "ν": "nu", "ξ": "xi",
    "π": "pi", "ρ": "rho", "σ": "sigma", "τ": "tau", "φ": "phi", "χ": "chi", "ψ": "psi",
    "ω": "omega", "Γ": "Gamma", "Δ": "Delta", "Θ": "Theta", "Λ": "Lambda", "Π": "Pi",
    "Σ": "Sigma", "Φ": "Phi", "Ψ": "Psi", "Ω": "Omega",
}
_GREEK_NAMES = {name for name in _GREEK_CHARS.values() if name.islower()} | {"iota"}

# Unicode sub- and superscripts, rewritten as _{...} and ^{...} before rendering.
_SUBSCRIPT_CHARS = dict(zip("₀₁₂₃₄₅₆₇₈₉₊₋ₜᵢⱼₖₙₘₐₑₒₓₕₗₚₛᵣᵤᵥ", "0123456789+-tijknmaeoxhlpsruv"))
_SUPERSCRIPT_CHARS = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ⁿᵀⁱ", "0123456789-+nTi"))

_INLINE_OPS = {
    "=": "=", "≈": r"\approx", "≤": r"\leq", "≥": r"\geq", "<=": r"\leq", ">=": r"\geq",
    "≠": r"\neq", "!=": r"\neq", "<": "<", ">": ">", "+": "+", "-": "-", "−": "-",
    "×": r"\times", "*": r"\cdot", "·": r"\cdot", "/": "/", "÷": r"\div", "~": r"\sim",
    "|": r"\vert", "→": r"\to",
}
# Operators that are a math signal on their own (an = needs symbols on both sides).
_SIGNAL_OPS = {"≈", "≤", "≥", "≠", "×", "÷"}
_INLINE_NAMES = {"sign": r"\operatorname{sign}", "Var": r"\operatorname{Var}",
                 "Cov": r"\operatorname{Cov}", "Std": r"\operatorname{Std}"}

_GREEK_ALT = "|".join(sorted(_GREEK_NAMES, key=len, reverse=True))
# x_t, σ_p, sigma_(n+1), RSS_r, w0_i, z_alpha: a short symbol with a short subscript.
# Lowercase snake_case names (end_date, is_etf, beta_lower) are not symbols.
_RE_INLINE_SUB = re.compile(
    r"(?<![A-Za-z0-9_])(?:[A-Za-z]\d?|[A-Z][A-Za-z]{1,2}|" + _GREEK_ALT + r"|[α-ωΓ-Ω])"
    r"[\u0302\u0304']*_(?:[({]|(?:\d+|[A-Za-z]{1,4}|" + _GREEK_ALT + r"|[α-ω])(?![A-Za-z0-9_]))"
)
_RE_INLINE_SIGNAL = re.compile(
    r"[α-ωΓΘΛΠΣΦΨΩ√∑∂\u0302\u0304≈×≤≥≠÷·" + "".join(_SUBSCRIPT_CHARS) + "".join(_SUPERSCRIPT_CHARS)
    + r"]|Δ(?:[A-Za-z](?![A-Za-z])|\d)|\w\^"
)
# A long word squared ("Implied Volatility²", "Price²") is a word formula, not a symbol.
_RE_WORD_POWER = re.compile(r"[A-Za-z]{4,}[²³]")
_RE_SYMBOL_ATOM = re.compile(
    r"-?\d+(\.\d+)?(e-?\d+)?%?|-?[A-Za-z]'*\*?|[A-Za-z]\d{1,2}'*|\d[a-z]{1,2}|d[A-Za-z]"
    r"|[A-Z][A-Za-z]{0,5}\*?|\.\.\.|ln|exp|max|min|log|sqrt|sign|" + _GREEK_ALT
)
# One-letter English words and spelled Greek names ("sigma (σ)") are only symbols
# next to an operator ("a + b < 1").
_AMBIGUOUS = {"a", "A", "I", "x"}
# Markdown and text that are never part of a formula.
_RE_INLINE_PROTECTED = re.compile(
    r"`[^`\n]*`|\[[^\]\n]*\]\((?:[^()\s]|\([^()\s]*\))*\)(?:\{:[^}\n]*\})?|https?://\S+"
    r"|<u>.*?</u>|\*\*[^*\n]+\*\*|^\s*(?:[-*]|\d+\.)\s+"
)

_INLINE_CONTEXT = {"page": "", "function": ""}
_INLINE_LOG: list[dict] = []  # every converted span, written out with DOCS_INLINE_MATH_LOG


def _inline_word_class(core: str) -> str:
    """O(perator), M(ath signal), S(ymbol), A(mbiguous letter), C(apitalized name) or W(ord)."""
    if core in _INLINE_OPS:
        return "O"
    # a word applied to a symbol ("Spot Rate(τ)") is a word formula, ln(Backcast) a name;
    # sigma_2 is how the GARCH docstrings write σ², so it stays as written
    call = re.match(r"([A-Za-z]{3,})\(", core)
    name = call.group(1) if call else ""
    if call and name not in _FUNC_MAP and name not in _INLINE_NAMES and name != "sqrt" \
            and sum(c.isupper() for c in name) < 2 or core == "sigma_2":
        return "W"
    if "@" in core or re.search(r"[A-Z]{2,}_[A-Z]{2,}", core):  # dataset codes: DSD_HSL@DF_HSL
        return "W"
    if re.fullmatch(r"(?:ln|log|exp)\([A-Z][a-z]+\)", core):
        return "C"
    if _RE_INLINE_SIGNAL.search(_RE_WORD_POWER.sub("", core)) or _RE_INLINE_SUB.search(core):
        return "M"
    atoms = [a for a in re.split(r"[()\[\]{},|/]+", core) if a]
    if all(_RE_SYMBOL_ATOM.fullmatch(a) for a in atoms):
        if core.strip("()[],") in _AMBIGUOUS or core.strip("()[],") in _GREEK_NAMES:
            return "A"
        # capitalized words such as "The" or "Std" are no symbols, and neither are longer
        # acronyms (GARCH, LPFD); short ones are (IR, VaR, SR*)
        if all(not re.fullmatch(r"[A-Z][a-z]{1,5}|[A-Z]{3,}", a) or a in _INLINE_NAMES for a in atoms):
            return "S"
    if re.fullmatch(r"[A-Z][a-z]+|[A-Z]{3,}(\([^)]*\))?", core.strip("()")):
        return "C"
    return "W"


class _Inline:
    """Render one plain-text formula span as LaTeX."""

    def __init__(self, text: str):
        # Ŷ and ȳ come apart into a letter and a combining hat or bar
        text = unicodedata.normalize("NFD", text)
        text = text.replace("&#124;", "|").replace("−", "-").replace("…", "...")
        text = re.sub("[" + "".join(_SUBSCRIPT_CHARS) + "]+",
                      lambda m: "_{" + "".join(_SUBSCRIPT_CHARS[c] for c in m.group(0)) + "}", text)
        text = re.sub("[" + "".join(_SUPERSCRIPT_CHARS) + "]+",
                      lambda m: "^{" + "".join(_SUPERSCRIPT_CHARS[c] for c in m.group(0)) + "}", text)
        self.s = text
        self.pos = 0
        self.pending_sub = ""  # digits glued to the last symbol, its subscript

    def render(self) -> str:
        return self.sequence("")

    def sequence(self, closer: str) -> str:
        parts: list[str] = []
        while self.pos < len(self.s):
            char = self.s[self.pos]
            if closer and char == closer:
                self.pos += 1
                break
            if char == " ":
                self.pos += 1
                continue
            parts.append(self.item())
        return " ".join(p for p in parts if p)

    def item(self) -> str:
        s, char = self.s, self.s[self.pos]
        if s.startswith("...", self.pos) or s.startswith("..", self.pos):
            self.pos += 3 if s.startswith("...", self.pos) else 2
            return r"\ldots"
        two = s[self.pos:self.pos + 2]
        if two in ("<=", ">=", "!="):
            self.pos += 2
            return _INLINE_OPS[two]
        if char == "*" and self.pos > 0 and s[self.pos - 1] != " ":
            self.pos += 1  # a star glued to its symbol: SR*, σ*
            return "^{*}"
        if char in _INLINE_OPS:
            self.pos += 1
            return _INLINE_OPS[char]
        if char in ",;":
            self.pos += 1
            return char
        if char == "%":
            self.pos += 1
            return r"\%"
        return self.postfix(self.atom())

    def atom(self) -> str:
        s, char = self.s, self.s[self.pos]
        if char in "([{":
            self.pos += 1
            inner = self.sequence({"(": ")", "[": "]", "{": "}"}[char])
            return {"(": f"({inner})", "[": f"[{inner}]", "{": rf"\{{{inner}\}}"}[char]
        if char == "√":
            self.pos += 1
            if self.pos < len(s) and s[self.pos] == "(":
                self.pos += 1
                return r"\sqrt{" + self.sequence(")") + "}"
            inner = self.postfix(self.atom())
            if self.pos < len(s) and s[self.pos] == "(":  # √Var(...)
                inner += " " + self.atom()
            return r"\sqrt{" + inner + "}"
        if char == "½":
            self.pos += 1
            return r"\tfrac{1}{2}"
        if char == "∂":
            self.pos += 1
            return r"\partial"
        if char in _GREEK_CHARS:
            self.pos += 1
            name = _GREEK_CHARS[char]
            if char == "Σ":
                # Σ is a sum before an index or a term ("Σ w_i", "Σ_(s≤t)", "Σ(1/σ_j)"),
                # and the covariance matrix when glued to a symbol ("w'Σw", "τΣ", "Σ_AA") or
                # followed by an operator ("Σ + M"). After a division it is a sum ("y / Σy").
                before = s[self.pos - 2] if self.pos >= 2 else " "
                nxt = s[self.pos:self.pos + 1]
                after = s[self.pos:].lstrip(" ")
                glued = before.isalnum() or before in "'" or before in _GREEK_CHARS
                if s[:self.pos - 1].rstrip().endswith("/") or not glued and (
                        nxt in (" ", "(", "[") and after and (after[0] == "|" or after[0] not in _INLINE_OPS)
                        and after[0] not in ",)" or nxt == "_" and not s[self.pos + 1:self.pos + 2].isupper()):
                    return r"\sum"
            return "\\" + name + self.digits()
        match = re.compile(r"[A-Za-z]+").match(s, self.pos)
        if match:
            word = match.group(0)
            self.pos = match.end()
            if word == "sqrt" and s[self.pos:self.pos + 1] == "(":
                self.pos += 1
                return r"\sqrt{" + self.sequence(")") + "}"
            if word in _FUNC_MAP:
                return _FUNC_MAP[word]
            if word in _INLINE_NAMES:
                return _INLINE_NAMES[word]
            if word in _GREEK_NAMES:
                return "\\" + word + self.digits()
            if len(word) == 1 or (len(word) == 2 and word.islower()) or re.fullmatch(r"d[A-Z]", word):
                return word + self.digits()
            return r"\text{" + _text_escape(word) + "}" + self.digits()
        match = re.compile(r"(\d+)/(\d+)(?![\d.])").match(s, self.pos)
        if match:  # 1/2 w'Σw
            self.pos = match.end()
            return r"\tfrac{" + match.group(1) + "}{" + match.group(2) + "}"
        match = re.compile(r"\d+(\.\d+)?").match(s, self.pos)
        if match:
            self.pos = match.end()
            return match.group(0)
        self.pos += 1
        return r"\text{" + _text_escape(char) + "}"

    def digits(self) -> str:
        """Digits glued to a symbol are its subscript: d1, β0, τ1."""
        match = re.compile(r"\d+").match(self.s, self.pos)
        if not match:
            return ""
        self.pos = match.end()
        self.pending_sub = match.group(0)
        return ""

    def postfix(self, atom: str) -> str:
        s = self.s
        sub, sup, primes = self.pending_sub, "", ""
        self.pending_sub = ""
        while self.pos < len(s):
            char = s[self.pos]
            if char in "\u0302\u0304":
                command = r"\hat" if char == "\u0302" else r"\bar"
                if atom.startswith(r"\text"):
                    command = r"\widehat" if char == "\u0302" else r"\overline"
                atom = command + "{" + atom + "}"
                self.pos += 1
            elif char == "'":
                if sub or sup:
                    primes += "'"  # r_t'w: the transpose of r_t
                else:
                    atom += "'"
                self.pos += 1
            elif char == "*" and (self.pos + 1 == len(s) or s[self.pos + 1] in " ),^]"):
                sup += "*"
                self.pos += 1
            elif char == "_":
                self.pos += 1
                sub = (sub + "," if sub else "") + self.script(subscript=True)
            elif char == "^":
                self.pos += 1
                sup += self.script(subscript=False)
            else:
                break
        if sub:
            atom += "_{" + sub + "}"
        if sup:
            atom += "^{" + sup + "}"
        return atom + primes

    def script(self, subscript: bool) -> str:
        s = self.s
        if self.pos >= len(s):
            return ""
        char = s[self.pos]
        if char in "({":
            self.pos += 1
            return self.sequence(")" if char == "(" else "}")
        if char == "|":
            end = s.find("|", self.pos + 1)
            if end != -1:
                inner = _Inline(s[self.pos + 1:end]).render()
                self.pos = end + 1
                return r"\vert " + inner + r" \vert"
        if char == "-":
            self.pos += 1
            return "-" + self.script(subscript)
        if char in _GREEK_CHARS:
            self.pos += 1
            return "\\" + _GREEK_CHARS[char]
        pattern = r"[A-Za-z0-9]+(?:,[A-Za-z0-9]+)*" if subscript else r"[A-Za-z0-9]+|\d+(\.\d+)?"
        match = re.compile(pattern).match(s, self.pos)
        if not match:
            return ""
        self.pos = match.end()
        pieces = []
        for piece in match.group(0).split(","):
            if piece in _GREEK_NAMES:
                pieces.append("\\" + piece)
            elif piece.isdigit() or len(piece) == 1 or re.fullmatch(r"[ijklmnpqst]{2}", piece):
                pieces.append(piece)
            else:
                pieces.append(r"\text{" + _text_escape(piece) + "}")
        return ",".join(pieces)


def _inline_to_latex(span: str) -> str:
    return _Inline(span).render()


def _balance(span: str) -> tuple[str, str, str] | None:
    """Move unmatched brackets at either end, and a pair wrapping the whole span,
    out of the formula: "(σ)" keeps its parentheses as text. None when the
    brackets don't match inside the span."""
    lead = trail = ""
    pairs = {")": "(", "]": "[", "}": "{"}
    for _ in range(len(span)):
        stack, unmatched = [], []
        for i, char in enumerate(span):
            if char in "([{":
                stack.append(i)
            elif char in pairs:
                if stack and span[stack[-1]] == pairs[char]:
                    opened = stack.pop()
                    if opened == 0 and i == len(span) - 1:
                        unmatched = [0, i]
                else:
                    unmatched.append(i)
        unmatched = sorted(set(unmatched + stack))
        if not unmatched:
            return lead, span, trail
        if unmatched[0] == 0:
            lead += span[0]
            span = span[1:].lstrip()
        elif unmatched[-1] == len(span) - 1:
            trail = span[-1] + trail
            span = span[:-1].rstrip()
        else:
            return None
        if not span:
            return None
    return None


def _inline_spans(text: str) -> list[tuple[int, int, str]]:
    """Find the formula spans of a stretch of prose: (start, end, latex)."""
    words = [(m.start(), m.end(), m.group(0)) for m in re.finditer(r"\S+", text)]
    cores, classes = [], []
    for start, end, word in words:
        lead = len(word) - len(word.lstrip("\"'“‘"))
        core = word[lead:]
        if not re.fullmatch(r"\.{2,}[,;:]?", core):
            core = core.rstrip(".,;:!?\"”’")
        cores.append((start + lead, start + lead + len(core), core, word[lead + len(core):]))
        classes.append(_inline_word_class(core) if core else "W")

    def op(i):
        return 0 <= i < len(classes) and classes[i] == "O"

    keep = []
    for i, cls in enumerate(classes):
        if cls == "A":
            keep.append(op(i - 1) or op(i + 1))
        elif cls == "C":
            # a name between operators ("= Omega + Alpha *"), or ending the formula
            keep.append(op(i - 1) and (op(i + 1) or bool(cores[i][3]) or i == len(classes) - 1
                                       or cores[i][2].endswith(")")))
        else:
            keep.append(cls in "MSO")

    # runs of kept words, broken at sentence and clause punctuation outside brackets
    runs, run, depth = [], [], 0
    for i, kept in enumerate(keep):
        if not kept or (run and words[i][2][:1] in "\"'“‘"):
            if run:
                runs.append(run)
            run, depth = [], 0
            if not kept:
                continue
        run.append(i)
        core = cores[i][2]
        depth += sum(core.count(c) for c in "([{") - sum(core.count(c) for c in ")]}")
        if cores[i][3] and depth <= 0:
            runs.append(run)
            run, depth = [], 0
    if run:
        runs.append(run)

    spans = []
    for run in runs:
        while run and classes[run[0]] == "O":
            run = run[1:]
        while run and classes[run[-1]] == "O":
            run = run[:-1]
        if not run:
            continue
        # brackets that don't match inside the span ("β2 (a hump"): drop words from the end
        balanced = None
        while run and not balanced:
            start, end = cores[run[0]][0], cores[run[-1]][1]
            balanced = _balance(text[start:end])
            if not balanced:
                run = run[:-1]
        if not balanced:
            continue
        lead, span, trail = balanced
        start = text.index(span, start + len(lead))
        end = start + len(span)
        # an operator left dangling once a bracket is moved out ("(t_i ≥ w_i, ... Σ t_i ≤")
        while span and span.split(" ")[-1] in _INLINE_OPS:
            span = span.rsplit(" ", 1)[0].rstrip() if " " in span else ""
            end = start + len(span)
        if not span:
            continue

        inside = [i for i in run if cores[i][1] > start and cores[i][0] < end]
        run_classes = [classes[i] for i in inside]
        run_words = [cores[i][2].strip("()[]") for i in inside]
        signal = "M" in run_classes or any(w in _SIGNAL_OPS for w in run_words)
        if "C" in run_classes:  # "1 × Strong Buy + 2 × Buy" is a sum in words
            signal = "M" in run_classes
        for k, word in enumerate(run_words):
            # an (in)equation between symbols ("h = 1", "H < 0.5"), not between numbers ("2015 = 100")
            if word in ("=", "<", ">", "<=", ">=") and 0 < k < len(run_words) - 1 \
                    and run_classes[k - 1] in "MSA" and run_classes[k + 1] in "MSA" \
                    and re.search(r"[A-Za-z]", run_words[k - 1] + run_words[k + 1]):
                signal = True
        # a comparison cut out of a bracket ("Count(|x| < |y|, s < t)") is part of a word formula
        if "M" not in run_classes and lead + trail and not (lead in "([" and trail in ")]" and lead and trail):
            continue
        if not signal or not re.search(r"[^\W\d_]", span):
            continue
        # a lone Σ is the covariance matrix ("where Σ is", "with Σ the"), but "the sum of"
        # before a noun ("Σ contribution / Σ start weight")
        nxt = run[-1] + 1
        if span == "Σ" and nxt < len(classes) and classes[nxt] in "WC" \
                and cores[nxt][2] not in ("is", "the", "their", "itself", "and", "as"):
            continue
        spans.append((start, end, _inline_to_latex(span)))
    return spans


def _inline_math(text: str) -> str:
    """Wrap the formula spans of prose lines in $$...$$ (inline math). Lines in
    display-math blocks and code blocks, table rows, headings and the "Also known
    as" names are left alone; links, code and argument labels are skipped."""
    out, in_math, in_code = [], False, False
    lines = text.split("\n")
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
        if stripped == "$$":
            in_math = not in_math
        if in_code or in_math or stripped in ("$$", "") or stripped.startswith(("|", "#", "**Also known as:**")):
            out.append(line)
            continue
        pieces, last = [], 0
        for protected in list(_RE_INLINE_PROTECTED.finditer(line)) + [None]:
            stop = protected.start() if protected else len(line)
            # a pipe is &#124; in the Markdown (_escape_pipes) and \vert in the math
            free = line[last:stop].replace("&#124;", "|")
            cursor = 0
            for start, end, latex in _inline_spans(free):
                # glued to code or a link ("int(`train_fraction`·n)"): part of that, not a formula
                if (start == 0 and last > 0 and not line[last - 1].isspace()) \
                        or (end == len(free) and protected):
                    continue
                pieces.append(free[cursor:start].replace("|", "&#124;") + "$$" + latex + "$$")
                _INLINE_LOG.append({**_INLINE_CONTEXT, "text": free[start:end], "latex": latex})
                cursor = end
            pieces.append(free[cursor:].replace("|", "&#124;"))
            if protected:
                pieces.append(protected.group(0))
                last = protected.end()
        line = "".join(pieces)
        # a paragraph that is nothing but formulas ("λ = s / (1 - R), P(t_n) = ...")
        # is a display formula
        alone = (index == 0 or not lines[index - 1].strip()) \
            and (index == len(lines) - 1 or not lines[index + 1].strip())
        formulas = re.findall(r"\$\$(.+?)\$\$", line)
        if alone and formulas and not re.sub(r"\$\$.+?\$\$", "", line).strip(" ,.;"):
            line = "$$\n" + r",\quad ".join(formulas) + "\n$$"
        out.append(line)
    return "\n".join(out)

_GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
_REQUEST_TIMEOUT = 30

# ── Local mode ──────────────────────────────────────────────────────────────
# Set DOCS_LOCAL_PATH (or pass --local) to read controller modules straight
# off disk instead of hitting the GitHub API. Points at the financetoolkit
# package directory, e.g. /Users/jeroenbouma/Documents/FinanceToolkit/financetoolkit
_DEFAULT_LOCAL_PATH = "/Users/jeroenbouma/Documents/FinanceToolkit/financetoolkit"
_LOCAL_PATH = os.environ.get("DOCS_LOCAL_PATH", "")
if "--local" in sys.argv and not _LOCAL_PATH:
    _LOCAL_PATH = _DEFAULT_LOCAL_PATH

_INSTALL_SNIPPET = """\
Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or install the Python package:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

"""

# The Portfolio class is not in the MCP.
_INSTALL_SNIPPET_PYTHON = """\
To install the FinanceToolkit it simply requires the following:

```python
pip install financetoolkit -U
```

{% include algolia.html %}

"""


def _trim_url(url: str) -> tuple[str, str]:
    """Split a raw regex match into (url, trailing_punctuation).

    Sentence punctuation directly after a URL (e.g. "See https://x.com.")
    is not part of the link, but a closing paren that balances one inside
    the URL itself (e.g. Wikipedia's ".../wiki/Beta_(finance)") is.
    """
    trailing = ""
    while url and url[-1] in ".,;:!?":
        trailing = url[-1] + trailing
        url = url[:-1]
    if url.endswith(")") and url.count("(") < url.count(")"):
        trailing = ")" + trailing
        url = url[:-1]
    return url, trailing


def _escape_pipes(text: str) -> str:
    """Write | as &#124; outside inline code.

    A bare pipe (|x| as an absolute value, or "int | str" in a type) can make
    kramdown read the line as a table, and a backslash escape shows up
    literally inside the <u> argument labels. The HTML entity renders as a
    plain | everywhere and never starts a table. Inside backticks the entity
    would be shown as-is, so code spans keep their real pipe.
    """
    parts = re.split(r"(`[^`\n]*`)", text)
    return "".join(p if p.startswith("`") else p.replace("|", "&#124;") for p in parts)


def _linkify(text: str) -> str:
    def _replace(match: re.Match) -> str:
        url, trailing = _trim_url(match.group(0))
        return f'[{url}]({url}){{:target="_blank"}}{trailing}'

    return _RE_URL.sub(_replace, text)


def _underline_arg(match: re.Match) -> str:
    return f"- <u>{match.group(0)}</u>"


def _dedent_block(text: str) -> str:
    """Strip the docstring's fixed source indentation while preserving any
    relative indentation the author used (e.g. nested multi-line calls or
    aligned table columns).

    The section regexes (Args:, Which returns:, ...) match starting mid-line,
    right after the header text, so the first captured line often has zero
    leading whitespace even though every other line shares the docstring's
    real indent. That lone unindented line would otherwise fool
    `textwrap.dedent` into stripping nothing at all, so it is excluded when
    the common indent is computed.
    """
    lines = text.strip("\n").split("\n")
    if not lines:
        return ""

    indents = [len(l) - len(l.lstrip(" ")) for l in lines[1:] if l.strip()]
    if not indents:
        return "\n".join(l.strip() for l in lines).strip()

    base = min(indents)
    dedented = [lines[0].strip()] + [
        l[base:] if l.strip() else "" for l in lines[1:]
    ]
    return "\n".join(dedented).strip("\n")


def _clean_description(text: str) -> str:
    """Turn a raw docstring description into clean Markdown.

    Paragraphs are detected via blank lines (the only reliable signal in the
    source). A paragraph is treated as a bullet list whenever its first line
    starts with "- " once dedented - anything else (formula minus signs,
    hyphenated words, negative numbers) is left alone. Wrapped continuation
    lines that don't themselves start with "- " (Google-style docstrings
    often indent a bullet's second line instead of repeating the marker) are
    folded back onto the bullet they continue, rather than breaking list
    detection for the whole paragraph.

    Source docstrings often put a blank line between each bullet (for their
    own readability). If that blank line survived into the Markdown, Kramdown
    would render the list as "loose" - wrapping each item's text in its own
    <p> - which double-applies the site's `.page__content li { font-size:
    0.8em }` rule (once for the <li>, again for the nested <p>) and renders
    the bullets visibly smaller than surrounding text. Consecutive
    bullet-list paragraphs are therefore joined with a single newline so
    Kramdown treats them as one tight list instead.
    """
    text = text.replace("—", "-")  # em dash -> hyphen, used for formula minus signs
    text = _escape_pipes(text)  # so |x| (absolute value) isn't parsed as a table
    text = text.replace("The formula is a follows:", "The formula is as follows:")

    paragraphs = []
    for raw_paragraph in _RE_BLANK_LINE.split(_dedent_block(text)):
        lines = [_RE_MULTI_SPACE.sub(" ", line.strip()) for line in raw_paragraph.split("\n")]
        lines = [line for line in lines if line]
        if not lines:
            continue

        for header in _BOLD_HEADERS:
            if lines[0].startswith(header):
                lines[0] = f"**{header}**{lines[0][len(header):]}"
                break

        # A list can start part-way through a paragraph ("It contains the
        # following columns:" directly followed by "- Open: ..."), and
        # numbered items can carry their own bullets (the Piotroski criteria).
        # Two or more list lines make it a list; a single line that happens to
        # start with "- " is more likely a wrapped dash in running text.
        item_lines = [i for i, line in enumerate(lines) if _RE_LIST_ITEM.match(line)]
        if len(item_lines) >= 2 or (item_lines and item_lines[0] == 0):
            first = item_lines[0]
            if first > 0:
                paragraphs.append((" ".join(lines[:first]), False))  # the lead-in sentence
            merged = []
            in_numbered = False
            for line in lines[first:]:
                if _RE_NUMBERED.match(line):
                    merged.append(line)
                    in_numbered = True
                elif line.startswith("- "):
                    merged.append(("   " if in_numbered else "") + line)  # nest under the number
                else:
                    merged[-1] = f"{merged[-1]} {line}"  # fold wrapped continuation into its item
            paragraph = "\n".join(merged)
            starts_as_bullet = True
        else:
            paragraph = " ".join(lines)
            starts_as_bullet = False
        paragraphs.append((paragraph, starts_as_bullet))

    # Bullet paragraphs directly after a formula introduction become math blocks.
    for i, (paragraph, starts_as_bullet) in enumerate(paragraphs):
        if not starts_as_bullet or i == 0:
            continue
        intro = paragraphs[i - 1][0].rstrip()
        # any introduction ending in a colon counts when every bullet is an equation
        equations = all(" = " in line and _looks_like_formula(line) for line in paragraph.split("\n"))
        if not (_RE_FORMULA_INTRO.search(intro) or (intro.endswith(":") and equations)):
            continue
        blocks = []
        for line in paragraph.split("\n"):
            blocks.append(_formula_to_latex(line) if _looks_like_formula(line) else line)
        paragraphs[i] = ("\n\n".join(blocks), False)

    parts = []
    for i, (paragraph, starts_as_bullet) in enumerate(paragraphs):
        if i > 0:
            parts.append("\n" if starts_as_bullet and paragraphs[i - 1][1] else "\n\n")
        parts.append(paragraph)

    return "".join(parts)


def _local_file_path(file_url: str) -> str:
    """Map a GitHub contents-API URL to its local file path under _LOCAL_PATH."""
    relative_path = file_url.split(f"{_BASE}/", 1)[1]
    return os.path.join(_LOCAL_PATH, relative_path)


def _fetch_file(url: str) -> str:
    if _LOCAL_PATH:
        local_path = _local_file_path(url)
        with open(local_path, encoding="utf-8") as f:
            return f.read()

    headers = {"Authorization": f"token {_GITHUB_TOKEN}"} if _GITHUB_TOKEN else {}
    try:
        response = requests.get(url, headers=headers, timeout=_REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        if response.status_code == 403:
            raise RuntimeError(
                f"GitHub API rate limit likely exceeded fetching {url}. "
                "Set a GITHUB_TOKEN environment variable to raise the limit."
            ) from error
        raise RuntimeError(f"Failed to fetch {url}: {error}") from error
    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Network error fetching {url}: {error}") from error

    data = response.json()
    if "content" not in data:
        raise ValueError(f"No 'content' key in GitHub API response for {url}")
    return base64.b64decode(data["content"]).decode("utf-8")


def _iter_functions(source: str):
    """Yield (name, docstring) for every documented function, in source order.

    Pairing each `def` with whatever docstring happens to follow it in the raw
    text silently drops a function whenever the preceding one has no docstring
    of its own: the match runs straight past it and swallows the *next*
    function's docstring instead. Parsing the module means a function only ever
    gets its own docstring, or is skipped for having none.
    """
    def _walk(body):
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                docstring = ast.get_docstring(node, clean=False)
                if docstring:
                    yield node.name, docstring
            elif isinstance(node, ast.ClassDef):
                yield from _walk(node.body)

    yield from _walk(ast.parse(source).body)


def create_markdown_file(file_url: str, header: str, location: str) -> None:
    file_content = _fetch_file(file_url)

    functions_with_docstrings = []
    for function_name, docstring in _iter_functions(file_content):
        # Skip private and dunder methods
        if function_name.startswith("_"):
            continue

        # Description
        desc_m = _RE_DESCRIPTION.match(docstring)
        _INLINE_CONTEXT.update(page=os.path.basename(location), function=function_name)
        description = _clean_description(desc_m.group(1)) if desc_m else ""
        description = _inline_math(description)
        description = _linkify(description)

        # Arguments (also covers Returns / Raises / Notes, which follow Args:)
        args_m = _RE_ARGUMENTS.search(docstring)
        arguments = _linkify(args_m.group(1)) if args_m else ""
        arguments = _escape_pipes(arguments)  # so "int | str" isn't parsed as a table
        arguments = _dedent_block(arguments)
        arguments = _RE_ARG_LABEL.sub(_underline_arg, arguments)
        arguments = "\n".join(
            _RE_MULTI_SPACE.sub(" ", line).strip() for line in arguments.split("\n")
        )
        arguments = _inline_math(arguments)

        # Example code block
        code_m = _RE_CODE.search(docstring)
        example_code = _dedent_block(code_m.group(1)) if code_m else ""

        # Example result
        result_m = _RE_RESULT.search(docstring)
        example_result = _dedent_block(result_m.group(0)) if result_m else ""

        functions_with_docstrings.append({
            "function_name": function_name,
            "description": description,
            "arguments": arguments,
            "example_code": example_code,
            "example_result": example_result,
        })

    # The front matter and introduction are edited on the page itself (SEO titles,
    # descriptions, counts), so an existing page keeps its own; the header here is
    # only the starting point for a new page.
    if os.path.exists(location):
        with open(location, encoding="utf-8") as f:
            existing = f.read()
        # everything before the first function section is the page's own header
        end = existing.find("\n## ")
        if end != -1:
            header = existing[: end + 1]

    markdown_content = header
    for fn in functions_with_docstrings:
        markdown_content += f'## {fn["function_name"]}\n'
        markdown_content += f'{fn["description"]}\n\n'

        if fn["arguments"]:
            arguments = (
                re.sub(
                    r"^([ \t]*)(Args|Raises|Returns|Notes):[ \t]*$",
                    r"\1**\2:**",
                    fn["arguments"],
                    flags=re.MULTILINE,
                ).replace("As an example:", "**As an example:**")
            )
            # Ensure a blank line follows each bolded header so a directly
            # adjacent bullet list (e.g. "**Notes:**\n- ...") renders as a list.
            arguments = re.sub(r"(\*\*[^*]+:\*\*)\n(?!\n)", r"\1\n\n", arguments)
            markdown_content += arguments
            markdown_content += "\n"

        if fn["example_code"]:
            markdown_content += f"\n```python\n{fn['example_code']}\n```\n"

        if fn["example_result"]:
            result_body = fn["example_result"].replace("Which returns:", "").strip()
            markdown_content += f"\nWhich returns:\n\n{result_body}\n"

        markdown_content += "\n---\n\n"

    with open(location, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"✓  {location}  ({len(functions_with_docstrings)} functions)")


# ── Page definitions ──────────────────────────────────────────────────────────
_BASE = "https://api.github.com/repos/JerBouma/FinanceToolkit/contents/financetoolkit"

PAGES = [
    {
        "url": f"{_BASE}/toolkit_controller.py",
        "location": "_pages/financetoolkit/documentation/docs.md",
        "header": f"""---
title: Documentation
excerpt: This the documentation of the FinanceToolkit. This is an open-source toolkit in which 500+ financial methods are written down in the most simplistic way allowing for complete transparency of the calculation method.
description: This the documentation of the FinanceToolkit. This is an open-source toolkit in which 500+ financial methods are written down in the most simplistic way allowing for complete transparency of the calculation method.
author_profile: false
permalink: /projects/financetoolkit/docs
classes: wide-sidebar
layout: single
redirect_from:
    - /docs
sidebar:
    nav: "financetoolkit-docs"
---

These pages document the Finance Toolkit, an open-source toolkit in which all relevant financial methods (500+) are written down in the most simplistic way allowing for complete transparency of the calculation method. Each class has an introduction page like this one, and the sidebar leads to a page for every function that shows how to use it through the [Finance Toolkit MCP](/projects/financetoolkit/mcp) in an AI assistant and in Python. The Python examples are also embedded in the code. For simplicity sake, only the controller modules are included here given that the models themselves should be relatively straightforward. Make sure to also have a look at the [Getting Started](#getting-started) section below and the one that opens every module page.

The Toolkit Module is a collection of functions that collect and parse data, including historical data, fundamental data (balance, income and cash flow statements) and metrics from Financial Modeling Prep such as enterprise values, company profiles and more. From this module you can access all related sub-modules.

{_INSTALL_SNIPPET}

""",
    },
    {
        "url": f"{_BASE}/discovery/discovery_controller.py",
        "location": "_pages/financetoolkit/documentation/discovery.md",
        "header": f"""---
title: Discovery
excerpt: The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, etfs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit.
description: The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, etfs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit.
author_profile: false
permalink: /projects/financetoolkit/docs/discovery
classes: wide-sidebar
layout: single
redirect_from:
    - /discovery
sidebar:
    nav: "financetoolkit-docs-discovery"
---

The Discovery Module contains lists of companies, cryptocurrencies, forex, commodities, ETFs and indices including screeners, quotes, performance metrics and more to find and select tickers to use in the Finance Toolkit.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/ratios/ratios_controller.py",
        "location": "_pages/financetoolkit/documentation/ratios.md",
        "header": f"""---
title: Ratios
excerpt: The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories which are efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.
description: The Ratios Module contains over 50+ ratios that can be used to analyse companies. These ratios are divided into 5 categories which are efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.
author_profile: false
permalink: /projects/financetoolkit/docs/ratios
classes: wide-sidebar
layout: single
redirect_from:
    - /ratios
sidebar:
    nav: "financetoolkit-docs-ratios"
---

The Ratios Module contains 50+ ratios divided into 5 categories: efficiency, liquidity, profitability, solvency and valuation. Each ratio is calculated using the data from the Toolkit module.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/models/models_controller.py",
        "location": "_pages/financetoolkit/documentation/models.md",
        "header": f"""---
title: Models
excerpt: The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.
description: The Models module is meant to execute well-known models such as DUPONT and the Discounted Cash Flow (DCF) model. These models are also directly related to the data retrieved from the Toolkit module.
author_profile: false
permalink: /projects/financetoolkit/docs/models
classes: wide-sidebar
layout: single
redirect_from:
    - /models
sidebar:
    nav: "financetoolkit-docs-models"
---

The Models module executes well-known models such as DuPont analysis and the Discounted Cash Flow (DCF) model, using data retrieved from the Toolkit module.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/options/options_controller.py",
        "location": "_pages/financetoolkit/documentation/options.md",
        "header": f"""---
title: Options
excerpt: The Options module is meant to calculate important options metrics such as the First, Second and Third Order Greeks, the Black Scholes Model and the Option Chains as well as Implied Volatilities, Breeden Litzenberger and more.
description: The Options module is meant to calculate important options metrics such as the First, Second and Third Order Greeks, the Black Scholes Model and the Option Chains as well as Implied Volatilities, Breeden Litzenberger and more.
author_profile: false
permalink: /projects/financetoolkit/docs/options
classes: wide-sidebar
layout: single
redirect_from:
    - /options
sidebar:
    nav: "financetoolkit-docs-options"
---

The Options module calculates important options metrics including First, Second and Third Order Greeks, the Black-Scholes Model, Option Chains, Implied Volatilities, Breeden–Litzenberger and more.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/technicals/technicals_controller.py",
        "location": "_pages/financetoolkit/documentation/technicals.md",
        "header": f"""---
title: Technicals
excerpt: The Technicals Module contains 30+ Technical Indicators that can be used to analyse companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.
description: The Technicals Module contains 30+ Technical Indicators that can be used to analyse companies. These ratios are divided into 4 categories which are breadth, momentum, overlap and volatility. Each indicator is calculated using the data from the Toolkit module.
author_profile: false
permalink: /projects/financetoolkit/docs/technicals
classes: wide-sidebar
layout: single
redirect_from:
    - /technicals
sidebar:
    nav: "financetoolkit-docs-technicals"
---

The Technicals Module contains 30+ technical indicators divided into 4 categories: breadth, momentum, overlap and volatility.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/fixedincome/fixedincome_controller.py",
        "location": "_pages/financetoolkit/documentation/fixedincome.md",
        "header": f"""---
title: Fixed Income
excerpt: The Fixed Income module contains a wide variety of fixed income related calculations such as the Effective Yield, the Macaulay Duration, the Modified Duration Convexity, the Yield to Maturity and models such as Black and Bachelier to valuate derivative instruments such as Swaptions.
description: The Fixed Income module contains a wide variety of fixed income related calculations such as the Effective Yield, the Macaulay Duration, the Modified Duration Convexity, the Yield to Maturity and models such as Black and Bachelier to valuate derivative instruments such as Swaptions.
author_profile: false
permalink: /projects/financetoolkit/docs/fixedincome
classes: wide-sidebar
layout: single
redirect_from:
    - /fixedincome
sidebar:
    nav: "financetoolkit-docs-fixedincome"
---

The Fixed Income module covers a wide variety of calculations including the Effective Yield, Macaulay Duration, Modified Duration, Convexity, Yield to Maturity and derivative pricing models such as Black and Bachelier (used for Swaptions and other instruments).

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/risk/risk_controller.py",
        "location": "_pages/financetoolkit/documentation/risk.md",
        "header": f"""---
title: Risk
excerpt: The Risk module is meant to calculate important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (cVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.
description: The Risk module is meant to calculate important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (cVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.
author_profile: false
permalink: /projects/financetoolkit/docs/risk
classes: wide-sidebar
layout: single
redirect_from:
    - /risk
sidebar:
    nav: "financetoolkit-docs-risk"
---

The Risk module calculates important risk metrics such as Value at Risk (VaR), Conditional Value at Risk (CVaR), Maximum Drawdown, Correlations, GARCH, EWMA and more.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/performance/performance_controller.py",
        "location": "_pages/financetoolkit/documentation/performance.md",
        "header": f"""---
title: Performance
excerpt: The Performance module is meant to calculate important performance metrics such as Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model, R-Squared and more.
description: The Performance module is meant to calculate important performance metrics such as Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model, R-Squared and more.
author_profile: false
permalink: /projects/financetoolkit/docs/performance
classes: wide-sidebar
layout: single
redirect_from:
    - /performance
sidebar:
    nav: "financetoolkit-docs-performance"
---

The Performance module calculates important performance metrics such as the Sharpe Ratio, Sortino Ratio, Treynor Ratio, Information Ratio, Jensen's Alpha, Beta, Capital Asset Pricing Model (CAPM), R-Squared and more.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/econometrics/econometrics_controller.py",
        "location": "_pages/financetoolkit/documentation/econometrics.md",
        "header": f"""---
title: Econometrics
excerpt: The Econometrics module contains statistical tests and estimators for financial time series and panel data, including unit root and cointegration tests, regression estimators, causal inference methods, diagnostics, forecasting and event studies.
description: The Econometrics module contains statistical tests and estimators for financial time series and panel data, including unit root and cointegration tests, regression estimators, causal inference methods, diagnostics, forecasting and event studies.
author_profile: false
permalink: /projects/financetoolkit/docs/econometrics
classes: wide-sidebar
layout: single
redirect_from:
    - /econometrics
sidebar:
    nav: "financetoolkit-docs-econometrics"
---

The Econometrics module contains statistical tests and estimators for financial time series and panel data. It covers unit root and cointegration tests, regression estimators (OLS, WLS, GLS, quantile, logit, probit, Fama-MacBeth), causal inference methods (instrumental variables, difference-in-differences, regression discontinuity, propensity score matching, synthetic control), panel data estimators, specification and diagnostic tests, time series forecasting (ARIMA, VAR, VECM) and event studies.

Use it in Claude, ChatGPT or another AI assistant through the [Finance Toolkit MCP](/projects/financetoolkit/mcp), or in Python. Unlike the other modules, this one depends on `statsmodels` and `linearmodels`. These are bundled in the optional `econometrics` extra, so install the Finance Toolkit with:

```python
pip install "financetoolkit[econometrics]" -U
```

{{% include algolia.html %}}

""",
    },
    {
        "url": f"{_BASE}/economics/economics_controller.py",
        "location": "_pages/financetoolkit/documentation/economics.md",
        "header": f"""---
title: Economics
excerpt: The Economics module gives insights for 60+ countries into key economic indicators such as the Consumer Price Index (CPI), Gross Domestic Product (GDP), Unemployment Rates and 3-month and 10-year Government Interest Rates. This is done through the economics module and can be used as a standalone module as well.
description: The Economics module gives insights for 60+ countries into key economic indicators such as the Consumer Price Index (CPI), Gross Domestic Product (GDP), Unemployment Rates and 3-month and 10-year Government Interest Rates. This is done through the economics module and can be used as a standalone module as well.
author_profile: false
permalink: /projects/financetoolkit/docs/economics
classes: wide-sidebar
layout: single
redirect_from:
    - /economics
sidebar:
    nav: "financetoolkit-docs-economics"
---

The Economics module provides insights for 60+ countries into key economic indicators such as the Consumer Price Index (CPI), Gross Domestic Product (GDP), Unemployment Rates and government interest rates. It can also be used as a standalone module.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/etf/etf_controller.py",
        "location": "_pages/financetoolkit/documentation/etf.md",
        "header": f"""---
title: ETF
seo_title: "ETF Analysis in Python | Finance Toolkit"
seo_title_suffix: false
excerpt: The ETF module analyzes exchange-traded funds, from their holdings, sector and country weightings to their tracking, concentration, overlap, valuation and liquidity.
description: The ETF module analyzes exchange-traded funds, from their holdings, sector and country weightings to their tracking, concentration, overlap, valuation and liquidity.
author_profile: false
permalink: /projects/financetoolkit/docs/etf
classes: wide-sidebar
layout: single
sidebar:
    nav: "financetoolkit-docs-etf"
---

The ETF module analyzes exchange-traded funds: their holdings, sector and country weightings, tracking against what they follow, concentration, the overlap between funds, valuation and liquidity.

{_INSTALL_SNIPPET}{{% include financetoolkit-getting-started/etf.md %}}

""",
    },
    {
        "url": f"{_BASE}/portfolio/construction_controller.py",
        "location": "_pages/financetoolkit/documentation/portfolio-optimization.md",
        "header": f"""---
title: Portfolio Optimization
seo_title: "Portfolio Optimization in Python | Finance Toolkit"
seo_title_suffix: false
excerpt: The Portfolio Optimization module builds portfolios from the tickers of a Toolkit, from minimum variance, maximum Sharpe ratio and risk parity weights to the efficient frontier, risk contributions, stress tests and attribution.
description: The Portfolio Optimization module builds portfolios from the tickers of a Toolkit, from minimum variance, maximum Sharpe ratio and risk parity weights to the efficient frontier, risk contributions, stress tests and attribution.
author_profile: false
permalink: /projects/financetoolkit/docs/portfolio-optimization
classes: wide-sidebar
layout: single
sidebar:
    nav: "financetoolkit-docs-portfolio-optimization"
---

The Portfolio Optimization module builds portfolios from the tickers of a Toolkit: minimum variance, maximum Sharpe ratio, mean-variance, risk parity, Hierarchical Risk Parity, minimum CVaR and Black-Litterman weights, the efficient frontier, risk contributions, stress tests and attribution.

{_INSTALL_SNIPPET}""",
    },
    {
        "url": f"{_BASE}/portfolio/portfolio_controller.py",
        "location": "_pages/financetoolkit/documentation/portfolio.md",
        "header": f"""---
title: Portfolio
excerpt: The Portfolio module is meant to calculate important portfolio metrics allows you to compare your own portfolio to a benchmark, seeing performance of individual assets and directly load the portfolio into the Finance Toolkit.
description: The Portfolio module is meant to calculate important portfolio metrics allows you to compare your own portfolio to a benchmark, seeing performance of individual assets and directly load the portfolio into the Finance Toolkit.
author_profile: false
permalink: /projects/financetoolkit/docs/portfolio
classes: wide-sidebar
layout: single
redirect_from:
    - /portfolio
sidebar:
    nav: "financetoolkit-docs-portfolio"
---

The Portfolio module calculates important portfolio metrics, allowing you to compare your portfolio against a benchmark, analyse individual asset performance and load your portfolio directly into the Finance Toolkit.

{_INSTALL_SNIPPET_PYTHON}""",
    },
]

# ── Generate all pages ────────────────────────────────────────────────────────
if __name__ == "__main__":
    if _LOCAL_PATH:
        print(f"Local mode: reading controllers from {_LOCAL_PATH}\n")
    for page in PAGES:
        create_markdown_file(page["url"], page["header"], page["location"])
    # DOCS_INLINE_MATH_LOG=<file> lists every inline formula, to review the conversion
    if os.environ.get("DOCS_INLINE_MATH_LOG"):
        with open(os.environ["DOCS_INLINE_MATH_LOG"], "w", encoding="utf-8") as f:
            for entry in _INLINE_LOG:
                f.write(f"{entry['page']}\t{entry['function']}\t{entry['text']}\t{entry['latex']}\n")
