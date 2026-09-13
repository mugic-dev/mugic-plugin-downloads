# MUGIC MOTION® Plugin — Downloads

Public download page for the MUGIC MOTION plugin (Audio Unit, VST3, Standalone).

**→ [mugic-dev.github.io/mugic-plugin-downloads](https://mugic-dev.github.io/mugic-plugin-downloads/)**

This repository holds **no source code**. It exists so that releases can be
downloaded by users while the plugin source stays private. It contains:

| | |
|---|---|
| `index.html` | the download page, served by GitHub Pages |
| `versions.json` | the published versions and their release notes — read by the page |
| Releases | the actual `.pkg` / `.zip` downloads |

Both `versions.json` and the Releases here are written by the **Publish** workflow
in the private `mugic-plugin` repository. Don't edit them by hand — a later publish
would overwrite the change.

Not every build is published here. Versions are released publicly only when they
are blessed for general use, so the list is deliberately non-consecutive.

Source, issues and development: private repository `mugic-dev/mugic-plugin`.

## Install guides

`guides/<version>/{macos,windows}.html` are rendered from the private repo's
`docs/{MACOS,WINDOWS}_INSTALL.md` at publish time by `tools/render-guide.py`, so
users read them as pages instead of downloading a `.md`. They are generated —
edit the Markdown in the private repo, not the HTML here.
