require "cgi"
require "json"

# Structures the Finance Toolkit documentation as one introduction page per
# class plus one page per function.
#
# assets/python/docs.py writes a Markdown page per class (Toolkit, Discovery,
# Ratios, Models, ...) with every function of that class on it. At build time
# this plugin turns each of those into:
#
# - a class page (/projects/financetoolkit/docs/ratios): the intro, the install
#   instructions and a "Getting Started" section that shows how to reach the
#   class, taken from the matching section on the Toolkit page (or, for
#   Toolkit, Discovery and Portfolio, from how their first example creates the
#   class);
# - a page per function (/projects/financetoolkit/docs/ratios/current-ratio)
#   with its description, formula, Python example, parameters and related
#   functions.
#
# The sidebar is how readers move between them: every sidebar entry that
# pointed at a function on a class page now points at the function's page, and
# the "Ratios Module" style entries on the Toolkit page point at the class
# pages. Links in page content are rewritten the same way, and old anchor links
# (the FinanceToolkit README uses them) are forwarded by a small script.
#
# The collect_ functions (collect_profitability_ratios, collect_all_greeks,
# ...) only gather the get_ functions of a module, so the docs leave them out:
# no page, no section on the module page and no sidebar entry. Links to them
# point at the module page and the pages they used to have redirect there. Portfolio's collect_historical_data
# and collect_benchmark_historical_data load data and keep their pages.
#
# Nothing is duplicated in the repository: the pages are cut from docs.py's
# output on every build. Names and grouping come from the docs sidebars in
# _data/navigation.yml; a function without a sidebar entry gets no page and
# stays on its class page.
module DocsMetricPages
  DOCS_ROOT = "/projects/financetoolkit/docs".freeze

  # key => display name, page url and sidebar; function pages live under url
  CLASSES = {
    "toolkit"      => { :name => "Toolkit",      :url => DOCS_ROOT,                     :nav => "financetoolkit-docs" },
    "discovery"    => { :name => "Discovery",    :url => "#{DOCS_ROOT}/discovery",      :nav => "financetoolkit-docs-discovery" },
    "ratios"       => { :name => "Ratios",       :url => "#{DOCS_ROOT}/ratios",         :nav => "financetoolkit-docs-ratios" },
    "models"       => { :name => "Models",       :url => "#{DOCS_ROOT}/models",         :nav => "financetoolkit-docs-models" },
    "options"      => { :name => "Options",      :url => "#{DOCS_ROOT}/options",        :nav => "financetoolkit-docs-options" },
    "technicals"   => { :name => "Technicals",   :url => "#{DOCS_ROOT}/technicals",     :nav => "financetoolkit-docs-technicals" },
    "fixedincome"  => { :name => "Fixed Income", :url => "#{DOCS_ROOT}/fixedincome",    :nav => "financetoolkit-docs-fixedincome" },
    "risk"         => { :name => "Risk",         :url => "#{DOCS_ROOT}/risk",           :nav => "financetoolkit-docs-risk" },
    "performance"  => { :name => "Performance",  :url => "#{DOCS_ROOT}/performance",    :nav => "financetoolkit-docs-performance" },
    "econometrics" => { :name => "Econometrics", :url => "#{DOCS_ROOT}/econometrics",   :nav => "financetoolkit-docs-econometrics" },
    "economics"    => { :name => "Economics",    :url => "#{DOCS_ROOT}/economics",      :nav => "financetoolkit-docs-economics" },
    "portfolio"    => { :name => "Portfolio",    :url => "#{DOCS_ROOT}/portfolio",      :nav => "financetoolkit-docs-portfolio" },
  }.freeze

  # classes whose functions fetch data rather than calculate metrics
  DATA_CLASSES = %w[toolkit discovery portfolio].freeze

  # classes created directly rather than reached through a Toolkit instance;
  # their Getting Started example is how their first example creates them
  CONSTRUCTORS = { "toolkit" => "Toolkit", "discovery" => "Discovery", "portfolio" => "Portfolio" }.freeze

  SECTION = /^## (\w+)\n(.*?)(?=^## |\z)/m

  # generated page paths, "page_url#anchor" => new url, and the sidebar urls of
  # the collect_ functions that link to their module instead
  GENERATED = []
  URL_MAP = {}
  RETIRED = []

  class Page < Jekyll::PageWithoutAFile; end

  module_function

  # collect_ functions of the calculating modules, which link to their module
  def collector?(key, anchor)
    anchor.start_with?("collect_") && !DATA_CLASSES.include?(key)
  end

  def slugify(text)
    Jekyll::Utils.slugify(text.to_s.gsub("&", " and "), :mode => "default")
  end

  # anchor => { title:, group: } for every function the class sidebar lists,
  # plus group => [anchors] in sidebar order and anchor => title for the
  # collect_ functions
  def sidebar(site, key)
    cls = CLASSES[key]
    entries = Array(site.data.dig("navigation", cls[:nav]))
    functions = {}
    collectors = {}
    groups = Hash.new { |h, k| h[k] = [] }
    walk = lambda do |items, group|
      items.each do |item|
        url = item["url"].to_s
        if url.start_with?("#{cls[:url]}#")
          anchor = url.split("#", 2).last.downcase
          # on the Toolkit page "#ratios" etc. are class sections, not functions
          if collector?(key, anchor)
            collectors[anchor] ||= item["title"].to_s.strip
          elsif !(anchor == "site-nav" || (key == "toolkit" && CLASSES.key?(anchor)) || functions.key?(anchor))
            functions[anchor] = { :title => item["title"].to_s.strip, :group => group }
            groups[group] << anchor
          end
        end
        walk.call(Array(item["children"]), item["title"].to_s.strip) if item["children"]
      end
    end
    walk.call(entries, cls[:name])
    [functions, groups, collectors]
  end

  # split a function section into its parts
  def parse(body)
    body = body.sub(/\n---\s*\z/, "").strip
    code_at   = body.index("```python")
    args_at   = body.index("**Args:**") || body.index("**Returns:**")
    desc_end  = [args_at, code_at, body.length].compact.min
    desc      = body[0...desc_end].strip
    args      = args_at ? body[args_at...(code_at || body.length)].sub(/\*\*As an example:\*\*\s*\z/, "").strip : ""
    example   = code_at ? body[code_at..].strip : ""
    { :description => desc, :arguments => args, :example => example }
  end

  def plain(markdown)
    markdown.gsub(/\$\$.*?\$\$/m, " ")
            .gsub(/\[([^\]]+)\]\([^)]+\)(\{:[^}]*\})?/, '\1')
            .gsub(/[*_`]/, "")
            .gsub(/\s+/, " ").strip
  end

  # First paragraph of the docstring, topped up with the next paragraphs when
  # it is a one-liner ("Calculate the Ljung-Box test for autocorrelation."),
  # and with a line about the page itself when even that stays short.
  def description_for(desc)
    paragraphs = desc.split(/\n\s*\n/)
                     .reject { |p| p.lstrip.start_with?("- ", "$$", "|") }
                     .map { |p| plain(p) }
                     .reject { |p| p.empty? || (p.end_with?(":") && p.length < 40) }
    # a sentence that only introduces a list ("It contains the following
    # columns:") means nothing once the list is left out
    paragraphs = paragraphs.map do |p|
      next p unless p.end_with?(":")
      lead = p.sub(/(?<=[.!?])\s+[^.!?]*:\z/, "")
      lead == p ? p : lead
    end
    text = paragraphs.shift.to_s
    text = "#{text} #{paragraphs.shift}" while text.length < 110 && !paragraphs.empty?
    text = "#{text} Parameters and a Python example with the Finance Toolkit." if text.length < 110
    text = text.sub(/:\z/, ".")
    return text if text.length <= 158
    cut = text[0, 155]
    cut = cut[0, cut.rindex(" ") || cut.length].sub(/[,;:]\z/, "")
    "#{cut}..."
  end

  # The theme runs <title> through markdownify, where a bare "|" turns the
  # title into a table, so the separator is written as an entity (as the
  # theme's own title_separator is); lengths are measured with a plain "|".
  # "Altman Z-Score | Finance Toolkit". When that runs past 65 characters the
  # bracketed acronym goes first ("Forward Price to Earnings Growth Ratio
  # (Forward PEG)" loses "(Forward PEG)"), and only then the suffix.
  def seo_title_for(name)
    short = name.sub(/\s*\([^()]*\)\s*\z/, "")
    title = ["#{name} | Finance Toolkit", "#{short} | Finance Toolkit", short]
              .find { |t| t.length <= 65 } || short
    title.sub(" | ", " &#124; ")
  end

  # just the argument bullets from the Args block, without Returns/Raises/Notes
  def arguments_for(block)
    args = block[/\*\*Args:\*\*\s*(.*?)(?=\*\*(?:Returns|Raises|Notes|As an example):\*\*|\z)/m, 1].to_s.strip
    args.start_with?("- ") ? args : ""
  end

  def related_heading(key, group)
    name = CLASSES[key][:name]
    return "Related #{group}" unless group == name || group == "Finance Toolkit"
    return "Related Models" if key == "models"
    DATA_CLASSES.include?(key) ? "Related #{name} Functions" : "Related #{name} Metrics"
  end

  def content_for(name, key, fn_name, parts, related)
    cls = CLASSES[key]
    out = +""
    out << parts[:description] << "\n\n"
    unless parts[:example].empty?
      out << "## #{name} in Python\n\n"
      out << "`#{fn_name}` is part of the [#{cls[:name]} module](#{cls[:url]}) of the open-source "
      out << "[Finance Toolkit](/projects/financetoolkit). Install it with:\n{: .docs-boilerplate}\n\n"
      out << "```python\npip install financetoolkit -U\n```\n\n"
      out << "Then call `#{fn_name}` as shown below.\n{: .docs-boilerplate}\n\n"
      out << parts[:example] << "\n\n"
    end
    arguments = arguments_for(parts[:arguments])
    unless arguments.empty?
      out << "## Parameters\n\n"
      out << "`#{fn_name}` accepts the following parameters:\n{: .docs-boilerplate}\n\n"
      out << arguments << "\n\n"
    end
    unless related.empty?
      # same pill buttons as the module switcher on the docs pages
      pills = related.map do |r|
        %(<a href="#{r[:url]}" class="ft-module-pill">#{CGI.escapeHTML(r[:title])}</a>)
      end
      out << "## #{related_heading(key, related.first[:group])}\n\n"
      out << %(<div class="ft-module-switcher docs-related">\n  #{pills.join("\n  ")}\n</div>\n\n)
    end
    out
  end

  # The docs sidebar is how readers move through the documentation, so it says
  # so: a line at its top on wide screens, and "Documentation menu" instead of
  # "Toggle menu" on the button that opens it on phones.
  def sidebar_data(nav, hint)
    { "nav" => nav, "hint" => hint, "menu_label" => "Documentation menu" }
  end

  # A quiet line pointing at the sidebar, used under the class intro and at the
  # end of Getting Started. On phones, where the sidebar is folded behind the
  # "Documentation menu" button, it links to that menu instead.
  OPEN_MENU = %(<label for="ac-toc" class="docs-browse-hint__open" onclick="setTimeout(function(){var s=document.querySelector('.sidebar');if(s)s.scrollIntoView({behavior:'smooth'});},50)">documentation menu</label>).freeze

  def browse_hint(sentence, wide_action, narrow_action)
    <<~HTML.gsub("\n", "")
      <p class="docs-browse-hint">
      <span class="docs-browse-hint__wide">#{sentence} #{wide_action}</span>
      <span class="docs-browse-hint__narrow">#{sentence} #{narrow_action.sub('%menu%', OPEN_MENU)}</span>
      </p>
    HTML
  end

  def intro_hint(key)
    browse_hint("Every function of the #{CLASSES[key][:name]} module has its own page with an example and its parameters.",
                "Pick one from the sidebar on the left.", "Pick one from the %menu%.")
  end

  # closes Getting Started: the sidebar is the way to every metric (or, for the
  # data classes, every function) of the class
  def getting_started_hint(key)
    kind = DATA_CLASSES.include?(key) ? "function" : "metric"
    browse_hint("The sidebar gives access to every #{kind} in the #{CLASSES[key][:name]} module, each on its own page with a description, an example and its parameters.",
                "Pick one there to open it.", "On a phone, open the %menu% to pick one.")
  end

  # up to twelve functions from the same sidebar group, nearest to this one in
  # the sidebar order first, so neighbouring functions link to each other
  def related_for(anchor, group_anchors, urls, limit = 12)
    list = group_anchors.select { |a| urls[a] }
    index = list.index(anchor) || 0
    (list - [anchor]).sort_by { |a| [(list.index(a) - index).abs, list.index(a)] }
                     .first(limit)
                     .sort_by { |a| list.index(a) }
  end

  # the docstring's "Also known as: PE ratio, P/E ratio, ..." names, used as
  # alternate names in the structured data
  def also_known_as(desc)
    line = desc[/\*\*Also known as:\*\*\s*(.+)/, 1].to_s
    line.sub(/\.\s*\z/, "").split(/,\s*/).map(&:strip).reject(&:empty?)
  end

  def unique_description(name, text, seen)
    unless seen.include?(text)
      seen << text
      return text
    end
    text = "#{name}: #{text}"
    text = "#{text[0, 155][0, text[0, 155].rindex(' ') || 155]}..." if text.length > 158
    seen << text
    text
  end

  # Getting Started for classes reached through the Toolkit: the matching
  # section on the Toolkit page, minus its first paragraph (the class page
  # already opens with the same introduction) and its "see this link" line
  # (which points at the class page itself).
  def getting_started_from_toolkit(key, body)
    parts = parse(body)
    paragraphs = parts[:description].split(/\n\s*\n/).map(&:strip)
    paragraphs.shift
    paragraphs.reject! { |p| p.start_with?("See the following link") }
    name = CLASSES[key][:name]
    standalone = paragraphs.any? { |p| p.include?("from financetoolkit import") }
    lead = if parts[:example].include?("Toolkit(") && standalone
             "The example below uses it through a `Toolkit` instance instead."
           elsif parts[:example].include?("Toolkit(")
             "The #{name} module is reached through a `Toolkit` instance, as shown below."
           elsif standalone
             # the paragraphs already explain the standalone import
             "For example:"
           else
             "The #{name} module can also be used on its own, as shown below."
           end
    out = +"## Getting Started\n\n"
    out << paragraphs.join("\n\n") << "\n\n" unless paragraphs.empty?
    out << lead << "\n\n"
    out << parts[:example] << "\n" unless parts[:example].empty?
    out
  end

  # Getting Started on the main docs page: a short tour taken from the Finance
  # Toolkit README, since initialising alone says little about what it does.
  TOOLKIT_GETTING_STARTED = <<~MD.freeze
    ## Getting Started

    Create a `Toolkit` instance with the tickers you want to analyse and your Financial Modeling Prep API key. Everything else hangs off this one instance: the data functions on this page, and every module as an attribute, such as `companies.ratios`.

    ```python
    from financetoolkit import Toolkit

    companies = Toolkit(
        ["AAPL", "MSFT"],
        api_key="FINANCIAL_MODELING_PREP_KEY",
        start_date="2017-12-31",
    )
    ```

    The data functions return the underlying data for all tickers at once. For example, the historical market data, selected here for Apple:

    ```python
    historical_data = companies.get_historical_data()

    historical_data.xs("AAPL", axis=1, level=1)
    ```

    | date       |    Open |    High |     Low |   Close |   Adj Close |      Volume |   Dividends |   Return |   Cumulative Return |
    |:-----------|--------:|--------:|--------:|--------:|------------:|------------:|------------:|---------:|--------------------:|
    | 2018-01-02 | 42.54   | 43.075  | 42.315  | 43.065  |       40.78 | 1.02224e+08 |           0 |   0      |              1      |
    | 2018-01-03 | 43.1325 | 43.6375 | 42.99   | 43.0575 |       40.77 | 1.17982e+08 |           0 |  -0.0002 |              0.9998 |
    | 2018-01-04 | 43.135  | 43.3675 | 43.02   | 43.2575 |       40.96 | 8.97384e+07 |           0 |   0.0047 |              1.0044 |
    | 2018-01-05 | 43.36   | 43.8425 | 43.2625 | 43.75   |       41.43 | 9.46401e+07 |           0 |   0.0115 |              1.0159 |
    | 2018-01-08 | 43.5875 | 43.9025 | 43.4825 | 43.5875 |       41.27 | 8.22711e+07 |           0 |  -0.0039 |              1.012  |

    The modules calculate on top of that data. Every metric has its own `get_` function, and a whole category can be calculated at once. For example, all profitability ratios, selected here for Microsoft:

    ```python
    profitability_ratios = companies.ratios.collect_profitability_ratios()

    profitability_ratios.loc["MSFT"]
    ```

    |                                 |    2017 |    2018 |    2019 |    2020 |    2021 |    2022 |    2023 |
    |:--------------------------------|--------:|--------:|--------:|--------:|--------:|--------:|--------:|
    | Gross Margin                    |  0.6191 |  0.6525 |  0.659  |  0.6778 |  0.6893 |  0.684  |  0.6892 |
    | Operating Margin                |  0.2482 |  0.3177 |  0.3414 |  0.3703 |  0.4159 |  0.4206 |  0.4177 |
    | Net Profit Margin               |  0.2357 |  0.1502 |  0.3118 |  0.3096 |  0.3645 |  0.3669 |  0.3415 |
    | Interest Coverage Ratio         | 13.9982 | 16.5821 | 20.3429 | 25.3782 | 34.7835 | 47.4275 | 52.0244 |
    | Income Before Tax Profit Margin |  0.2574 |  0.3305 |  0.3472 |  0.3708 |  0.423  |  0.4222 |  0.4214 |

    The same instance gives access to every other module:

    ```python
    # Extended DuPont Analysis
    companies.models.get_extended_dupont_analysis()

    # Weekly Value at Risk
    companies.risk.get_value_at_risk(period="weekly")

    # Ichimoku Cloud
    companies.technicals.get_ichimoku_cloud()

    # Correlations with the Fama-French factors, per quarter
    companies.performance.get_factor_asset_correlations(period="quarterly")
    ```

    A few options work across nearly every function:

    - **`growth` and `lag`:** `growth=True` returns the period-over-period growth instead of the value, and `lag` sets how many periods back it is measured against (e.g. `lag=4` for year-over-year growth on quarterly data).
    - **`rolling` and `trailing`:** compute a metric over a sliding window, or as a trailing sum or average (e.g. `trailing=4` for trailing twelve months on quarterly data).
    - **`standardize`:** `standardize=True` turns values into Z-scores against their own history, which makes metrics on different scales comparable.
  MD

  # Getting Started for classes created directly: the import and constructor
  # lines of the first example on the page.
  def getting_started_from_constructor(key, sections)
    klass = CONSTRUCTORS[key]
    code = sections.values.map { |_, body| parse(body)[:example][/```python\n(.*?)```/m, 1] }.compact
                   .find { |c| c.include?("#{klass}(") }
    return "" unless code
    lines = []
    depth = 0
    started = false
    code.each_line do |line|
      lines << line
      started ||= line.include?("#{klass}(")
      depth += line.count("(") - line.count(")") if started
      break if started && depth <= 0
    end
    lead = case key
           when "toolkit" then "Create a `Toolkit` instance with the tickers you want to analyse and your Financial Modeling Prep API key. Every module is then available as an attribute of that instance, for example `toolkit.ratios`, and the Toolkit's own functions retrieve the underlying data."
           else "Import the `#{klass}` class and create an instance as shown below."
           end
    "## Getting Started\n\n#{lead}\n\n```python\n#{lines.join.rstrip}\n```\n"
  end

  def generate(site)
    seen_descriptions = []
    built = []
    pages = site.pages.each_with_object({}) { |page, map| map[page.url] = page if page.url.start_with?(DOCS_ROOT) }
    toolkit_page = pages[DOCS_ROOT]
    toolkit_sections = toolkit_page ? toolkit_page.content.scan(SECTION).to_h { |fn, body| [fn.downcase, body] } : {}

    CLASSES.each do |key, cls|
      class_page = pages[cls[:url]]
      next unless class_page

      functions, groups, collectors = sidebar(site, key)
      # sidebar anchors are lowercase (kramdown's heading ids), a few function
      # names are not (get_EBT_to_EBIT), so sections are keyed by the lowercase
      # name and keep the real one for the code sample
      sections = class_page.content.scan(SECTION).to_h { |fn, body| [fn.downcase, [fn, body]] }

      urls = {}
      used = CLASSES.keys.to_h { |k| [k, true] } # toolkit pages share /docs/ with the classes
      functions.each do |anchor, info|
        next unless sections.key?(anchor)
        slug = slugify(info[:title])
        slug = "#{slug}-#{slugify(anchor.delete_prefix('get_'))}" if used[slug]
        used[slug] = true
        urls[anchor] = "#{cls[:url]}/#{slug}"
      end

      urls.each do |anchor, url|
        info    = functions[anchor]
        fn_name, body = sections[anchor]
        parts   = parse(body)
        # a function alone in its sidebar group falls back to its neighbours in
        # the whole class, so every page links onwards
        pool    = groups[info[:group]].count { |a| urls[a] } > 1 ? groups[info[:group]] : functions.keys
        group   = pool.equal?(groups[info[:group]]) ? info[:group] : cls[:name]
        related = related_for(anchor, pool, urls).map { |a| { :title => functions[a][:title], :url => urls[a], :group => group } }

        description = unique_description(info[:title], description_for(parts[:description]), seen_descriptions)
        page = Page.new(site, site.source, url.delete_prefix("/").sub(%r{/[^/]+\z}, ""), "#{url.split('/').last}.md")
        page.content = content_for(info[:title], key, fn_name, parts, related)
        page.data.merge!(
          "layout"               => "single",
          "title"                => info[:title],
          "seo_title"            => seo_title_for(info[:title]),
          "seo_title_suffix"     => false,
          "description"          => description,
          "excerpt"              => description,
          "permalink"            => url,
          "classes"              => "wide-sidebar",
          "author_profile"       => false,
          "sidebar"              => sidebar_data(cls[:nav], "Every function has its own page with an example and its parameters. Pick one below."),
          "redirect_from"        => ["#{url}/"],
          "docs_module"          => cls[:name],
          "docs_module_url"      => cls[:url],
          "docs_function"        => fn_name,
          "docs_aka"             => also_known_as(parts[:description]),
          "image"                => "/assets/images/projects/FinanceToolkit.jpg",
          "share"                => true,
          "last_modified_at"     => class_page.data["last_modified_at"],
          "last_modified_at_from_git" => class_page.data["last_modified_at_from_git"]
        )
        site.pages << page
        GENERATED << page.relative_path
        built << [page, key, info[:title]]
      end

      # The class page keeps what comes before its first function (intro,
      # install, search) and gains a Getting Started section. Functions with a
      # page of their own, and on the Toolkit page the per-class sections that
      # move to the class pages, are removed.
      intro, first_heading, rest = class_page.content.partition(/^## \w+\n/)
      remaining = (first_heading + rest).gsub(SECTION) do
        name = Regexp.last_match(1).downcase
        urls[name] || collector?(key, name) || (key == "toolkit" && CLASSES.key?(name)) ? "" : Regexp.last_match(0)
      end
      started = if toolkit_sections.key?(key) then getting_started_from_toolkit(key, toolkit_sections[key])
                elsif key == "toolkit" then TOOLKIT_GETTING_STARTED.dup
                elsif CONSTRUCTORS.key?(key) then getting_started_from_constructor(key, sections)
                else ""
                end

      forward = urls.dup
      if key == "toolkit"
        CLASSES.each { |k, c| forward[k] = c[:url] if toolkit_sections.key?(k) }
      end
      started = started.rstrip + "\n\n" + getting_started_hint(key) + "\n" unless started.empty?
      # the hint goes under the intro text, just before the install instructions
      hint = intro_hint(key) + "\n\n"
      install = intro.index(/^(To install the FinanceToolkit|Unlike the other modules)/)
      intro = if install then intro.dup.insert(install, hint)
              else
                paragraphs = intro.strip.split(/\n\s*\n/, 2)
                ([paragraphs.first, hint.strip] + paragraphs.drop(1)).join("\n\n")
              end
      class_page.data["sidebar"] = sidebar_data(cls[:nav], "Every function has its own page with an example and its parameters. Pick one below.")
      class_page.content = intro.rstrip + "\n\n" + started + "\n" + remaining + <<~HTML

        <script>
          (function () {
            var pages = #{JSON.generate(forward)};
            var target = pages[decodeURIComponent(location.hash.slice(1)).toLowerCase()];
            if (target) location.replace(target);
          })();
        </script>
      HTML
      forward.each { |anchor, url| URL_MAP["#{cls[:url]}##{anchor}"] = url }

      # collect_ functions: links go to the module page, their old pages
      # (/docs/ratios/all-profitability-ratios) redirect there
      collectors.each do |anchor, title|
        URL_MAP["#{cls[:url]}##{anchor}"] = cls[:url]
        RETIRED << "#{cls[:url]}##{anchor}"
        old = "#{cls[:url]}/#{slugify(title)}"
        class_page.data["redirect_from"] = Array(class_page.data["redirect_from"]) | [old, "#{old}/"]
      end
    end

    distinct_titles(built)
    rewrite_navigation(site)
  end

  # A few names exist in two classes (Historical Data in Toolkit and
  # Portfolio, Press Releases in Toolkit and Discovery). The Toolkit version
  # keeps the plain title, the others get their class in brackets so every
  # page has its own title in search results.
  def distinct_titles(built)
    built.group_by { |page, _, _| page.data["seo_title"] }.each_value do |same|
      next if same.size < 2
      keep = same.find { |_, key, _| key == "toolkit" } || same.first
      (same - [keep]).each do |page, key, title|
        page.data["seo_title"] = seo_title_for("#{title} (#{CLASSES[key][:name]})")
      end
    end
  end

  # every sidebar entry that pointed at a function (or, on the Toolkit page, a
  # class section) now points at its own page; collect_ entries are dropped,
  # or become a plain heading when they have children (First-Order Greeks)
  def rewrite_navigation(site)
    walk = lambda do |items|
      return unless items.is_a?(Array)
      items.reject! do |item|
        next false unless item.is_a?(Hash)
        url = item["url"].to_s.sub(/#(.*)\z/) { "##{Regexp.last_match(1).downcase}" }
        if RETIRED.include?(url)
          next true unless item["children"]
          item.delete("url")
        elsif (mapped = URL_MAP[url])
          item["url"] = mapped
        end
        walk.call(item["children"]) if item["children"]
        false
      end
    end
    Array(site.data["navigation"]&.values).each { |nav| walk.call(nav) }
  end

  # links in page content that still point at an anchor on a class page
  # (/projects/financetoolkit/docs/performance#get_sharpe_ratio) go straight
  # to the new page
  LINK = %r{href="((?:https?://(?:www\.)?jeroenbouma\.com)?(/projects/financetoolkit/docs(?:/[a-z]+)?)#(\w+))"}i

  def rewrite_links(doc)
    return if URL_MAP.empty? || doc.output_ext != ".html" || doc.output.nil?
    doc.output = doc.output.gsub(LINK) do
      target = URL_MAP["#{Regexp.last_match(2)}##{Regexp.last_match(3).downcase}"]
      target ? %(href="#{target}") : Regexp.last_match(0)
    end
  end

  class Generator < Jekyll::Generator
    safe true
    # before jekyll-redirect-from (normal) and jekyll-sitemap (lowest), so the
    # trailing-slash redirects and the sitemap entries include these pages
    priority :high

    def generate(site)
      GENERATED.clear
      URL_MAP.clear
      RETIRED.clear
      DocsMetricPages.generate(site)
    end
  end
end

Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  DocsMetricPages.rewrite_links(doc)
end

# Search: the function pages hold the full text now that the class pages are
# introductions, so they are indexed. Paragraphs that repeat on every page (the
# install and parameter lead-ins) are skipped so they do not flood the results.
# (This site defines no other Algolia hooks; move them here if that changes.)
if defined?(Jekyll::Algolia::Hooks)
  module Jekyll
    module Algolia
      module Hooks
        SKIPPED_CLASSES = %w[docs-boilerplate docs-mcp-note].freeze

        def self.before_indexing_each(record, node, _context)
          classes = node.respond_to?(:[]) ? node["class"].to_s.split : []
          return nil if (classes & SKIPPED_CLASSES).any?
          record
        end
      end
    end
  end
end
