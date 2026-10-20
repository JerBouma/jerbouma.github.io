"""
Download Jupyter Notebooks from GitHub and store them locally for
client-side rendering on the Jekyll site.

Run with:  python assets/python/notebooks.py
"""

import os
import ssl
import urllib.request
import urllib.error


def _make_ssl_context():
    """Create an SSL context, using certifi if available."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx


_SSL_CTX = _make_ssl_context()

# ── Notebook definitions ──────────────────────────────────────────────────────
# Each entry: (raw GitHub URL, local destination path)


NOTEBOOKS = [
    # ── Finance Database ──────────────────────────────────────
    (
        "https://raw.githubusercontent.com/JerBouma/FinanceDatabase/main/examples/FInance%20Database%20-%201.%20Getting%20Started.ipynb",
        "assets/notebooks/financedatabase/getting-started.ipynb",
    ),
    # ── Personal Finance ──────────────────────────────────────
    (
        "https://raw.githubusercontent.com/JerBouma/PersonalFinance/refs/heads/main/examples/Personal%20Finance%20-%202.%20Using%20Your%20Files.ipynb",
        "assets/notebooks/personalfinance/using-your-files.ipynb",
    ),

]


def download_all() -> None:
    for url, dest in NOTEBOOKS:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        print(f"  Downloading {dest} …")
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=_SSL_CTX) as resp:
                data = resp.read()
            with open(dest, "wb") as f:
                f.write(data)
            size_kb = len(data) / 1024
            print(f"  ✓  {dest}  ({size_kb:.0f} KB)")
        except urllib.error.HTTPError as e:
            print(f"  ✗  {dest}  (HTTP {e.code})")
        except Exception as e:
            print(f"  ✗  {dest}  ({e})")


if __name__ == "__main__":
    print("Downloading notebooks from GitHub…\n")
    download_all()
    print("\nDone.")
