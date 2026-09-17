"""Build the self-contained RDKE static reference site.

Usage:
    python build.py
    python build.py --page components
    python build.py --page all --check

All inputs and outputs are kept inside this directory. The northbound,
southbound, and hardware pages intentionally support empty datasets until
their source workbook and profiles are provided.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from extract_hardware_spec import extract as extract_hardware_pdf

ROOT = Path(__file__).resolve().parent


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def nav(active: str) -> str:
    links = [
        ("index.html", "Home", "home"),
        ("component-registry.html", "Core RDK Components", "components"),
        ("northbound-apis.html", "Northbound APIs", "northbound"),
        ("southbound-apis.html", "Southbound APIs", "southbound"),
        ("hardware-specifications.html", "Hardware specifications", "hardware"),
    ]
    items = "".join(
        f'<a class="{"active" if key == active else ""}" href="{href}">{label}</a>'
        for href, label, key in links
    )
    return f'''<div class="accent"></div>
<header class="nav"><a class="brand" href="index.html"><img src="RDK-logo.png" alt="RDK"><span>RDKE Platform</span></a><nav class="navlinks">{items}</nav></header>'''


def shell(title: str, active: str, body: str, footer: str = "") -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
{nav(active)}
<main>
{body}
</main>
<footer class="footer"><div class="wrap">{footer}</div></footer>
</body>
</html>
'''


def hero(eyebrow: str, title: str, description: str, badges: list[str] | None = None) -> str:
    badge_html = "" if not badges else '<div class="badges">' + "".join(
        f'<span class="badge">{esc(item)}</span>' for item in badges
    ) + "</div>"
    return f'''<section class="hero"><div class="wrap"><div class="eyebrow" style="font-size:1.1rem;letter-spacing:.08em">{esc(eyebrow)}</div><h1 style="font-size:clamp(1.9rem,3.6vw,3.5rem)">{esc(title)}</h1><p>{esc(description)}</p>{badge_html}</div></section>'''


def cards(items: list[list[str]]) -> str:
    return '<div class="grid">' + "".join(
        f'<article class="card"><h3>{esc(item[0])}</h3><p>{esc(item[1])}</p></article>'
        for item in items
    ) + "</div>"


def grouped_cards(groups: list[dict]) -> str:
    rendered = []
    for group in groups:
        description = f'<p>{esc(group["description"])}</p>' if group.get("description") else ""
        items = "".join(f'<li>{esc(item)}</li>' for item in group.get("items", []))
        rendered.append(f'<article class="card"><h3>{esc(group["title"])}</h3>{description}<ul>{items}</ul></article>')
    return '<div class="grid">' + "".join(rendered) + "</div>"


def build_home() -> None:
    content = load("home-content.json")
    body = hero(content["eyebrow"], content["title"], content["description"], content["badges"])
    why = content["why"]
    body += f'''<section class="section"><div class="eyebrow">Why RDKE</div><h2>{esc(why["title"])}</h2><p class="lede">{esc(why["description"])}</p>{cards(why["cards"])}</section>'''
    architecture = content["architecture"]
    body += f'''<section class="section alt"><div class="eyebrow">Architecture</div><h2>{esc(architecture["title"])}</h2>{cards(architecture["cards"])}</section>'''
    for section in content.get("platform_detail", []):
        body += f'''<section class="section alt"><div class="eyebrow">{esc(section["eyebrow"])}</div><h2>{esc(section["title"])}</h2>{grouped_cards(section["groups"])}</section>'''
    facts = content["facts"]
    body += f'''<section class="section"><div class="eyebrow">{esc(facts["eyebrow"])}</div><h2>{esc(facts["title"])}</h2><div class="grid">{"".join(f'<article class="card fact"><h3>{esc(item)}</h3></article>' for item in facts["items"])}</div></section>'''
    (ROOT / "index.html").write_text(shell("RDKE Platform", "home", body), encoding="utf-8")


def build_components() -> None:
    source = load("components.json")
    records = source.get("components", [])
    data = [
        [item.get("name", ""), item.get("category", ""), item.get("layer", ""), (item.get("url") or [""])[0]]
        for item in records
    ]
    categories = sorted({row[1] for row in data})
    layers = sorted({row[2] for row in data})
    body = hero("RDK-E · RDK8 · Core Components", "Core RDK Components", "The middleware-layer components of RDK-E, as of the RDK8 release. Together they provide a single, consistent implementation of core Entertainment device functionality, built on the Thunder framework, exposing standardized APIs to the application layer, and integrating with the vendor layer through the HAL. Delivered as binary packages, these components can be developed and updated independently of the other layers.")
    body += f'''<section class="section"><div class="stats"><div class="stat"><strong>{len(data)}</strong><span>Components</span></div><div class="stat"><strong>{len(categories)}</strong><span>Categories</span></div><div class="stat"><strong>{len(layers)}</strong><span>Layers</span></div><div class="stat"><strong>{esc(source.get("schemaVersion", "1.0"))}</strong><span>Schema version</span></div></div><div class="toolbar"><input id="search" type="search" placeholder="Search components" aria-label="Search components"><select id="category"><option value="">All categories</option>{''.join(f'<option>{esc(item)}</option>' for item in categories)}</select><select id="layer"><option value="">All layers</option>{''.join(f'<option>{esc(item)}</option>' for item in layers)}</select></div><div class="table-wrap"><table><thead><tr><th>Component</th><th>Category</th><th>Layer</th><th>Source</th></tr></thead><tbody id="rows"></tbody></table></div></section>'''
    rows = json.dumps(data, ensure_ascii=True)
    script = f'''<script>const DATA={rows};const esc=s=>{{const d=document.createElement('div');d.textContent=s;return d.innerHTML}};const search=document.querySelector('#search'),category=document.querySelector('#category'),layer=document.querySelector('#layer');function render(){{const q=search.value.toLowerCase();const rows=DATA.filter(c=>(!q||c.join(' ').toLowerCase().includes(q))&&(!category.value||c[1]===category.value)&&(!layer.value||c[2]===layer.value));document.querySelector('#rows').innerHTML=rows.length?rows.map(c=>`<tr><td>${{esc(c[0])}}</td><td><span class="pill">${{esc(c[1])}}</span></td><td>${{esc(c[2])}}</td><td><a href="${{esc(c[3])}}" target="_blank" rel="noopener">${{esc(c[3])}}</a></td></tr>`).join(''):'<tr><td class="empty" colspan="4">No components match the current filters.</td></tr>'}}[search,category,layer].forEach(e=>e.addEventListener('input',render));render()</script>'''
    footer = '<a href="https://github.com/rdkcentral/meta-rdk/blob/05c6119dcd99db78b8b9d7c6aff92194ed8e1d47/docs/core-components/core-v-components.json">Source: meta-rdk/docs/core-components/core-v-components.json</a>'
    (ROOT / "component-registry.html").write_text(shell("Core RDK Components | RDKE", "components", body + script, footer), encoding="utf-8")


def build_api(kind: str) -> None:
    is_northbound = kind == "northbound"
    filename = "northbound-apis.json" if is_northbound else "southbound-apis.json"
    output = "northbound-apis.html" if is_northbound else "southbound-apis.html"
    title = "Northbound APIs" if is_northbound else "Southbound APIs"
    description = ("Standardized APIs the middleware exposes upward to the application layer, giving apps consistent access to device capabilities via Thunder and Firebolt." if is_northbound else "The Hardware Abstraction Layer (HAL) between middleware and the vendor layer — standardized interfaces that abstract hardware differences.")
    data = load(filename)
    records = data.get("apis", [])
    columns = "<th>Component</th><th>API</th><th>Description</th><th>Reference</th>" if is_northbound else "<th>Component</th><th>Header or interface</th><th>API</th><th>Signature / reference</th>"
    rows = "" if not records else "".join(f'<tr><td>{esc(item.get("component"))}</td><td>{esc(item.get("name"))}</td><td>{esc(item.get("description"))}</td><td>{esc(item.get("reference"))}</td></tr>' for item in records)
    if not rows:
        rows = f'<tr><td class="empty" colspan="4">No {title.lower()} have been loaded.</td></tr>'
    body = hero("Interface catalog", title, description) + f'''<section class="section"><div class="notice"><strong>API workbook status</strong><br>{esc(data.get("status", "ready"))}</div><div class="table-wrap" style="margin-top:24px"><table><thead><tr>{columns}</tr></thead><tbody>{rows}</tbody></table></div></section>'''
    (ROOT / output).write_text(shell(f"{title} | RDKE", kind, body, f"{title} specification page deferred for a later phase."), encoding="utf-8")


def build_hardware() -> None:
    data = load("hardware-spec.json")
    profiles = data.get("profiles", [])
    rows = "".join(f'<tr><td>{esc(item.get("profileName"))}</td><td>{esc(item.get("cpu"))}</td><td>{esc(item.get("memory"))}</td><td>{esc(item.get("storage"))}</td><td>{esc(item.get("validationStatus"))}</td></tr>' for item in profiles)
    if not rows:
        rows = '<tr><td class="empty" colspan="5">No hardware profiles have been loaded.</td></tr>'
    body = hero("RDK-E · Reference hardware", "Hardware specifications", "Reference hardware requirements and device specifications defined for the Entertainment OS platform.")
    body += f'''<section class="section"><div class="notice"><strong>Hardware profile status</strong><br>{esc(data.get("status", "ready"))}</div><div class="table-wrap" style="margin-top:24px"><table><thead><tr><th>Profile</th><th>CPU</th><th>Memory</th><th>Storage</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>'''
    sections = data.get("sections", [])
    if sections:
        section_html = []
        for section in sections:
            text_html = "".join(f"<p>{esc(line)}</p>" for line in section.get("text", []))
            table_html = ""
            for table in section.get("tables", []):
                table_rows = "".join(
                    "<tr>" + "".join(f"<td>{esc(cell)}</td>" for cell in row) + "</tr>"
                    for row in table
                )
                table_html += f'<div class="table-wrap pdf-table"><table><tbody>{table_rows}</tbody></table></div>'
            section_html.append(f'<article class="card pdf-section"><h3>Page {esc(section.get("page"))}</h3>{text_html}{table_html}</article>')
        body += '<div class="subhead">Extracted specification</div><div class="pdf-sections">' + "".join(section_html) + "</div>"
    body += '</section>'
    (ROOT / "hardware-specifications.html").write_text(shell("Hardware Specifications | RDKE", "hardware", body, "Hardware profile data is kept local to RDKE."), encoding="utf-8")


def build(page: str) -> None:
    hardware_pdf = ROOT / "hardware-spec.pdf"
    if page in ("all", "hardware") and hardware_pdf.exists():
        (ROOT / "hardware-spec.json").write_text(
            json.dumps(extract_hardware_pdf(hardware_pdf), indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )
    if page in ("all", "home"):
        build_home()
    if page in ("all", "components"):
        build_components()
    if page in ("all", "northbound"):
        build_api("northbound")
    if page in ("all", "southbound"):
        build_api("southbound")
    if page in ("all", "hardware"):
        build_hardware()


def check() -> None:
    required = ["index.html", "component-registry.html", "northbound-apis.html", "southbound-apis.html", "hardware-specifications.html"]
    missing = [name for name in required if not (ROOT / name).exists()]
    if missing:
        raise SystemExit("Missing generated pages: " + ", ".join(missing))
    for name in ("home-content.json", "components.json", "northbound-apis.json", "southbound-apis.json", "hardware-spec.json"):
        load(name)
    print(f"RDKE build check passed: {len(load('components.json')['components'])} components")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--page", choices=["all", "home", "components", "northbound", "southbound", "hardware"], default="all")
    parser.add_argument("--check", action="store_true", help="Validate inputs and generated page presence")
    args = parser.parse_args()
    build(args.page)
    if args.check:
        check()
