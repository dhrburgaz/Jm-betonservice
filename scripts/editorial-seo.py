from pathlib import Path
import sys, json, re, html
from xml.sax.saxutils import escape
root=Path(sys.argv[1])
cfg=json.loads("{\"common\":{\"Zuid-Holland, Zeeland en richting Amsterdam\":\"Zuid-Holland, Zeeland en de regio Amsterdam\",\"De website wordt als statische preview aangeboden via GitHub Pages.\":\"De website wordt gehost via GitHub Pages.\",\"Deze preview is niet bedoeld voor gepersonaliseerde advertenties.\":\"Deze website gebruikt geen gepersonaliseerde advertenties.\",\"door deze afrondingspatch geen analyse- of marketingcookies toegevoegd.\":\"geen analyse- of marketingcookies door JM Betonservice geplaatst.\",\"Een zakelijk e-mailadres wordt toegevoegd zodra dit is ingericht.\":\"U kunt ook mailen naar <a href=\\\"mailto:info@jmbetonservice.nl\\\">info@jmbetonservice.nl</a>.\",\"KvK 67385524<a href=\\\"tel:+31648381164\\\" style=\\\"display:block\\\">06 48 38 11 64</a>\":\"KvK 67385524<a href=\\\"tel:+31648381164\\\" style=\\\"display:block\\\">06 48 38 11 64</a><a href=\\\"mailto:info@jmbetonservice.nl\\\" style=\\\"display:block;overflow-wrap:anywhere\\\">info@jmbetonservice.nl</a>\"},\"per\":{\"index.html\":{\"Uw vloer strak afgewerkt. Uw beton zorgvuldig hersteld.\":\"Strakke vloeren. Vakkundig betonherstel.\",\"Een nieuwe gietvloer, uw balkon laten aanpakken of beschadigd beton laten herstellen? JM Betonservice denkt met u mee over de mogelijkheden. Met 16 jaar praktijkervaring.\":\"JM Betonservice is uw specialist in gietvloeren, balkonafwerking en betonreparatie. Met 16 jaar praktijkervaring verzorgen wij vloer- en betonwerk voor woningen en bedrijven.\",\"Uw balkon aanpakken\":\"Balkonrenovatie\",\"Een strakke vloer die past bij uw ruimte, wensen en dagelijks gebruik.\":\"Een naadloze vloerafwerking, afgestemd op uw interieur en dagelijks gebruik.\",\"JM Betonservice is een jong bedrijf met veel praktijkervaring in vloer- en betonwerk. Wij bespreken wat bij uw situatie past.\":\"Bij JM Betonservice combineren we 16 jaar praktijkervaring met aandacht voor de ondergrond, voorbereiding en afwerking.\",\"We leggen uit welke werkzaamheden mogelijk zijn.\":\"U krijgt advies over de voorbereiding, afwerking of reparatie.\",\"Vertel ons over uw klus. Wij denken met u mee.\":\"Een nieuw vloer- of betonproject?\",\"Een nieuwe vloer, een balkon dat aandacht nodig heeft of beschadigd beton? Neem contact op en vertel kort wat er speelt.\":\"Vraag een offerte aan voor uw vloer, balkon of betonreparatie. Stuur een korte omschrijving en foto's van de huidige situatie.\"},\"over-ons/index.html\":{\"Een jong bedrijf. Gebouwd op 16 jaar praktijkervaring.\":\"16 jaar vakervaring in vloer- en betonwerk.\",\"Vakervaring als uitgangspunt\":\"Vakmanschap begint bij de ondergrond\",\"We helpen de vraag duidelijk te krijgen voordat het werk wordt besproken.\":\"Wij adviseren over de afwerking in relatie tot belasting, onderhoud en planning.\",\"We leggen uit welke werkzaamheden relevant kunnen zijn, welke informatie nog nodig is en waarom een bepaalde aanpak afhangt van de situatie.\":\"U krijgt uitleg over de voorgestelde voorbereiding, materialen en afwerking, zodat u weet waarvoor u kiest.\"},\"diensten/balkoncoatings/index.html\":{\"Uw balkonvloer weer netjes afgewerkt\":\"Balkonrenovatie en balkoncoatings\",\"We doen geen algemene toezegging dat iedere coating automatisch een balkon waterdicht of veilig maakt.\":\"Waterdichtheid en veiligheid vragen om beoordeling van de volledige balkonopbouw, niet alleen de afwerklaag.\"},\"diensten/betonreparatie/index.html\":{\"Betonreparatie begint bij het begrijpen van de schade\":\"Betonreparatie voor beschadigd beton\",\"Daarna bespreken we of en hoe JM Betonservice kan helpen.\":\"Zo kunnen wij gericht adviseren over de benodigde beoordeling en herstelwerkzaamheden.\"},\"bedrijven/index.html\":{\"Een vloer voor uw bedrijf. Passend bij het gebruik.\":\"Bedrijfsvloeren voor werkplaatsen en bedrijfsruimtes.\",\"Dat helpt bij het gesprek over de mogelijkheden.\":\"Zo kunnen wij de vereiste eigenschappen van de vloer beoordelen.\"},\"werkwijze/index.html\":{\"Een duidelijke aanpak, van eerste vraag tot voorstel.\":\"Van eerste contact naar een duidelijk voorstel.\",\"Aan de hand van de informatie kan worden besproken welke voorbereiding en afwerking passend kunnen zijn.\":\"Wij adviseren over de voorbereiding van de ondergrond en de passende afwerking.\"},\"contact/index.html\":{\"Aanvragen verlopen momenteel via WhatsApp. U kunt ons wel bellen om uw klus te bespreken.\":\"Vraag een offerte aan via WhatsApp of mail rechtstreeks naar <a href=\\\"mailto:info@jmbetonservice.nl\\\">info@jmbetonservice.nl</a>. Telefonisch overleggen kan ook.\",\"Zodra een formulierontvanger is aangesloten, kunnen de foto's met het formulier worden meegestuurd.\":\"U kunt uw foto's ook als bijlage mailen naar info@jmbetonservice.nl.\"},\"projecten/index.html\":{\"De foto's geven een indruk van uiteenlopende werkzaamheden.\":\"Bekijk voorbeelden van vloerafwerking, balkonwerk en voorbereiding van de ondergrond.\"}},\"titles\":{\"index.html\":[\"Gietvloeren, balkonrenovatie & betonreparatie | JM Betonservice\",\"Gietvloeren, balkonrenovatie en betonreparatie in Zuid-Holland, Zeeland en regio Amsterdam. 16 jaar praktijkervaring. Vraag uw offerte aan.\"],\"diensten/gietvloeren/index.html\":[\"Gietvloer laten aanbrengen | JM Betonservice\",\"Gietvloeren voor woningen en bedrijven in Zuid-Holland, Zeeland en regio Amsterdam. Advies over ondergrond, voorbereiding en afwerking.\"],\"diensten/balkoncoatings/index.html\":[\"Balkonrenovatie & balkoncoating | JM Betonservice\",\"Balkonvloer renoveren of coaten? JM Betonservice adviseert over voorbereiding, herstel en afwerking in Zuid-Holland, Zeeland en regio Amsterdam.\"],\"diensten/betonreparatie/index.html\":[\"Betonreparatie & betonherstel | JM Betonservice\",\"Betonschade, scheuren of beschadigde betonranden? Bespreek betonreparatie met JM Betonservice in Zuid-Holland, Zeeland en regio Amsterdam.\"],\"bedrijven/index.html\":[\"Bedrijfsvloeren & epoxyvloeren | JM Betonservice\",\"Vloerafwerking voor werkplaatsen, garages en bedrijfsruimtes. Actief in Zuid-Holland, Zeeland en regio Amsterdam. Vraag een zakelijke offerte aan.\"],\"contact/index.html\":[\"Offerte aanvragen | JM Betonservice\",\"Vraag een offerte aan voor gietvloeren, balkonrenovatie of betonreparatie. Bel 06 48 38 11 64 of mail info@jmbetonservice.nl.\"]}}")
origin="https://www.jmbetonservice.nl/"
urls=[]
for p in sorted(root.rglob("*.html")):
    rel=p.relative_to(root).as_posix()
    s=p.read_text(encoding="utf-8")
    for old,new in {**cfg["common"],**cfg["per"].get(rel,{})}.items():
        s=s.replace(old,new)
    if rel in cfg["titles"]:
        title,description=map(html.escape,cfg["titles"][rel])
        s=re.sub(r"<title>.*?</title>",lambda m:f"<title>{title}</title>",s,count=1)
        for key,value in [("description",description),("og:title",title),("og:description",description)]:
            attr="property" if key.startswith("og:") else "name"
            s=re.sub(fr'<meta {attr}="{key}" content="[^"]*">',lambda m:f'<meta {attr}="{key}" content="{value}">',s,count=1)
    if rel not in {"404.html","bedankt/index.html"}:
        url=origin+("" if rel=="index.html" else rel.removesuffix("index.html"))
        s=s.replace('<meta name="robots" content="noindex, nofollow">','<meta name="robots" content="index, follow">')
        s=re.sub(r'<link rel="canonical"[^>]*>','',s)
        s=re.sub(r'<meta property="og:url"[^>]*>','',s)
        s=s.replace("</head>",f'<link rel="canonical" href="{url}"><meta property="og:url" content="{url}"></head>',1)
        urls.append(url)
    p.write_text(s,encoding="utf-8")
