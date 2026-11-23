# JM Betonservice — oplevering nieuw domein en zakelijke e-mail

Status: **voorbereid, niet geactiveerd**. Deze checklist mag pas worden afgesloten na een echte test op het definitieve domein. Er is op dit moment geen bevestigde domeinnaam, mailboxnaam of provider in dit project.

## 1. Domein & GitHub Pages
1. Vraag de exacte domeinnaam en het beheerpaneel van de DNS-provider op. Gebruik geen voorbeeldnaam als feit.
2. Kies een canonieke host (apex of `www`) en stel de Custom domain-instelling in GitHub Pages in. De DNS-records moeten overeenkomen met de **actuele GitHub Pages-documentatie**; voorkom dubbele of conflicterende A, AAAA en CNAME-records.
3. Wacht op domeincontrole en geldig HTTPS-certificaat; schakel 'Enforce HTTPS' in zodra beschikbaar.
4. **Bouwbasis aanpassen:** deze preview is gebouwd onder `/Jm-betonservice/`. Bij een eigen domein moeten alle interne links, CSS/JS/assets, redirects, canonicals en de Pages-buildbase consequent op `/` worden gezet. Alleen een CNAME instellen is onvoldoende. Doe dit in een afzonderlijke geteste migratie, niet als globale tekstvervanging op de live export.
5. Controleer op het echte domein: 200 voor homepage en alle dienstpagina's; werkende afbeeldingen, fonts, menu, knoppen, mobiele navigatie, 404 en contactformulier.

## 2. Zakelijke e-mail
1. Verifieer de **exacte** mailbox en provider, en of de inbox berichten ontvangt en verstuurt.
2. Zet de door de mailprovider verstrekte MX-, SPF-, DKIM- en DMARC-records correct in DNS. Neem geen voorbeeldrecords over en zorg dat SPF niet dubbel wordt gepubliceerd.
3. Verstuur een test van een extern e-mailadres en antwoord vanuit de nieuwe mailbox. Controleer ook ongewenste e-mail.
4. Plaats het bevestigde e-mailadres in de footer, contactpagina en privacyverklaring pas wanneer ontvangst is getest.

## 3. Offerteformulier en foto's
1. Op dit moment gebruikt de website WhatsApp als fallback. Daarbij gaat **geen** foto automatisch mee en wordt geen offerte automatisch gemaild.
2. Selecteer eerst een betrouwbare formulierdienst of eigen beveiligde backend die multipart-foto's accepteert. Een zakelijke mailbox op zichzelf is geen upload-API.
3. Verifieer de verwerkingsovereenkomst, locatie van gegevensopslag, toegangsbeheer, bewaartermijn, spambeveiliging, rate limiting en anti-malwarebeleid.
4. Controleer server-side bestandsgrootte, aantal, daadwerkelijke MIME/signature, toegestane types, scan en veilige opslag; clientvalidatie is niet voldoende.
5. Stel pas na dit onderzoek de publieke variabele `JM_FORM_ENDPOINT` in via GitHub Actions variables. Voeg geen geheim token, API-key of wachtwoord in HTML of publieke buildvariabelen toe.
6. Test met fictieve contactgegevens en toegestane testfoto's: verzenden, ontvangst, foutscenario, mobiele upload, herhaalde verzending, spam en bevestiging. De site mag pas "verzonden" tonen als de ontvanger dit betrouwbaar bevestigt.
7. Werk privacyverklaring en contactuitleg gelijktijdig bij naar de **werkelijk gebruikte** verwerker en bewaartermijn.

## 4. SEO (uitsluitend bij definitieve lancering)
- Verwijder `noindex, nofollow` en de blokkerende preview-`robots.txt` **pas na** URL-migratie en volledige QA.
- Genereer een sitemap met de **werkelijke** canonieke HTTPS-URL's en unieke titles/metabeschrijvingen.
- Verifieer de definitieve property in Google Search Console en dien de sitemap in.
- Controleer lokale bedrijfsgegevens, structured data en of claims over diensten/ervaring kloppen.

## 5. Echte release-gate
- [ ] Domein en mailadres bevestigd, DNS/SSL en mailbox live getest
- [ ] Alle 22+ routes en afbeeldingen gecontroleerd op eigen domein
- [ ] Responsive visuele review: iPhone, Android, desktop; geen overlappende elementen
- [ ] Formulier met en zonder foto end-to-end ontvangen
- [ ] Privacytekst bijgewerkt voor werkelijke provider en uploads
- [ ] Redirects, sitemap, robots, canonicals en Search Console gecontroleerd
- [ ] GitHub QA geslaagd en goedgekeurde ontwerptaal behouden

Totdat dit is afgerond: behoud de preview als preview en de transparante WhatsApp-fallback. Verwar een succesvolle GitHub Actions-test niet met een geverifieerde aflevering van een echte klantaanvraag.
