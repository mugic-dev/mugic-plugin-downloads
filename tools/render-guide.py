#!/usr/bin/env python3
"""Render an install guide from Markdown into a standalone page.

The install guides are written in the private repo (docs/MACOS_INSTALL.md,
docs/WINDOWS_INSTALL.md) and ship as release assets. Handing a musician a .md file
to download is a poor experience, so the Publish workflow runs this to serve them
as real pages instead.

Rendered at publish time rather than in the browser: an install guide is what
someone reads when the plugin *isn't* working, so it must not depend on JavaScript
or a CDN being reachable.

    python3 tools/render-guide.py <input.md> <output.html> --version 1.1.1 --platform macos

Needs: pip install markdown
"""
import argparse
import pathlib
import markdown

PLATFORM_LABEL = {"macos": "macOS", "windows": "Windows"}

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Installing the MUGIC MOTION plugin {version} on {platform}.">
<style>
  :root {{
    --bg:#f7f7f5; --card:#ffffff; --fg:#17181c; --muted:#5f6470;
    --line:#e3e4e8; --accent:#1f6feb; --soft:#f0f1f4;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --bg:#14151a; --card:#1c1e25; --fg:#e9eaee; --muted:#9ba1ae;
      --line:#2b2e37; --accent:#5b9dff; --soft:#23262f;
    }}
  }}
  :root[data-theme="dark"] {{
    --bg:#14151a; --card:#1c1e25; --fg:#e9eaee; --muted:#9ba1ae;
    --line:#2b2e37; --accent:#5b9dff; --soft:#23262f;
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--bg); color:var(--fg);
    font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased;
  }}
  .wrap {{ max-width:760px; margin:0 auto; padding:28px 20px 80px; }}
  .back {{
    display:inline-block; color:var(--muted); text-decoration:none;
    font-size:0.9rem; margin-bottom:26px;
  }}
  .back:hover {{ color:var(--accent); }}
  .doc {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:34px; }}
  h1 {{ font-size:1.7rem; margin:0 0 22px; letter-spacing:-0.02em; line-height:1.25; }}
  h2 {{ font-size:1.2rem; margin:34px 0 12px; letter-spacing:-0.01em; }}
  h3 {{ font-size:1rem; margin:26px 0 10px; }}
  h2:first-of-type {{ margin-top:24px; }}
  p, li {{ overflow-wrap:break-word; }}
  a {{ color:var(--accent); }}
  hr {{ border:0; border-top:1px solid var(--line); margin:32px 0; }}
  code {{ background:var(--soft); padding:2px 6px; border-radius:5px; font-size:0.88em; }}
  pre {{
    background:var(--soft); padding:14px 16px; border-radius:10px;
    overflow-x:auto; border:1px solid var(--line);
  }}
  pre code {{ background:none; padding:0; font-size:0.85rem; line-height:1.5; }}
  blockquote {{
    margin:18px 0; padding:2px 18px; border-left:3px solid var(--accent);
    color:var(--muted); background:var(--soft); border-radius:0 8px 8px 0;
  }}
  blockquote p {{ margin:12px 0; }}
  table {{ border-collapse:collapse; width:100%; margin:18px 0; font-size:0.94rem; }}
  th, td {{ border:1px solid var(--line); padding:9px 12px; text-align:left; vertical-align:top; }}
  th {{ background:var(--soft); font-weight:600; }}
  .tablewrap {{ overflow-x:auto; }}
  .ver {{ color:var(--muted); font-size:0.85rem; margin:26px 0 0; text-align:center; }}
</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="../../">&larr; All downloads</a>
  <article class="doc">
{body}
  </article>
  <p class="ver">MUGIC MOTION {version} &middot; {platform} install guide</p>
</div>
</body>
</html>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("output")
    ap.add_argument("--version", required=True)
    ap.add_argument("--platform", required=True, choices=sorted(PLATFORM_LABEL))
    args = ap.parse_args()

    text = pathlib.Path(args.source).read_text(encoding="utf-8")
    # tables and fenced_code are both used by the guides; sane_lists keeps a list
    # that follows a paragraph from being swallowed into it.
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])

    # Let wide tables scroll on a phone instead of forcing the page sideways.
    body = body.replace("<table>", '<div class="tablewrap"><table>').replace("</table>", "</table></div>")

    label = PLATFORM_LABEL[args.platform]
    html = TEMPLATE.format(
        title=f"Installing MUGIC MOTION {args.version} on {label}",
        version=args.version,
        platform=label,
        body="\n".join("    " + line for line in body.splitlines()),
    )

    out = pathlib.Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"rendered {args.platform} guide -> {out}")


if __name__ == "__main__":
    main()
