# lets-qa Homebrew tap

Homebrew formulae for [lets-qa](https://github.com/lets-qa) tools.

| Formula | Description |
|---|---|
| [`webmd`](https://github.com/lets-qa/webmd) | Serve a directory in the browser, rendering Markdown files as web pages |

## Install

```bash
brew install lets-qa/tap/webmd
```

This adds the tap (`brew tap lets-qa/tap`) and installs in one step.

## Upgrade

```bash
brew update
brew upgrade webmd
```

## Uninstall

```bash
brew uninstall webmd
brew untap lets-qa/tap      # optional: remove the tap too
```

## Notes

- `webmd` is installed into its own Python virtualenv. It uses Homebrew's
  `cryptography` formula, so nothing is compiled from source except webmd
  itself, which is pure Python and takes about 30 seconds.
- Other install options (pipx, uv, pip) are in the
  [webmd README](https://github.com/lets-qa/webmd#install).

## How new webmd versions arrive

**Automatic.** The [`Bump webmd`](.github/workflows/bump-webmd.yml) workflow
runs daily at 06:17 UTC. When PyPI has a newer webmd than `Formula/webmd.rb`:

1. It takes the new sdist's URL and sha256 from PyPI and validates both: a
   `files.pythonhosted.org` webmd sdist URL, and a 64-character hex sha256.
2. It tests the updated formula on **Linux and macOS**: `brew style`,
   `brew audit --strict --online`, an install from source, `brew test`, and a
   check that `webmd --version` matches.
3. **Only if all of those pass**, it commits the `url`/`sha256` change to
   `main`. It refuses to commit if anything else in the repo changed.

If any check fails, nothing is committed and the run shows as failed. GitHub
emails the repo admins about failed scheduled runs. When nothing is new, it
finishes in a few seconds.

To pick up a release right away instead of waiting: *Actions → Bump webmd → Run
workflow*, or `gh workflow run bump-webmd.yml --repo lets-qa/homebrew-tap`.

It commits directly because the lets-qa organization doesn't allow GitHub
Actions to open pull requests. Pull requests from people are still tested by
[`tests.yml`](.github/workflows/tests.yml).

**Manual fallback** (for example, a release needing more than a url/sha256
change): edit `url` and `sha256` from
`https://pypi.org/pypi/webmd/<version>/json` (the `sdist` entry), open a PR,
and merge when CI is green. Keep `packaging/homebrew/webmd.rb` in the webmd
repo in sync.
