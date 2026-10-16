"""Check PyPI for a newer webmd and (optionally) rewrite Formula/webmd.rb to it.

  python3 bump_webmd.py check            # print GitHub outputs: update, version, url, sha256
  python3 bump_webmd.py apply FORMULA    # rewrite url/sha256 in FORMULA (reads VERSION/URL/SHA256 env)

Inputs from PyPI are validated before use: the URL must be a files.pythonhosted.org
webmd sdist and the sha256 must be 64 hex characters, so nothing unexpected can
reach the formula or the shell.
"""

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

FORMULA = Path(__file__).resolve().parents[2] / "Formula" / "webmd.rb"
URL_RE = re.compile(r"^https://files\.pythonhosted\.org/packages/[0-9a-f/]+/webmd-(\d+\.\d+\.\d+)\.tar\.gz$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def version_tuple(v):
    return tuple(int(x) for x in v.split("."))


def formula_version(text):
    m = re.search(r'url "https://files\.pythonhosted\.org/[^"]*/webmd-(\d+\.\d+\.\d+)\.tar\.gz"', text)
    if not m:
        sys.exit("could not find the webmd sdist url in the formula")
    return m.group(1)


def latest_sdist():
    with urllib.request.urlopen("https://pypi.org/pypi/webmd/json", timeout=30) as r:
        data = json.load(r)
    version = data["info"]["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        sys.exit(f"ignoring non-final release {version!r}")
    sdists = [u for u in data["urls"] if u["packagetype"] == "sdist" and not u.get("yanked")]
    if len(sdists) != 1:
        sys.exit(f"expected exactly one sdist for {version}, found {len(sdists)}")
    url, sha = sdists[0]["url"], sdists[0]["digests"]["sha256"]
    m = URL_RE.match(url)
    if not m or m.group(1) != version or not SHA_RE.match(sha):
        sys.exit(f"unexpected sdist url/sha256 from PyPI: {url} {sha}")
    return version, url, sha


def check():
    current = formula_version(FORMULA.read_text())
    version, url, sha = latest_sdist()
    update = version_tuple(version) > version_tuple(current)
    print(f"formula: {current}  pypi: {version}  -> {'update' if update else 'up to date'}", file=sys.stderr)
    out = os.environ.get("GITHUB_OUTPUT")
    lines = [f"update={'true' if update else 'false'}", f"current={current}", f"version={version}",
             f"url={url}", f"sha256={sha}"]
    if out:
        with open(out, "a") as f:
            f.write("\n".join(lines) + "\n")
    else:
        print("\n".join(lines))


def apply(path):
    version, url, sha = os.environ["VERSION"], os.environ["URL"], os.environ["SHA256"]
    m = URL_RE.match(url)
    if not m or m.group(1) != version or not SHA_RE.match(sha):
        sys.exit("refusing to write unvalidated url/sha256")
    p = Path(path)
    text = p.read_text()
    new, n_url = re.subn(r'^(\s*)url "[^"]*"$', rf'\1url "{url}"', text, count=1, flags=re.M)
    new, n_sha = re.subn(r'^(\s*)sha256 "[0-9a-f]{64}"$', rf'\1sha256 "{sha}"', new, count=1, flags=re.M)
    if n_url != 1 or n_sha != 1:
        sys.exit("could not find exactly one url and one sha256 line to update")
    p.write_text(new)
    print(f"{p}: webmd {formula_version(text)} -> {version}", file=sys.stderr)


if __name__ == "__main__":
    if sys.argv[1:2] == ["check"]:
        check()
    elif sys.argv[1:2] == ["apply"] and len(sys.argv) == 3:
        apply(sys.argv[2])
    else:
        sys.exit(__doc__)
