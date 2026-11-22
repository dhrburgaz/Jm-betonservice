#!/usr/bin/env python3
"""Expand the approved JM Betonservice About page without redesigning the website."""
from pathlib import Path
import html
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
page = root / "over-ons" / "index.html"
if not page.is_file():
    raise RuntimeError("JM Over ons-pagina ontbreekt.")

source = page.read_text(encoding="utf-8")
if 'id="jm-about-expanded"' in source:
    raise RuntimeError("Over ons-uitbreiding is al toegepast.")

# Reuse an existing authentic work photo from the built Astro export.
photos = list((root / "_astro").glob("F40.*.webp"))
if not photos:
    raise RuntimeError("Echte projectfoto F40 ontbreekt; geen fictieve afbeelding gebruiken.")
photo = max(photos, key=lambda p: p.stat().st_size)
photo_src = "/Jm-betonservice/_astro/" + photo.name
photo_src = html.escape(photo_src, quote=True)

new_hero = (
    '<h1 id="page-title">Een jong bedrijf. Gebouwd op 16 jaar praktijkervaring.</h1>'
    '<p class="lead">JM Betonservice werkt aan vloeren, coatings, balkons en betonwerk '
    'voor particulieren en bedrijven. Met aandacht voor de bestaande ondergrond, '
    'het gebruik van de ruimte en een afwerking die bij het project past.</p>'
)
source, n = re.subn(
    r'<h1 id="page-title">Een jong bedrijf met 16 jaar praktijkervaring\.</h1>'
    r'<p class="lead">.*?</p>',
    lambda _: new_hero, source, count=1, flags=re.S
)
if n != 1:
    raise RuntimeError("De bestaande Over ons-hero is veranderd.")

body = f"""
<section class="section jm-about" id="jm-about-expanded" aria-labelledby="jm-about-intro">
  <div class="container">
    <div class="jm-about-intro">
      <div class="jm-about-story">
        <p class="eyebrow">WIE WE ZIJN</p>
        <h2 id="jm-about-intro">Vakervaring als uitgangspunt</h2>
        <p>JM Betonservice is een jong bedrijf met <strong>16 jaar praktijkervaring</strong> in vloerafwerking en betonwerk. Die ervaring nemen we mee wanneer we met een klant bespreken wat er nodig is: van een nieuwe vloer in een woning tot de behandeling van een bedrijfsruimte of een balkon.</p>
        <p>Geen enkele ruimte is precies hetzelfde. Een mooie afwerking begint daarom met de juiste vragen. Hoe wordt het oppervlak gebruikt? Wat is de huidige ondergrond? Zijn er bestaande beschadigingen of vochtproblemen? Die informatie helpt om samen te kijken welke werkzaamheden passend kunnen zijn.</p>
        <p>We willen dat u begrijpt wat er wordt besproken. Ook als u niet precies weet welke vloer, coating of behandeling u nodig heeft, kunt u uw situatie gewoon aan ons voorleggen.</p>
      </div>
      <figure class="jm-about-photo">
        <img src="{photo_src}" alt="Werkzaamheden aan een binnenvloer" loading="lazy" decoding="async">
        <figcaption>Uit de praktijk: werkzaamheden aan een vloer.</figcaption>
      </figure>
    </div>
  </div>
</section>
<section class="section jm-about-values" aria-labelledby="jm-about-approach">
  <div class="container">
    <p class="eyebrow">ONZE AANPAK</p>
    <h2 id="jm-about-approach">Waar we op letten bij uw project</h2>
    <div class="jm-about-value-grid">
      <article class="jm-about-value">
        <span class="jm-about-value-number" aria-hidden="true">01</span>
        <h3>De ondergrond begrijpen</h3>
        <p>De staat van de bestaande vloer of het beton is belangrijk voor de keuze van de voorbereiding, afwerking of reparatie. Daarom kijken we niet alleen naar het gewenste eindbeeld.</p>
      </article>
      <article class="jm-about-value">
        <span class="jm-about-value-number" aria-hidden="true">02</span>
        <h3>Rekening houden met het gebruik</h3>
        <p>Een woonvloer, werkplaats en balkon stellen verschillende eisen. We bespreken de toepassing en de aandachtspunten voordat een passende oplossing kan worden gekozen.</p>
      </article>
      <article class="jm-about-value">
        <span class="jm-about-value-number" aria-hidden="true">03</span>
        <h3>Helder over de mogelijkheden</h3>
        <p>We leggen uit welke werkzaamheden relevant kunnen zijn, welke informatie nog nodig is en waarom een bepaalde aanpak afhangt van de situatie.</p>
      </article>
    </div>
  </div>
</section>
<section class="section jm-about-audiences" aria-labelledby="jm-about-clients">
  <div class="container">
    <p class="eyebrow">VOOR WIE WE WERKEN</p>
    <h2 id="jm-about-clients">Van woning tot bedrijfsruimte</h2>
    <div class="jm-about-audience-grid">
      <article class="jm-about-audience">
        <h3>Voor particulieren</h3>
        <p>Denkt u aan een gietvloer, een andere vloerafwerking of werk aan een balkon? We bespreken de wensen, de bestaande situatie en wat voor uw ruimte belangrijk is.</p>
        <a class="text-link" href="/Jm-betonservice/diensten/gietvloeren/">Bekijk gietvloeren</a>
      </article>
      <article class="jm-about-audience">
        <h3>Voor bedrijven</h3>
        <p>In een werkplaats, garage of bedrijfsruimte spelen gebruik, belasting, onderhoud en planning vaak een grote rol. We helpen de vraag duidelijk te krijgen voordat het werk wordt besproken.</p>
        <a class="text-link" href="/Jm-betonservice/bedrijven/">Bekijk onze zakelijke mogelijkheden</a>
      </article>
    </div>
  </div>
</section>
<section class="section jm-about-method" aria-labelledby="jm-about-method-title">
  <div class="container">
    <p class="eyebrow">VAN VRAAG TOT PLAN</p>
    <h2 id="jm-about-method-title">Zo begint een samenwerking</h2>
    <ol class="jm-about-method-list">
      <li><span aria-hidden="true">1</span><div><h3>Vertel over uw situatie</h3><p>Geef aan wat u wilt laten maken of herstellen. Een korte omschrijving, het soort ruimte en eventueel foto's helpen om uw vraag beter te begrijpen.</p></div></li>
      <li><span aria-hidden="true">2</span><div><h3>We bespreken de mogelijkheden</h3><p>De ondergrond, toepassing en eventuele aandachtspunten bepalen welke opties verder bekeken moeten worden. Soms is aanvullende informatie nodig.</p></div></li>
      <li><span aria-hidden="true">3</span><div><h3>We stemmen de vervolgstap af</h3><p>Op basis van de informatie bespreken we wat passend is en hoe het project verder kan worden voorbereid.</p></div></li>
    </ol>
    <p class="jm-about-area"><strong>Werkgebied:</strong> JM Betonservice is actief in Zuid-Holland, Zeeland en richting Amsterdam. Of uw project mogelijk is, bespreken we graag met u.</p>
    <div class="btn-row">
      <a class="btn btn--primary" href="/Jm-betonservice/contact/">Bespreek uw project</a>
      <a class="btn btn--secondary" href="/Jm-betonservice/diensten/">Bekijk alle diensten</a>
    </div>
  </div>
</section>
"""

