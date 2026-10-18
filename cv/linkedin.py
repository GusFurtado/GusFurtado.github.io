"""Imprime o currículo no formato das seções do LinkedIn, para copiar e colar.

O LinkedIn não tem API para editar o perfil, então o texto sai de cv/<idioma>.yaml,
a mesma fonte do PDF e do site.

Uso: python cv/linkedin.py [pt|en]   (padrão: pt)
"""

import re
import sys
from pathlib import Path

import yaml

CV_DIR = Path(__file__).resolve().parent

LABELS = {
    "pt": {
        "headline": "Título",
        "about": "Sobre",
        "experience": "Experiência",
        "education": "Formação acadêmica",
        "publications": "Publicações",
        "projects": "Projetos",
        "honors": "Prêmios e reconhecimentos",
        "skills": "Competências",
        "present": "o momento",
        "sections": {
            "summary": "Resumo",
            "experience": "Experiência Profissional",
            "education": "Formação Acadêmica",
            "publications": "Publicações",
            "projects": "Projetos",
            "honors": "Reconhecimentos",
            "skills": "Data Stack",
        },
        "months": "jan fev mar abr mai jun jul ago set out nov dez".split(),
    },
    "en": {
        "headline": "Headline",
        "about": "About",
        "experience": "Experience",
        "education": "Education",
        "publications": "Publications",
        "projects": "Projects",
        "honors": "Honors & awards",
        "skills": "Skills",
        "present": "Present",
        "sections": {
            "summary": "Summary",
            "experience": "Professional Experience",
            "education": "Education",
            "publications": "Publications",
            "projects": "Projects",
            "honors": "Awards",
            "skills": "Data Stack",
        },
        "months": "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(),
    },
}


def plain(text):
    """Remove a marcação Markdown do RenderCV (negrito e links)."""
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", str(text))
    return re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", text)


def month(value, labels):
    if str(value) == "present":
        return labels["present"]
    year, _, mon = str(value).partition("-")
    return f"{labels['months'][int(mon) - 1]} {year}" if mon else year


def heading(title):
    return f"\n=== {title} ===\n"


def main(lang):
    labels = LABELS[lang]
    names = labels["sections"]
    cv = yaml.safe_load((CV_DIR / f"{lang}.yaml").read_text(encoding="utf-8"))["cv"]
    sections = cv["sections"]
    out = []

    out.append(heading(labels["headline"]))
    out.append(cv["headline"])

    out.append(heading(labels["about"]))
    out.append("\n\n".join(plain(p) for p in sections[names["summary"]]))

    out.append(heading(labels["experience"]))
    for job in sections[names["experience"]]:
        period = f"{month(job['start_date'], labels)} - {month(job['end_date'], labels)}"
        out.append(f"{job['position']}\n{job['company']} · {job.get('location') or ''} · {period}")
        out.append("\n".join(f"• {plain(h)}" for h in job["highlights"]) + "\n")

    out.append(heading(labels["education"]))
    for course in sections[names["education"]]:
        period = f"{str(course['start_date'])[:4]} - {str(course['end_date'])[:4]}"
        out.append(f"{course['institution']}\n{course['degree']}, {course['area']} · {period}")
        out.append("\n".join(f"• {plain(h)}" for h in course["highlights"]) + "\n")

    out.append(heading(labels["publications"]))
    for pub in sections[names["publications"]]:
        url = f"https://doi.org/{pub['doi']}" if pub.get("doi") else f"https://www.gustavofurtado.com/{pub['pdf']}"
        authors = ", ".join(plain(a) for a in pub["authors"])
        out.append(f"{pub['title']}\n{pub['journal']} · {month(pub['date'], labels)}\n{url}\n{authors}\n")

    out.append(heading(labels["projects"]))
    for project in sections[names["projects"]]:
        out.append(f"{plain(project['name'])}\n{plain(project['summary'])}\n")

    out.append(heading(labels["honors"]))
    out.append("\n".join(plain(h) for h in sections[names["honors"]]))

    out.append(heading(labels["skills"]))
    skills = []
    for group in sections[names["skills"]]:
        skills += [s.strip() for s in group["details"].split(",")]
    out.append(", ".join(dict.fromkeys(skills)))

    print("\n".join(out).strip() + "\n")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pt")