(root/"robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: "+origin+"sitemap.xml\n",encoding="utf-8")
(root/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+escape(u)+'</loc></url>' for u in urls)+'</urlset>\n',encoding="utf-8")
assert len(urls)>=20
assert "info@jmbetonservice.nl" in (root/"contact/index.html").read_text()
assert "afrondingspatch" not in (root/"privacy/index.html").read_text()
print(f"Editorial and SEO update: {len(urls)} indexable routes")


# Confirmed business identity and local SEO (2026-11-25).
# The registered address is not advertised as a walk-in location.
business = {
    "@context": "https://schema.org",
    "@type": "HomeAndConstructionBusiness",
    "@id": origin + "#business",
    "name": "JM Betonservice",
    "url": origin,
    "telephone": "+31648381164",
    "email": "info@jmbetonservice.nl",
    "vatID": "NL002210676B47",
    "identifier": {"@type": "PropertyValue", "propertyID": "KvK", "value": "67385524"},
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Admiraalsplein 209",
        "postalCode": "3317 BD",
        "addressLocality": "Dordrecht",
        "addressRegion": "Zuid-Holland",
        "addressCountry": "NL"
    },
    "areaServed": ["Dordrecht", "Zuid-Holland", "Zeeland", "Regio Amsterdam"],
    "description": "Gietvloeren, balkonrenovatie en betonreparatie vanuit Dordrecht."
}
business_lines = (
    '<span style="display:block">Btw: NL002210676B47</span>'
    '<span style="display:block">Admiraalsplein 209</span>'
    '<span style="display:block">3317 BD Dordrecht</span>'
)
footer_anchor = 'JM Betonservice · KvK 67385524'
contact_anchor = '<p class="contact-meta">Actief in Zuid-Holland, Zeeland en de regio Amsterdam.</p>'
contact_details = (
    '<p class="contact-meta">Gevestigd in Dordrecht. Actief in Zuid-Holland, Zeeland en de regio Amsterdam.</p>'
    '<p class="contact-meta"><strong>Bedrijfsgegevens</strong><br>JM Betonservice<br>'
    'Admiraalsplein 209<br>3317 BD Dordrecht<br>KvK 67385524<br>Btw: NL002210676B47<br>'
    '<a href="mailto:info@jmbetonservice.nl" style="overflow-wrap:anywhere">info@jmbetonservice.nl</a></p>'
)
privacy_anchor = 'KvK-nummer: <strong>67385524</strong>.'
privacy_details = (
    privacy_anchor + ' Btw-nummer: NL002210676B47. '
    'Adres: Admiraalsplein 209, 3317 BD Dordrecht, Nederland. '
    'E-mail: <a href="mailto:info@jmbetonservice.nl">info@jmbetonservice.nl</a>.'
)
local_meta = {
    "index.html": ("Gietvloeren & betonreparatie Dordrecht | JM Betonservice",
        "JM Betonservice in Dordrecht: gietvloeren, balkonrenovatie en betonreparatie in Zuid-Holland, Zeeland en regio Amsterdam. Vraag uw offerte aan."),
    "contact/index.html": ("Contact & offerte | JM Betonservice Dordrecht",
        "Contact met JM Betonservice in Dordrecht voor gietvloeren, balkonrenovatie en betonreparatie. Bel 06 48 38 11 64 of mail info@jmbetonservice.nl."),
    "over-ons/index.html": ("Over JM Betonservice Dordrecht | 16 jaar praktijkervaring",
        "JM Betonservice uit Dordrecht heeft 16 jaar praktijkervaring in gietvloeren, coatings en betonwerk voor woningen en bedrijven.")
}
count = 0
for page in sorted(root.rglob("*.html")):
    rel = page.relative_to(root).as_posix()
    source = page.read_text(encoding="utf-8")
    assert source.count(footer_anchor) == 1, f"Business footer missing or duplicated: {rel}"
    source = source.replace(footer_anchor, footer_anchor + business_lines, 1)
    if rel == "contact/index.html":
        assert source.count(contact_anchor) == 1, "Contact address insertion point changed"
        source = source.replace(contact_anchor, contact_details, 1)
    if rel == "privacy/index.html":
        assert source.count(privacy_anchor) == 1, "Privacy identity insertion point changed"
        source = source.replace(privacy_anchor, privacy_details, 1)
    if rel in local_meta:
        title, desc = map(html.escape, local_meta[rel])
        source, n = re.subn(r"<title>.*?</title>", lambda m: f"<title>{title}</title>", source, count=1)
        assert n == 1, rel
        for key, value in [("description", desc), ("og:title", title), ("og:description", desc)]:
            attr = "property" if key.startswith("og:") else "name"
            source, n = re.subn(fr'<meta {attr}="{key}" content="[^"]*">', lambda m: f'<meta {attr}="{key}" content="{value}">', source, count=1)
            assert n == 1, (rel, key)
    if rel == "index.html":
        schema = json.dumps(business, ensure_ascii=False)
        assert json.loads(schema)["address"]["postalCode"] == "3317 BD"
        assert 'id="jm-business-schema"' not in source
        source = source.replace("</head>", '<script type="application/ld+json" id="jm-business-schema">' + schema + "</script></head>", 1)
    assert "NL002210676B47" in source and "Admiraalsplein 209" in source, rel
    page.write_text(source, encoding="utf-8")
    count += 1
assert count >= 20
print(f"Business identity verified on {count} HTML pages; local metadata and business JSON-LD generated.")
