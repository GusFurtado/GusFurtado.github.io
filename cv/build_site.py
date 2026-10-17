"""Gera partes do index.html a partir de cv/pt.yaml.

- Entre <!-- about:start --> e <!-- about:end -->: o resumo, na seção "Sobre mim".
- Entre <!-- cv:start --> e <!-- cv:end -->: a timeline da seção "Meu currículo".
  Cada entrada usa o campo `site` (uma frase curta), que o RenderCV ignora no PDF.
Uso: python cv/build_site.py
"""

from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CV_FILE = ROOT / "cv" / "pt.yaml"
INDEX_FILE = ROOT / "index.html"

INDENT = "\t" * 3
ABOUT_INDENT = "\t" * 5

SUMMARY_SECTION = "Resumo"

EXPERIENCE_SECTION = "Experiência Profissional"
EDUCATION_SECTION = "Formação Acadêmica"


def period(entry):
    start = str(entry["start_date"])[:4]
    end = entry.get("end_date")
    end = "Atual" if str(end) == "present" else str(end)[:4]
    return f"{start} - {end}"


def heading(title):
    return (
        f'{INDENT}<li class="timeline-section animate-box"><h3>{escape(title)}</h3></li>\n'
    )


def item(index, icon, title, subtitle, text):
    side = "left" if index % 2 == 0 else "right"
    return (
        f'{INDENT}<li class="timeline-item {side} animate-box">\n'
        f'{INDENT}\t<span class="timeline-badge"><svg class="icon"><use href="#{icon}"/></svg></span>\n'
        f'{INDENT}\t<div class="timeline-panel">\n'
        f"{INDENT}\t\t<h3>{escape(title)}</h3>\n"
        f'{INDENT}\t\t<span class="company">{escape(subtitle)}</span>\n'
        f"{INDENT}\t\t<p>{escape(text)}</p>\n"
        f"{INDENT}\t</div>\n"
        f"{INDENT}</li>\n"
    )


def build(cv):
    sections = cv["cv"]["sections"]
    html = heading(EXPERIENCE_SECTION)
    for i, job in enumerate(sections[EXPERIENCE_SECTION]):
        html += item(
            i,
            "i-briefcase",
            job["position"],
            f"{job['company']} - {period(job)}",
            job["site"],
        )
    html += heading(EDUCATION_SECTION)
    for i, course in enumerate(sections[EDUCATION_SECTION]):
        html += item(
            i + 1,
            "i-graduation",
            f"{course['degree']} em {course['area']}",
            f"{course['institution']} - {period(course)}",
            course["site"],
        )
    return html


def build_about(cv):
    return "".join(
        f"{ABOUT_INDENT}<p>{escape(text)}</p>\n"
        for text in cv["cv"]["sections"][SUMMARY_SECTION]
    )


def replace_between(page, name, content, indent):
    start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
    before, rest = page.split(start, 1)
    _, after = rest.split(end, 1)
    return f"{before}{start}\n{content}{indent}{end}{after}"


def main():
    cv = yaml.safe_load(CV_FILE.read_text(encoding="utf-8"))
    page = INDEX_FILE.read_text(encoding="utf-8")
    page = replace_between(page, "about", build_about(cv), ABOUT_INDENT)
    page = replace_between(page, "cv", build(cv), INDENT)
    INDEX_FILE.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
