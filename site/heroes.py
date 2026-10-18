"""Gera as hero images dos READMEs (assets/img/projects/<id>.png) a partir dos cards do site.

Cada card é renderizado com o CSS do site em 1280x640, o tamanho do social preview do GitHub.
Os READMEs dos projetos apontam para https://www.gustavofurtado.com/assets/img/projects/<id>.png.

Requer o Playwright (pip install playwright && playwright install chromium).
Uso: python site/heroes.py
"""

import tempfile
from pathlib import Path

import yaml
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "img" / "projects"

# O card é desenhado com 400 px de largura, a mesma escala do site, e ampliado para 1280.
WIDTH, HEIGHT, SCALE = 400, 200, 3.2

PAGE = """<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,200;0,700;0,800;1,600&display=swap">
<link rel="stylesheet" href="{root}/assets/style.css">
<style>
body {{ margin: 0; background: none; }}
.project {{ width: {width}px; aspect-ratio: auto; height: {height}px; transition: none; }}
.project:hover {{ transform: none; }}
</style>
</head>
<body>
<div class="project project--{id}" style="background-image: url({root}/assets/img/projects/{id}.svg);">
<span class="project-title">{title}</span>
</div>
</body>
</html>
"""


def main():
    projects = yaml.safe_load((ROOT / "site" / "projects.yaml").read_text(encoding="utf-8"))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=SCALE)
        # A página precisa estar em disco para carregar o CSS e os SVGs locais.
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "hero.html"
            for project in projects:
                html = PAGE.format(root=ROOT.as_uri(), width=WIDTH, height=HEIGHT, **project)
                html_path.write_text(html, encoding="utf-8")
                page.goto(html_path.as_uri(), wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                page.locator(".project").screenshot(path=OUT_DIR / f"{project['id']}.png")
        browser.close()


if __name__ == "__main__":
    main()
