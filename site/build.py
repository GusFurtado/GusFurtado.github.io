"""Gera as páginas do site (uma por idioma) a partir de site/template.html.

- Textos fixos: site/strings.yaml. O primeiro idioma é o padrão e vai para /index.html;
  os demais vão para /<idioma>/index.html.
- Projetos: site/projects.yaml (iguais nos dois idiomas).
- Currículo: cv/<idioma>.yaml. Cada entrada usa o campo `site` (uma frase curta),
  que o RenderCV ignora no PDF.

Uso: python site/build.py
"""

from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / "site"
CV_DIR = ROOT / "cv"
SITE_URL = "https://www.gustavofurtado.com/"


def load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def period(entry, present):
    start = str(entry["start_date"])[:4]
    end = entry.get("end_date")
    end = present if str(end) == "present" else str(end)[:4]
    return f"{start} - {end}"


def timeline(sections, t):
    jobs = [
        {
            "title": job["position"],
            "subtitle": f"{job['company']} - {period(job, t['present'])}",
            "text": job["site"],
            "pdf": None,
        }
        for job in sections[t["experience_section"]]
    ]
    courses = [
        {
            "title": f"{course['degree']} {t['degree_in']} {course['area']}",
            "subtitle": f"{course['institution']} - {period(course, t['present'])}",
            "text": course["site"],
            "pdf": course.get("pdf"),
        }
        for course in sections[t["education_section"]]
    ]
    # Os cartões alternam entre esquerda e direita ao longo de toda a linha do tempo.
    for i, item in enumerate(jobs + courses):
        item["side"] = "left" if i % 2 == 0 else "right"
    return [
        {"title": t["experience_section"], "icon": "i-briefcase", "items": jobs},
        {"title": t["education_section"], "icon": "i-graduation", "items": courses},
    ]


def author(name):
    # O RenderCV marca o próprio nome em negrito com **...**.
    me = name.startswith("**") and name.endswith("**")
    return {"name": name.strip("*"), "me": me}


def publications(sections, t):
    return [
        {
            "title": pub["title"],
            "authors": [author(name) for name in pub["authors"]],
            "journal": pub["journal"],
            "year": str(pub["date"])[:4],
            "doi": pub.get("doi"),
            "pdf": pub["pdf"],
        }
        for pub in sections[t["publications_section"]]
    ]


def main():
    strings = load_yaml(SITE_DIR / "strings.yaml")
    projects = load_yaml(SITE_DIR / "projects.yaml")
    default_lang = next(iter(strings))
    languages = [
        {
            "code": code,
            "label": t["label"],
            "html_lang": t["html_lang"],
            "path": "" if code == default_lang else f"{code}/",
        }
        for code, t in strings.items()
    ]
    env = Environment(
        loader=FileSystemLoader(SITE_DIR),
        autoescape=True,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    template = env.get_template("template.html")

    for language in languages:
        code = language["code"]
        t = strings[code]
        cv = load_yaml(CV_DIR / f"{code}.yaml")["cv"]
        out_dir = ROOT / language["path"]
        out_dir.mkdir(exist_ok=True)
        html = template.render(
            t=t,
            cv=cv,
            lang=code,
            default_lang=default_lang,
            languages=languages,
            site_url=SITE_URL,
            root="../" if language["path"] else "",
            summary=cv["sections"][t["summary_section"]],
            timeline=timeline(cv["sections"], t),
            projects=projects,
            publications=publications(cv["sections"], t),
        )
        (out_dir / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
