"""RDKE home-page generator."""
from build import ROOT, esc, grouped_cards, hero, linked_metric_cards, load, shell, stacked_cards


def build_home() -> None:
    content = load("home-content.json")
    components = load("components.json")
    northbound = load("northbound-apis.json")
    southbound = load("southbound-apis.json")
    body = hero("", content["title"], content["description"], content["badges"])
    title_html = '<h1 style="font-size:clamp(1.9rem,3.6vw,3.5rem)">' + esc(content["title"]) + '</h1>'
    subtitle_html = f'<div class="hero-subtitle" style="font-size:.95rem;font-weight:600;line-height:1;color:#b8df63;margin:0">{esc(content["eyebrow"])}</div>'
    intro_html = f'<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px;line-height:1"><div style="display:inline-flex;align-items:center;padding:5px 12px;border:1px solid #b8df63;border-radius:999px;color:#b8df63;font:700 .72rem/1 Consolas,monospace;letter-spacing:.14em">RDKE</div>{subtitle_html}</div>'
    body = body.replace(title_html, intro_html + title_html, 1)
    why = content["why"]
    body += f'''<section class="section"><div class="eyebrow">Why RDKE</div><h2>{esc(why["title"])}</h2><p class="lede">{esc(why["description"])}</p>{stacked_cards(why["cards"])}</section>'''
    architecture = content["architecture"]
    body += f'''<section class="section alt"><div class="eyebrow">Architecture</div><h2>RDKE architecture</h2><div style="display:grid;gap:0;max-width:1000px">{''.join(f'<article class="card" style="border-left-color:{color};border-radius:0"><h3>{esc(layer[0])}</h3><p>{esc(layer[1])}</p></article>' for layer, color in zip(architecture["layers"], ("#29b6e8", "#7ac943", "#f5a623")))}</div></section>'''
    architecture_links = ["component-registry.html", "northbound-apis.html", "southbound-apis.html", "hardware-specifications.html"]
    architecture_metrics = [len(components.get("components", [])), len(northbound.get("apis", [])), len(southbound.get("apis", [])), None]
    body += f'''<section class="section"><div class="eyebrow">Registry access</div><h2>Explore the Core RDK platform</h2>{linked_metric_cards(architecture["cards"], architecture_links, architecture_metrics)}</section>'''
    (ROOT / "index.html").write_text(shell("RDKE. Core RDK Entertainment Platform", "home", body), encoding="utf-8")


if __name__ == "__main__":
    build_home()
