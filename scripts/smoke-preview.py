#!/usr/bin/env python3
"""Static post-build QA for the existing JM Betonservice preview."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else "_site").resolve()
base=sys.argv[2] if len(sys.argv)>2 else "/Jm-betonservice/"
pages=sorted(root.rglob("*.html"))
problems=[]
links=0
assets=0

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items=[]
        self.ids=[]
        self.h1_count=0
        self.title_count=0
        self.images_without_alt=0
        self.page_anchors=[]
    def handle_starttag(self,tag,attrs):
        data=dict(attrs)
        if data.get("id"): self.ids.append(data["id"])
        if tag=="h1": self.h1_count+=1
        if tag=="title": self.title_count+=1
        if tag=="img" and "alt" not in data: self.images_without_alt+=1
        if tag=="a" and data.get("href","").startswith("#") and data.get("href")!="#":
            self.page_anchors.append(unquote(data["href"][1:]))
        if tag=="a" and data.get("href") is not None:
            self.items.append(("link",data["href"]))
        if tag in {"script","img","source","link"}:
            src=data.get("src") or data.get("href")
            if src and tag!="link" or (tag=="link" and data.get("rel") and "stylesheet" in data["rel"]):
                self.items.append(("asset",src))

for page in pages:
    rel=page.relative_to(root).as_posix()
    current="https://preview.invalid"+base+("" if rel=="index.html" else rel.removesuffix("index.html"))
    source=page.read_text(encoding="utf-8")
    parser=PageParser()
    parser.feed(source)
    if parser.h1_count!=1:problems.append(f"{rel}: expected one H1, found {parser.h1_count}")
    if parser.title_count!=1:problems.append(f"{rel}: expected one title, found {parser.title_count}")
    if len(parser.ids)!=len(set(parser.ids)):problems.append(f"{rel}: duplicate HTML IDs")
    if parser.images_without_alt:problems.append(f"{rel}: {parser.images_without_alt} images missing alt")
    for anchor in parser.page_anchors:
        if anchor not in parser.ids:problems.append(f"{rel}: broken same-page anchor #{anchor}")
    if 'id="jm-final-contact-style"' not in source or "KvK 67385524" not in source:
        problems.append(f"{rel}: legal footer/style missing")
    for typ,href in parser.items:
        if typ=="link":links+=1
        else:assets+=1
        href=href.strip()
        if not href or href.startswith("#"):continue
        if href.startswith(("mailto:","tel:","https://wa.me/","data:")):continue
        dest=urlsplit(urljoin(current,href))
        if dest.scheme not in {"http","https"}:continue
        if dest.netloc!="preview.invalid":continue
        if not dest.path.startswith(base):
            problems.append(f"{rel}: link outside preview base: {href}")
            continue
        inside=unquote(dest.path[len(base):])
        if ".." in Path(inside).parts:
            problems.append(f"{rel}: unsafe relative path: {href}")
            continue
        target=(root/inside)
        if target.is_dir() or inside.endswith("/"):
            target=target/"index.html"
        if not target.exists():
            problems.append(f"{rel}: missing target {href}")

contact=(root/"contact/index.html").read_text(encoding="utf-8")
privacy=(root/"privacy/index.html").read_text(encoding="utf-8")
if 'id="jm-final-contact-script"' not in contact:problems.append("contact: handoff script missing")
if "form.noValidate=true;" not in contact:problems.append("contact: custom validation not activated")
if "allowedTypes=" not in contact or "canShareFiles(" not in contact:
    problems.append("contact: strict photo validation and safe sharing missing")
if 'accept="image/jpeg,image/png,image/webp,image/heic,image/heif,.heic,.heif"' not in contact:
    problems.append("contact: file picker must restrict supported image formats")
if 'data-form-enabled="true"' not in contact:problems.append("contact: form not enabled")
if "<fieldset disabled>" in contact:problems.append("contact: fieldset still disabled")
if 'id="jm-contact-handoff-status"' not in contact:problems.append("contact: status note missing")
if 'data-submit>Ga verder via WhatsApp' not in contact:problems.append("contact: CTA missing")

if 'id="jm-fotos"' not in contact or 'type="file"' not in contact:
    problems.append("contact: photo selector missing")
if 'id="jm-photo-previews"' not in contact:
    problems.append("contact: photo previews missing")
if 'maximaal 5 foto' not in contact.lower():
    problems.append("contact: photo limits not displayed")
if '.cards .card:hover' not in contact:
    problems.append("style: refined card styling missing")
# Parse the new inline controller syntax using Node available on the GitHub Actions runner.
import subprocess
import re
scripts = re.findall(r'<script id="jm-final-contact-script">(.*?)</script>', contact, flags=re.S)
if len(scripts) != 1:
    problems.append("contact: exactly one final controller required")
else:
    check = subprocess.run(["node","--check"],input=scripts[0],text=True,capture_output=True)
    if check.returncode:
        problems.append("contact: controller syntax error: "+check.stderr[:250])

if 'class="todo-note"' in privacy or "Nog in te vullen vóór publicatie" in privacy:
    problems.append("privacy: placeholder remains")
for heading in ("Wie verantwoordelijk is","Welke gegevens we ontvangen","Waarom we die gebruiken",
                "Rechtsgrond","Met wie we gegevens delen","Hoe lang we gegevens bewaren",
                "Beveiliging","Rechten van betrokkenen","Contact over privacy",
                "Cookies en statistieken","Wijzigingen"):
    if f"<h2>{heading}</h2>" not in privacy:problems.append("privacy: missing "+heading)
if len(pages)<20:problems.append(f"unexpected page count {len(pages)}")
about=(root/"over-ons/index.html").read_text(encoding="utf-8")
for section in ("jm-about-expanded","jm-about-approach","jm-about-clients","jm-about-method-title","jm-about-expansion-styles"):
    if section not in about:
        problems.append("over-ons: missing expanded section "+section)
if "16 jaar praktijkervaring" not in about:
    problems.append("over-ons: correct experience claim missing")

print(f"JM QA: {len(pages)} HTML routes, {links} anchor links, {assets} asset references checked")
if problems:
    print("JM QA FAILED:")
    for issue in problems[:50]:print(" -",issue)
    raise SystemExit(1)
print("JM QA PASS: internal targets, contact markup, 11 privacy sections, business footer.")