pattern = (
    r'<section class="section"><div class="container">'
    r'<div class="doc-section"><h2>Goed werk begint met goed kijken</h2>.*?'
    r'</div></section>(?=<section class="section section--dark cta-band")'
)
source, n = re.subn(pattern, lambda _: body, source, count=1, flags=re.S)
if n != 1:
    raise RuntimeError("De bestaande Over ons-contentstructuur is gewijzigd.")

css = """
<style id="jm-about-expansion-styles">
.jm-about h2,.jm-about-values h2,.jm-about-audiences h2,.jm-about-method h2{max-width:22ch;text-wrap:balance}
.jm-about-intro{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);align-items:center;gap:clamp(1.5rem,5vw,4rem)}
.jm-about-story{min-width:0;max-width:68ch}
.jm-about-story p{line-height:1.8;max-width:66ch}
.jm-about-story p+p{margin-top:1rem}
.jm-about-photo{margin:0;min-width:0}
.jm-about-photo img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:16px;box-shadow:0 14px 35px rgba(47,32,24,.11)}
.jm-about-photo figcaption{font-size:.83rem;opacity:.78;margin-top:.55rem;line-height:1.45}
.jm-about-value-grid,.jm-about-audience-grid{display:grid;gap:clamp(1rem,2.4vw,1.5rem);margin-top:clamp(1.4rem,3.5vw,2rem)}
.jm-about-value-grid{grid-template-columns:repeat(3,minmax(0,1fr))}
.jm-about-audience-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
.jm-about-value,.jm-about-audience{min-width:0;padding:clamp(1.25rem,3vw,2rem);border:1px solid rgba(85,62,48,.16);background:#fff;border-radius:16px;box-shadow:0 5px 18px rgba(50,38,30,.05)}
.jm-about-value-number{display:block;font-size:.78rem;font-weight:700;letter-spacing:.12em;color:#9e4139;margin-bottom:1.2rem}
.jm-about-value h3,.jm-about-audience h3{margin-top:0;text-wrap:balance}
.jm-about-value p,.jm-about-audience p{line-height:1.72;overflow-wrap:break-word}
.jm-about-audience .text-link{display:inline-block;margin-top:.7rem}
.jm-about-method-list{list-style:none;margin:clamp(1rem,3vw,1.8rem) 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.3rem}
.jm-about-method-list>li{display:flex;align-items:flex-start;gap:1rem;min-width:0}
.jm-about-method-list>li>span{display:grid;place-items:center;flex:none;width:2.5rem;height:2.5rem;border:1px solid rgba(145,66,59,.35);border-radius:50%;color:#99493f;font-weight:700}
.jm-about-method-list h3{margin:.2rem 0 .45rem;text-wrap:balance}
.jm-about-method-list p{line-height:1.72;margin:0}
.jm-about-area{border-left:3px solid #a34d44;padding:.7rem 1rem;line-height:1.7;max-width:70ch;margin:2rem 0}
.jm-about-values{background:#f8f5f0}
.jm-about-method{background:#faf8f5}
@media(max-width:900px){.jm-about-intro{grid-template-columns:1fr}.jm-about-photo{max-width:620px}.jm-about-photo img{aspect-ratio:4/3}.jm-about-value-grid,.jm-about-method-list{grid-template-columns:1fr}}
@media(max-width:640px){.jm-about-audience-grid{grid-template-columns:1fr}.jm-about-value,.jm-about-audience{padding:1.2rem}.jm-about-photo img{aspect-ratio:5/4}.jm-about-method-list{gap:1.6rem}}
@media(prefers-reduced-motion:reduce){.jm-about *{scroll-behavior:auto}}
</style>
"""

if source.count("</head>") != 1:
    raise RuntimeError("Geen unieke HTML-head op Over ons.")
source = source.replace("</head>", css+"</head>", 1)
page.write_text(source, encoding="utf-8")
print("JM About expanded with evidence-based copy, 3 differentiators, 2 audiences, 3 steps and authentic project photo.")
