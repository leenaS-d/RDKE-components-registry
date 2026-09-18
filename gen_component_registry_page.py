"""RDKE Core RDK Components generator."""
import json
from build import ROOT, esc, hero, load, shell


def build_components() -> None:
    source = load("components.json")
    records = source.get("components", [])
    data = [[item.get("name", ""), item.get("category", ""), item.get("layer", ""), (item.get("url") or [""])[0]] for item in records]
    categories = sorted({row[1] for row in data})
    layers = sorted({row[2] for row in data})
    body = hero("Core Components", "Core RDK Components", "The middleware-layer components of RDK-E. Together they provide a single, consistent implementation of core Entertainment device functionality, built on the Thunder framework, exposing standardized APIs to the application layer, and integrating with the vendor layer through the HAL. Delivered as binary packages, these components can be developed and updated independently of the other layers.")
    body += f'''<section class="section"><div class="stats"><div class="stat"><strong>{len(data)}</strong><span>Components</span></div><div class="stat"><strong>{len(categories)}</strong><span>Categories</span></div><div class="stat"><strong>{len(layers)}</strong><span>Layers</span></div><div class="stat"><strong>{esc(source.get("schemaVersion", "1.0"))}</strong><span>Schema version</span></div></div><div class="toolbar"><input id="search" type="search" placeholder="Search components" aria-label="Search components"><select id="category"><option value="">All categories</option>{''.join(f'<option>{esc(item)}</option>' for item in categories)}</select><select id="layer"><option value="">All layers</option>{''.join(f'<option>{esc(item)}</option>' for item in layers)}</select></div><div class="table-wrap"><table><thead><tr><th>Component</th><th>Category</th><th>Layer</th><th>Source</th></tr></thead><tbody id="rows"></tbody></table></div></section>'''
    rows = json.dumps(data, ensure_ascii=True)
    script = f'''<script>const DATA={rows};const esc=s=>{{const d=document.createElement('div');d.textContent=s;return d.innerHTML}};const search=document.querySelector('#search'),category=document.querySelector('#category'),layer=document.querySelector('#layer');function render(){{const q=search.value.toLowerCase();const rows=DATA.filter(c=>(!q||c.join(' ').toLowerCase().includes(q))&&(!category.value||c[1]===category.value)&&(!layer.value||c[2]===layer.value));document.querySelector('#rows').innerHTML=rows.length?rows.map(c=>`<tr><td>${{esc(c[0])}}</td><td><span class="pill">${{esc(c[1])}}</span></td><td>${{esc(c[2])}}</td><td><a href="${{esc(c[3])}}" target="_blank" rel="noopener">${{esc(c[3])}}</a></td></tr>`).join(''):'<tr><td class="empty" colspan="4">No components match the current filters.</td></tr>'}}[search,category,layer].forEach(e=>e.addEventListener('input',render));render()</script>'''
    footer = '<a href="https://github.com/rdkcentral/meta-rdk/blob/05c6119dcd99db78b8b9d7c6aff92194ed8e1d47/docs/core-components/core-v-components.json">Source: meta-rdk/docs/core-components/core-v-components.json</a>'
    (ROOT / "component-registry.html").write_text(shell("Core RDK Components | RDKE", "components", body + script, footer), encoding="utf-8")

if __name__ == "__main__":
    build_components()
