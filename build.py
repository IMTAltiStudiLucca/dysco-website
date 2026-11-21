#!/usr/bin/env python3
"""Build the static DYSCO website from content/ into plain HTML files.

Usage:  python3 build.py
Only the Python standard library is used. Output files (index.html, people.html, ...)
are written next to this script and must be committed, since GitHub Pages serves them.
"""
import datetime
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
TEMPLATE = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")


# ---------------------------------------------------------------- content helpers
def read_md(path):
    """Return (meta dict, body str). Front matter is `key: value` lines between `---`."""
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if line.strip() and not line.lstrip().startswith("#"):
                if ":" not in line:
                    sys.exit(f"{path}: bad front matter line {line!r}")
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        body = m.group(2)
    return meta, body.strip()


def md_files(folder):
    return sorted(p for p in (CONTENT / folder).glob("*.md") if not p.name.startswith("_"))


def inline(text):
    """Escape HTML, then apply [text](url), **bold** and *italic*."""
    t = html.escape(text, quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
               lambda m: f'<a href="{m.group(2)}"{ext(m.group(2))}>{m.group(1)}</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
    return t


def ext(url):
    return ' target="_blank" rel="noopener noreferrer"' if url.startswith("http") else ""


def markdown(body):
    """Tiny Markdown subset: ## / ### headings, - lists, paragraphs, inline markup."""
    out, para, items = [], [], []

    def flush():
        nonlocal para, items
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
        para, items = [], []

    for line in body.splitlines():
        s = line.strip()
        if not s:
            flush()
        elif s.startswith("### "):
            flush(); out.append(f"<h3>{inline(s[4:])}</h3>")
        elif s.startswith("## "):
            flush(); out.append(f"<h2>{inline(s[3:])}</h2>")
        elif s.startswith("- "):
            if para:
                flush()
            items.append(s[2:])
        else:
            if items:
                flush()
            para.append(s)
    flush()
    return "\n".join(out)


def e(s):
    return html.escape(s, quote=True)


def check_file(rel):
    if not (CONTENT / rel).is_file():
        sys.exit(f"Missing file referenced in content: content/{rel}")
    return f"content/{rel}"


# ---------------------------------------------------------------- page builders
SITE = json.loads((CONTENT / "site.json").read_text(encoding="utf-8"))


def figure(meta, key, cls="figure"):
    if not meta.get(key):
        return ""
    src = check_file(meta[key])
    credit = meta.get(key + "_credit", "")
    if credit and meta.get(key + "_credit_url"):
        credit = f'<a href="{e(meta[key + "_credit_url"])}"{ext(meta[key + "_credit_url"])}>{e(credit)}</a>'
    else:
        credit = e(credit)
    cap = f"<figcaption>{credit}</figcaption>" if credit else ""
    return (f'<figure class="{cls}"><img src="{src}" alt="{e(meta.get(key + "_alt", ""))}" '
            f'loading="lazy">{cap}</figure>')


def page_home():
    meta, body = read_md(CONTENT / "pages" / "home.md")
    tagline = f'<p class="tagline">{e(meta["tagline"])}</p>' if meta.get("tagline") else ""
    hero = f"""
<section class="hero">
  <img class="hero-bg" src="{check_file(meta["image"])}" alt="" aria-hidden="true">
  <div class="wrap">
    <h1><span class="wordmark">{e(SITE['name'])}</span><span class="slogan">{e(meta['title'])}</span></h1>
    {tagline}
    <p class="hero-links"><a class="btn" href="#research">Our research</a>
      <a class="btn btn-ghost" href="#people">People</a></p>
  </div>
</section>"""
    main = f"""{hero}
<div class="wrap">
  <section class="section"><div class="prose">{markdown(body)}</div></section>
</div>"""
    return {"title": SITE["name"] + " | Control, optimization and learning research group at IMT Lucca", "desc": SITE["description"],
            "main": main, "page": "index"}


def initials(name):
    parts = [p for p in re.split(r"[\s.]+", name) if p]
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else name[:2].upper()


def person_card(meta):
    name = meta["name"]
    if meta.get("photo"):
        img = (f'<div class="photo"><img src="{check_file("people/photos/" + meta["photo"])}" '
               f'alt="{e(name)}" loading="lazy"></div>')
    else:
        img = f'<div class="photo"><span class="avatar" aria-hidden="true">{e(initials(name))}</span></div>'
    links = []
    if meta.get("scholar"):
        links.append(("Google Scholar", meta["scholar"]))
    if meta.get("website"):
        links.append(("Personal webpage", meta["website"]))
    if meta.get("email"):
        links.append(("Email", "mailto:" + meta["email"]))
    pills = "".join(f'<a href="{e(u)}"{ext(u)} aria-label="{l} of {e(name)}">{l}</a>' for l, u in links)
    return (f'<article class="person">{img}<p class="role">{e(meta.get("role", ""))}</p>'
            f'<h3>{e(name)}</h3><p class="pills">{pills}</p></article>')


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def page_people():
    people = [read_md(p)[0] for p in md_files("people")]
    groups = SITE["people_groups"]
    for p in people:
        if p.get("group") not in groups:
            sys.exit(f"{p.get('name')}: group {p.get('group')!r} is not in people_groups of site.json")
    sections, jump = [], []
    list_groups = SITE.get("people_list_groups", [])
    for g in groups:
        members = sorted((p for p in people if p["group"] == g),
                         key=lambda p: (float(p.get("order", 100)), p["name"].split()[-1].lower()))
        if not members:
            continue
        jump.append(f'<a href="#{slug(g)}">{e(g)}</a>')
        if g in list_groups:
            items = "".join(
                "<li>" + (f'<a href="{e(p["website"])}"{ext(p["website"])}>{e(p["name"])}</a>' if p.get("website")
                          else e(p["name"])) + "</li>" for p in members)
            body = f'<ul class="name-list">{items}</ul>'
        else:
            body = '<div class="grid people">' + "".join(person_card(p) for p in members) + "</div>"
        sections.append(f'<section class="section" id="{slug(g)}"><h2 class="center">{e(g)}</h2>{body}</section>')
    main = (f'<div class="wrap"><header class="page-head center"><h1>People</h1>'
            f'<p class="jump">{" | ".join(jump)}</p></header>{"".join(sections)}</div>')
    return {"title": "People | " + SITE["name"] + " research group, IMT Lucca", "desc": "Faculty, postdocs and PhD students of the DYSCO research unit at IMT Lucca.",
            "main": main, "page": "people"}


def page_research():
    meta, _ = read_md(CONTENT / "research" / "research.md")
    topics = "".join(
        f'<article class="card"><h3>{e(m["title"])}</h3><div class="prose">{markdown(b)}</div></article>'
        for m, b in (read_md(p) for p in md_files("research/topics")))
    apps = "".join(
        f'<article class="card soft"><h3>{e(m["title"])}</h3><p>{inline(b)}</p></article>'
        for m, b in (read_md(p) for p in md_files("research/applications")))
    cm, cb = read_md(CONTENT / "research" / "collaborations.md")
    sm, sb = read_md(CONTENT / "research" / "spinoff.md")
    pubs = "".join(
        f'<li><a href="{e(p["scholar"])}" target="_blank" rel="noopener noreferrer">{e(p["name"])}</a></li>'
        for p in sorted((read_md(f)[0] for f in md_files("people")),
                        key=lambda p: float(p.get("order", 100))) if p.get("scholar") and p.get("group") == "Faculty")
    pubsec = (f'<section class="section"><h2>Publications</h2><p class="lead">Publications are listed on the '
              f'Google Scholar profile of each faculty member.</p><ul class="chips">{pubs}</ul></section>'
              if pubs else "")
    main = f"""<div class="wrap">
<header class="page-head"><h1>{e(meta['title'])}</h1></header>
<div class="split"><section><h2>Research topics</h2><div class="stack">{topics}</div></section>
{figure(meta, 'image', 'figure side')}</div>
<section class="section"><h2>Applications</h2>
<div class="grid g2">{apps}</div></section>
{pubsec}
<section class="section"><h2>{e(cm['title'])}</h2><div class="prose">{markdown(cb)}</div></section>
<section class="section"><h2>Spinoff company</h2><div class="prose">{markdown(sb)}</div></section>
</div>"""
    return {"title": "Research | " + SITE["name"] + ", model predictive control and optimization", "desc": "Research topics of DYSCO at IMT Lucca. Model predictive control, numerical optimization, machine learning and system identification, with applications.",
            "main": main, "page": "research"}


def page_collab():
    meta, body = read_md(CONTENT / "pages" / "collab.md")
    main = f"""<div class="wrap"><header class="page-head"><h1>{e(meta['title'])}</h1>
<p>{e(meta['subtitle'])}</p></header>
<div class="split"><section class="prose">{markdown(body)}</section>
{figure(meta, 'image', 'figure side logo')}</div></div>"""
    return {"title": "COLLab | " + SITE["name"], "desc": meta["subtitle"] + " of the DYSCO research unit.",
            "main": main, "page": "collab"}


def page_software():
    cards = []
    for m, b in (read_md(p) for p in md_files("software")):
        inner = (f'<p class="tag">{e(m.get("tag", ""))}</p><h3>{e(m["name"])}</h3><p>{inline(b)}</p>')
        if m.get("url"):
            cards.append(f'<a class="card link-card" href="{e(m["url"])}"{ext(m["url"])}>{inner}'
                         f'<span class="arrow" aria-hidden="true">↗</span></a>')
        else:
            cards.append(f'<div class="card">{inner}</div>')
    main = ('<div class="wrap"><header class="page-head"><h1>Software</h1>'
            '<p>MATLAB and Python packages for real-time model predictive control, numerical '
            'optimization, and system identification.</p></header>'
            f'<div class="grid g3">{"".join(cards)}</div></div>')
    return {"title": "Software | " + SITE["name"] + ", control and optimization tools", "desc": "MATLAB and Python packages for model predictive control, optimization, system identification and machine learning developed by DYSCO.",
            "main": main, "page": "software"}


def page_teaching():
    meta, body = read_md(CONTENT / "pages" / "teaching.md")
    rows = []
    for m, _ in (read_md(p) for p in md_files("teaching")):
        if m.get("url"):
            rows.append(f'<li><a href="{e(m["url"])}"{ext(m["url"])}><span>{e(m["title"])}</span>'
                        f'<span class="arrow" aria-hidden="true">↗</span></a></li>')
        else:
            rows.append(f'<li><div class="row"><span>{e(m["title"])}</span></div></li>')
    main = (f'<div class="wrap"><header class="page-head"><h1>{e(meta["title"])}</h1>'
            f'<div class="prose">{markdown(body)}</div></header><ul class="rows">{"".join(rows)}</ul></div>')
    return {"title": "Teaching | " + SITE["name"], "desc": "PhD courses offered by DYSCO.",
            "main": main, "page": "teaching"}


def page_join():
    meta, body = read_md(CONTENT / "pages" / "join.md")
    main = (f'<div class="wrap"><header class="page-head"><h1>{e(meta["title"])}</h1>'
            f'<p>{e(meta.get("intro", ""))}</p></header>'
            f'<section class="prose section">{markdown(body)}</section></div>')
    return {"title": "Join us | " + SITE["name"], "desc": meta.get("intro", ""), "main": main, "page": "join"}


def page_contact():
    meta, body = read_md(CONTENT / "pages" / "contact.md")
    addr = "<br>".join(e(l) for l in SITE["address"])
    tel = SITE["phone"]
    main = f"""<div class="wrap"><header class="page-head"><h1>{e(meta['title'])}</h1></header>
<div class="split">
<section class="prose"><h2>Address</h2>
<p>{e(SITE['name'])}, {e(SITE['slogan'])}<br>{e(SITE['institution'])}<br>{addr}</p>
<p><a href="{e(meta['map_url'])}" target="_blank" rel="noopener noreferrer">Open in OpenStreetMap ↗</a></p>
<h2>Email and phone</h2>
<p><a href="mailto:{e(SITE['email'])}">{e(SITE['email'])}</a><br>
<a href="tel:{e(re.sub(r'[^+0-9]', '', tel))}">{e(tel)}</a></p>
{markdown(body)}</section>
{figure(meta, 'image', 'figure side')}</div></div>"""
    return {"title": "Contact | " + SITE["name"], "desc": "How to contact DYSCO.",
            "main": main, "page": "contact"}


# ---------------------------------------------------------------- assemble
def jsonld():
    data = {"@context": "https://schema.org", "@type": "ResearchOrganization", "name": SITE["name"],
            "alternateName": SITE["slogan"], "url": SITE["site_url"], "email": SITE["email"],
            "description": SITE["description"],
            "parentOrganization": {"@type": "CollegeOrUniversity", "name": SITE["institution"],
                                   "url": SITE["institution_url"]},
            "address": {"@type": "PostalAddress", "streetAddress": SITE["address"][0],
                        "addressLocality": "Lucca", "postalCode": "55100", "addressCountry": "IT"}}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def render(p):
    nav = "".join(
        f'<a href="#{n["page"] if n["page"] != "index" else "home"}">{e(n["label"])}</a>' for n in SITE["nav"])
    addr = ", ".join(SITE["address"])
    footer = (f'&copy; {datetime.date.today().year} <a href="{e(SITE["institution_url"])}" target="_blank" rel="noopener noreferrer">'
              f'{e(SITE["institution"])}</a><br>{e(addr)}<br>'
              f'<a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a> &middot; {e(SITE["phone"])}')
    subs = {"TITLE": e(p["title"]), "DESC": e(p["desc"]), "NAME": e(SITE["name"]),
            "SLOGAN": e(SITE["slogan"]), "NAV": nav, "MAIN": p["main"], "FOOTER": footer,
            "PAGEFILE": "index.html" if p["page"] == "index" else p["page"] + ".html"}
    subs["CANONICAL"] = SITE["site_url"]
    subs["OGIMAGE"] = SITE["site_url"] + SITE["share_image"]
    subs["JSONLD"] = jsonld() if p["page"] == "index" else ""
    out = TEMPLATE
    for k, v in subs.items():
        out = out.replace("{{" + k + "}}", v)
    return out


def main():
    builders = {"index": page_home, "people": page_people, "research": page_research, "collab": page_collab,
                "software": page_software, "teaching": page_teaching, "join": page_join, "contact": page_contact}
    sections, first = [], None
    for n in SITE["nav"]:
        p = builders[n["page"]]()
        first = first or p
        body = p["main"]
        if n["page"] != "index":
            body = body.replace("<h1>", "<h2>", 1).replace("</h1>", "</h2>", 1)
        sid = "home" if n["page"] == "index" else n["page"]
        sections.append(f'<section class="page-section" id="{sid}">{body}</section>')
    page = {"title": first["title"], "desc": first["desc"], "main": "\n".join(sections), "page": "index"}
    (ROOT / "index.html").write_text(render(page), encoding="utf-8")
    print("wrote index.html")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                      f"<url><loc>{SITE['site_url']}</loc></url></urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['site_url']}sitemap.xml\n", encoding="utf-8")
    print("wrote sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
