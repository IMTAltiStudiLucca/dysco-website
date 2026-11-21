#!/usr/bin/env python3
"""Report broken external links found in content/. Usage: python3 check_links.py
Only the standard library is used. Needs an internet connection."""
import re
import ssl
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
urls = {}
for f in (ROOT / "content").rglob("*"):
    if f.suffix in {".md", ".json"}:
        for u in re.findall(r"https?://[^\s)\"'<>]+", f.read_text(encoding="utf-8")):
            urls.setdefault(u.rstrip(".,;"), f.relative_to(ROOT))


def check(u):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(u, method=method, headers={"User-Agent": "Mozilla/5.0 link-check"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return u, r.status
        except urllib.error.HTTPError as ex:
            if method == "GET" or ex.code not in (403, 405, 501):
                return u, ex.code
        except (urllib.error.URLError, ssl.SSLError, TimeoutError, OSError) as ex:
            if method == "GET":
                return u, f"error {getattr(ex, 'reason', ex)}"
    return u, "unknown"


with ThreadPoolExecutor(8) as ex:
    results = list(ex.map(check, urls))
bad = [(u, s) for u, s in results if not (isinstance(s, int) and s < 400)]
for u, s in bad:
    print(f"{s}\t{u}\t({urls[u]})")
print(f"{len(urls)} links checked, {len(bad)} to review")
sys.exit(1 if bad else 0)
