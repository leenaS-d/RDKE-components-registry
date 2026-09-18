"""RDKE home-page generator."""
from build import ROOT, cards, esc, grouped_cards, hero, load, shell


def build_home() -> None:
    content = load("home-content.json")
    body = hero("", content["title"], content["description"], content["badges"], content["eyebrow"])
    body = body.replace('<h1 style="font-size:clamp(1.9rem,3.6vw,3.5rem)">', '<div style="display:inline-block;margin-bottom:14px;padding:5px 12px;border:1px solid #b8df63;border-radius:999px;color:#b8df63;font:700 .72rem/1 Consolas,monospace;letter-spacing:.14em">RDKE</div><h1 style="font-size:clamp(1.9rem,3.6vw,3.5rem)">', 1)
    why = content["why"]
    body += f'''<section class="section"><div class="eyebrow">Why RDKE</div><h2>{esc(why["title"])}</h2><p class="lede">{esc(why["description"])}</p>{cards(why["cards"])}</section>'''
    architecture = content["architecture"]
    body += f'''<section class="section alt"><div class="eyebrow">Architecture</div><h2>{esc(architecture["title"])}</h2>{cards(architecture["cards"])}</section>'''
    for section in content.get("platform_detail", []):
        body += f'''<section class="section alt"><div class="eyebrow">{esc(section["eyebrow"])}</div><h2>{esc(section["title"])}</h2>{grouped_cards(section["groups"])}</section>'''
    facts = content["facts"]
    body += f'''<section class="section"><div class="eyebrow">{esc(facts["eyebrow"])}</div><h2>{esc(facts["title"])}</h2><div class="grid">{"".join(f'<article class="card fact"><h3>{esc(item)}</h3></article>' for item in facts["items"])}</div></section>'''
    (ROOT / "index.html").write_text(shell("RDKE. Core RDK Entertainment Platform", "home", body), encoding="utf-8")

if __name__ == "__main__":
    build_home()
