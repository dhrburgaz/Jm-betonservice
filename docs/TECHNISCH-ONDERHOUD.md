# JM Betonservice — technisch onderhoud en preview

## Huidige bronstructuur
De actuele GitHub Pages-preview is een statische Astro-export, **geen oorspronkelijke Astro-broncode**. De basiswebsite is opgeslagen in twee gesplitste ZIP-delen:
- `JM_Betonservice_V83_preview_deel1.part`
- `JM_Betonservice_V83_preview_deel2.part`

De workflow `.github/workflows/preview-pages.yml` reconstrueert deze ZIP en zet de HTML en assets in `_site`. Vervolgens worden de bewerkingen in onderstaande volgorde uitgevoerd:
1. `scripts/patch-preview.py` — contactfooter, WhatsApp en mobiele navigatie.
2. `scripts/finish-preview.py` — privacy, formulier en fotoselectie.
3. `scripts/expand-about.py` — bestaande Over ons-pagina uitbreiden.
4. `scripts/smoke-preview.py` — links, routes, alt-teksten, headings, IDs, privacy, veiligheid en JS-syntax.
5. `scripts/test-form-controller.mjs` — WhatsApp-fallback, formuliercontrole, fotolimits en foutafhandeling.

**Pas niet handmatig uitsluitend de gegenereerde `_site` aan:** die map wordt bij iedere build overschreven. De oude `jm-gh-pages.zip` staat ook in de repository, maar wordt niet door de actieve workflow gebruikt. Verwijder of vervang de ZIP-delen niet zonder een gecontroleerde bronmigratie.

## Veilig wijzigen en testen
Maak wijzigingen op een branch en open een pull request. `.github/workflows/qa-preview.yml` bouwt dan de preview en voert de statische controles en gedragstests uit **zonder live publicatie**. Controleer de uitslag en merge pas na een geslaagde run. De actieve Pages-workflow test opnieuw voordat hij publiceert.

## Formulier en foto's
Zonder `JM_FORM_ENDPOINT` opent de website na validatie een vooraf ingevuld WhatsApp-bericht. De bezoeker moet het bericht **zelf verzenden**. Foto's worden in die modus **niet automatisch meegestuurd**. Op ondersteunde apparaten kunnen bezoekers de foto's via het deelmenu apart delen; anders voegen ze ze in WhatsApp toe.

De fotoselectie accepteert maximaal 5 afbeeldingen (JPG, PNG, WebP, HEIC of HEIF), maximaal 8 MB per foto en 10 MB totaal. De browsercontrole is slechts gebruiksgemak, **geen beveiligde servercontrole**. Wanneer een echte formulierontvanger wordt aangesloten, controleer dan server-side bestandstype, grootte en malware, toegang tot uploads, bewaartermijnen, spambeveiliging, e-mailbezorging en privacyverklaring. Test de echte aflevering end-to-end voordat je een ontvangstbevestiging toont.

## SEO en lancering
De preview is bewust niet voor zoekmachines bedoeld: HTML gebruikt `noindex, nofollow`, `robots.txt` blokkeert crawlers en de sitemap is leeg. Bij de definitieve domeinlancering moet dit gecontroleerd worden aangepast, met echte canonicals, sitemap en Search Console.

## Beperkingen
Automatische GitHub-tests tonen **geen echte mobiele browserweergave** en bewijzen niet dat WhatsApp-berichten of serverformulieren daadwerkelijk zijn afgeleverd. Doe vóór live klantoplevering een visuele test op telefoon en desktop en een echte testaanvraag, met toestemming en zonder echte persoonsgegevens in testlogs.
