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

## Maintainers: releasing a new webmd version

The source copy of the formula lives in the webmd repo at
`packaging/homebrew/webmd.rb`. After a new version is on PyPI:

1. Get the sdist URL and sha256 from `https://pypi.org/pypi/webmd/<version>/json`
   (the entry with `"packagetype": "sdist"`).
2. Update `url` and `sha256` in `Formula/webmd.rb` here and in the webmd repo.
3. Open a PR. CI runs `brew style`, `brew audit --strict --online`,
   `brew install --build-from-source`, and `brew test` on Linux and macOS.
4. Merge. Users get it with `brew update && brew upgrade webmd`.
