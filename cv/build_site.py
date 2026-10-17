"""Gera a timeline da seção "Meu currículo" do index.html a partir de cv/pt.yaml.

Substitui apenas o trecho entre os marcadores <!-- cv:start --> e <!-- cv:end -->.
Cada entrada usa o campo `site` (uma frase curta), que o RenderCV ignora no PDF.
Uso: python cv/build_site.py
"""

from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CV_FILE = ROOT / "cv" / "pt.yaml"
INDEX_FILE = ROOT / "index.html"

START = "<!-- cv:start -->"
END = "<!-- cv:end -->"
INDENT = "\t" * 5

EXPERIENCE_SECTION = "Experiência Profissional"
EDUCATION_SECTION = "Formação Acadêmica"


def period(entry):
    start = str(entry["start_date"])[:4]
    end = entry.get("end_date")
    end = "Atual" if str(end) == "present" else str(end)[:4]
    return f"{start} - {end}"


def heading(title):
    return (
        f'{INDENT}<li class="timeline-heading text-center animate-box">\n'
        f"{INDENT}\t<div><h3>{escape(title)}</h3></div>\n"
        f"{INDENT}</li>\n"
    )


def item(index, icon, title, subtitle, text):
    side = "timeline-unverted" if index % 2 == 0 else "timeline-inverted"
    return (
        f'{INDENT}<li class="animate-box {side}">\n'
        f'{INDENT}\t<div class="timeline-badge"><i class="{icon}"></i></div>\n'
        f'{INDENT}\t<div class="timeline-panel">\n'
        f'{INDENT}\t\t<div class="timeline-heading">\n'
        f'{INDENT}\t\t\t<h3 class="timeline-title">{escape(title)}</h3>\n'
        f'{INDENT}\t\t\t<span class="company">{escape(subtitle)}</span>\n'
        f"{INDENT}\t\t</div>\n"
        f'{INDENT}\t\t<div class="timeline-body">\n'
        f"{INDENT}\t\t\t<p>{escape(text)}</p>\n"
        f"{INDENT}\t\t</div>\n"
        f"{INDENT}\t</div>\n"
        f"{INDENT}</li>\n"
    )


def build(cv):
    sections = cv["cv"]["sections"]
    html = heading(EXPERIENCE_SECTION)
    for i, job in enumerate(sections[EXPERIENCE_SECTION]):
        html += item(
            i,
            "icon-suitcase",
            job["position"],
            f"{job['company']} - {period(job)}",
            job["site"],
        )
    html += f"\n{INDENT}<br>\n" + heading(EDUCATION_SECTION)
    for i, course in enumerate(sections[EDUCATION_SECTION]):
        html += item(
            i + 1,
            "icon-graduation-cap",
            f"{course['degree']} em {course['area']}",
            f"{course['institution']} - {period(course)}",
            course["site"],
        )
    return html


def main():
    cv = yaml.safe_load(CV_FILE.read_text(encoding="utf-8"))
    page = INDEX_FILE.read_text(encoding="utf-8")
    before, rest = page.split(START, 1)
    _, after = rest.split(END, 1)
    page = f"{before}{START}\n{build(cv)}{INDENT}{END}{after}"
    INDEX_FILE.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
