# JM Betonservice — projectstatus

## Productie op 24 november 2026

- GitHub Pages levert HTTPS via `www.jmbetonservice.nl` en leidt het hoofddomein door naar `www`. Deployment [45419162089](https://github.com/dhrburgaz/Jm-betonservice/actions/runs/45419162089) is geslaagd op publicatiecommit `c18b0b8`.
- Live crawl met `scripts/check-live.py` slaagde voor 37 bereikbare URL's en 287 bestanden. Robots staat indexering toe en verwijst naar de sitemap met 20 URL's. De contactcanonical is `https://www.jmbetonservice.nl/contact/`.
- De live contactcontroller heeft een lege endpoint. Hij bereidt WhatsApp voor. De bezoeker verstuurt het bericht en eventuele foto's zelf. De code en site vermelden `info@jmbetonservice.nl`, `+31 6 48381164` en KvK `67385524`. Vestigingsadres en btw-nummer blijven onbevestigd. Het MX-record wijst naar STRATO. Werkelijke mailboxontvangst moet nog worden bewezen.

## Offerteontvangst

- [Concept-PR 3](https://github.com/dhrburgaz/Jm-betonservice/pull/3) bevat een Cloudflare Worker, koppeling aan de bestaande controller, tests en een activeringsprocedure. Beide lokale buildmodi slaagden voor 22 gegenereerde HTML-routes. De ontvangertest gebruikt synthetische data en gesimuleerde Turnstile- en Resend-antwoorden. Chromium verifieerde echte multipart-overdracht met foto naar de ontvangercode, herstel na netwerk- en providerfouten en blokkade van dubbele submit. Wrangler heeft de Worker in een dry-run gebundeld.
- Voor activering zijn Cloudflare- en Resend-beheer, DNS-verificatie van het afzendersubdomein en GitHub Actions-variablebeheer nodig. De huidige GitHub-integratie kan de Actions-variabelen niet lezen (HTTP 403). De website gebruikt intussen de bestaande WhatsApp-route.
- Eerstvolgende oplevercriterium is een synthetische aanvraag met en zonder foto in de zakelijke inbox, inclusief herhaalde poging en controle van de verwerkingsafspraken. Zie [Offerteontvanger](docs/OFFERTEONTVANGER.md).

## Overige oplevering

- De GSC Wizard-connector weigert Search Console- en GA4-inzage zonder actief abonnement. Controleer rechtstreeks vanuit de Google-eigenaarssessie de sitemapverwerking, het bedrijfsprofiel en eventuele analytics en conversiemeting. De gecontroleerde live homepage en contactpagina bevatten geen GA4- of Google Tag Manager-script. Het [Google-overdrachtsdocument](docs/COMMERCIELE-OPLEVERING.md) bevat de bestaande voorbereiding. Meet een bevestigde offerte apart van contactklikken.
- Rond mobiele fysieke toesteltests, toetsenbordcontrole, Lighthouse en inhoudelijke controle van dienstclaims af. Gebruik de huidige commerciële positionering, werkfoto’s en huisstijl als uitgangspunt.
