#!/usr/bin/env python3
"""Gerichte JM Betonservice V8.3 websitecorrecties tijdens de Pages-deployment."""
from pathlib import Path
from urllib.parse import quote
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
old_footer = ('<h2>Contact</h2><ul>'
              '<li><a class="footer-tel" href="tel:+31648381164">Bel 06 48 38 11 64</a></li>'
              '<li><a href="/Jm-betonservice/contact/">Offerte aanvragen</a></li></ul>')
new_footer = '<h2><a class="jm-footer-contact" href="/Jm-betonservice/contact/">Contact</a></h2>'
message = "Goedendag, ik heb uw website bekeken en wil graag meer informatie of een vrijblijvende offerte aanvragen."
wa_url = "https://wa.me/31648381164?text=" + quote(message)

# Officieel WhatsApp-symbool (Simple Icons): vector wordt lokaal in HTML opgenomen.
icon = ("M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z")
css = """<style id="jm-contact-fixes">
.site-footer .jm-footer-contact{color:inherit;text-decoration:none;display:inline-block}
.site-footer .jm-footer-contact:hover{text-decoration:underline;text-underline-offset:4px}
.site-footer .jm-footer-contact:focus-visible,.jm-whatsapp:focus-visible,.jm-whatsapp-inline:focus-visible{outline:3px solid #1754c8;outline-offset:4px}
.jm-whatsapp{position:fixed;z-index:55;right:calc(20px + env(safe-area-inset-right));bottom:calc(20px + env(safe-area-inset-bottom));width:58px;height:58px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:#25d366;color:#fff;border:2px solid #fff;box-shadow:0 6px 24px rgba(0,0,0,.22);text-decoration:none;transition:transform .15s ease,box-shadow .15s ease}
.jm-whatsapp svg{width:32px;height:32px;fill:currentColor;display:block}
.jm-whatsapp:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(0,0,0,.3)}
.jm-whatsapp-inline{display:none}
@media(max-width:767px){
  .jm-whatsapp{display:none}
  .jm-whatsapp-inline{display:inline-flex;align-items:center;min-height:44px;text-decoration:underline;text-underline-offset:3px}
  .form-notice .jm-whatsapp-inline{margin-inline-start:12px}
}
@media(min-width:768px) and (max-width:1199px){body:has(.mobile-bar:not([hidden])) .jm-whatsapp{bottom:calc(96px + env(safe-area-inset-bottom))}body:has(.primary-nav[data-open="true"]) .jm-whatsapp{visibility:hidden;pointer-events:none}}
@media(prefers-reduced-motion:reduce){.jm-whatsapp{transition:none}}
</style>"""
button = (f'<a class="jm-whatsapp" href="{wa_url}" target="_blank" rel="noopener noreferrer" '
          'aria-label="Stuur JM Betonservice een WhatsApp-bericht" title="Contact via WhatsApp">'
          f'<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"><path d="{icon}"/></svg></a>')

inline_link = (f'<a class="jm-whatsapp-inline" href="{wa_url}" target="_blank" '
               'rel="noopener noreferrer">Contact via WhatsApp</a>')

pages = sorted(root.rglob("*.html"))
header_js = root / "_astro/Header.astro_astro_type_script_index_0_lang.BpPdg-ut.js"
if len(pages) < 10 or not header_js.is_file():
    raise RuntimeError("De V8.3-export heeft een onverwachte structuur.")

# Op mobiel blokkeerde deze handler de gewone 'Diensten'-link.
# De aparte pijltjesknop houdt zijn functie om het submenu te tonen.
js = header_js.read_text(encoding="utf-8")
start = js.find("o.querySelector(")
end = js.find("}),", start) + 3
intercept = js[start:end]
if start < 0 or end < start or "n.preventDefault()" not in intercept or "data-view" not in intercept:
    raise RuntimeError("De verwachte Diensten-handler is gewijzigd; handmatige controle vereist.")
header_js.write_text(js[:start] + js[end:], encoding="utf-8")

for page in pages:
    html = page.read_text(encoding="utf-8")
    if html.count(old_footer) != 1 or html.count("</head>") != 1 or html.count("</body>") != 1:
        raise RuntimeError(f"Onverwachte footer- of HTML-structuur: {page}")
    if "jm-contact-fixes" in html or 'class="jm-whatsapp"' in html:
        raise RuntimeError(f"Dubbele wijziging voorkomen: {page}")
    html = html.replace(old_footer, new_footer + inline_link, 1)
    if page.relative_to(root).as_posix() == "contact/index.html":
        form_start = '</div><form class="lead-form"'
        if html.count(form_start) != 1:
            raise RuntimeError("De start van het contactformulier is gewijzigd.")
        html = html.replace(form_start, inline_link + form_start, 1)
    html = html.replace("</head>", css + "</head>", 1)
    html = html.replace("</body>", button + "</body>", 1)
    page.write_text(html, encoding="utf-8")

print(f"Contact, WhatsApp en mobiele Dienstennavigatie bijgewerkt op {len(pages)} pagina's.")
