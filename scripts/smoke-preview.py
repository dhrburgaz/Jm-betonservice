#!/usr/bin/env python3
"""Static post-build QA for the existing JM Betonservice preview."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import sys

root=Path(sys.argv[1] if len(sys.argv)>1 else "_site").resolve()
base="/Jm-betonservice/"
pages=sorted(root.rglob("*.html"))
problems=[]
links=0
assets=0

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items=[]
    def handle_starttag(self,tag,attrs):
        data=dict(attrs)
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
if 'data-form-enabled="true"' not in contact:problems.append("contact: form not enabled")
if "<fieldset disabled>" in contact:problems.append("contact: fieldset still disabled")
if 'id="jm-contact-handoff-status"' not in contact:problems.append("contact: status note missing")
if 'data-submit>Ga verder via WhatsApp' not in contact:problems.append("contact: CTA missing")
if 'class="todo-note"' in privacy or "Nog in te vullen vóór publicatie" in privacy:
    problems.append("privacy: placeholder remains")
for heading in ("Wie verantwoordelijk is","Welke gegevens we ontvangen","Waarom we die gebruiken",
                "Rechtsgrond","Met wie we gegevens delen","Hoe lang we gegevens bewaren",
                "Beveiliging","Rechten van betrokkenen","Contact over privacy",
                "Cookies en statistieken","Wijzigingen"):
    if f"<h2>{heading}</h2>" not in privacy:problems.append("privacy: missing "+heading)
if len(pages)<20:problems.append(f"unexpected page count {len(pages)}")
print(f"JM QA: {len(pages)} HTML routes, {links} anchor links, {assets} asset references checked")
if problems:
    print("JM QA FAILED:")
    for issue in problems[:50]:print(" -",issue)
    raise SystemExit(1)
print("JM QA PASS: internal targets, contact markup, 11 privacy sections, business footer.")
