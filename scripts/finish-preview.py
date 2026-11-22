#!/usr/bin/env python3
"""Finalize legal/contact information on the existing JM Betonservice V8.3 static preview.

Conservative post-build patch. No redesign. Independent of a domain or mailbox.
An optional public HTTPS form endpoint can be supplied via JM_FORM_ENDPOINT.
"""
from pathlib import Path
import html
import json
import os
import re
import sys
from urllib.parse import urlparse

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
base = "/Jm-betonservice/"
endpoint = os.environ.get("JM_FORM_ENDPOINT", "").strip()
if endpoint:
    u = urlparse(endpoint)
    if u.scheme != "https" or not u.netloc or u.username or u.password:
        raise ValueError("JM_FORM_ENDPOINT must be a public HTTPS submission URL, not a secret.")

privacy_sections = {
    "Wie verantwoordelijk is": (
        "<p>JM Betonservice is verantwoordelijk voor de persoonsgegevens die u rechtstreeks "
        "met het bedrijf deelt. KvK-nummer: <strong>67385524</strong>. "
        "U kunt contact opnemen via <a href=\"tel:+31648381164\">06 48 38 11 64</a>.</p>"
    ),
    "Welke gegevens we ontvangen": (
        "<p>Als u contact opneemt of een offerte voorbereidt, kunt u uw naam, telefoonnummer, "
        "e-mailadres, plaats of postcode, gewenste dienst, projectomschrijving en eventuele "
        "aanvullende projectgegevens invullen. Zakelijke bezoekers kunnen ook bedrijfsnaam en "
        "informatie over de ruimte toevoegen. Wij vragen geen volledig adres voor een eerste aanvraag.</p>"
    ),
    "Waarom we die gebruiken": (
        "<p>Wij gebruiken deze gegevens om contact met u op te nemen, uw vraag te beoordelen, "
        "een eventuele offerte te bespreken en afspraken over werkzaamheden te maken. "
        "Wij gebruiken uw aanvraaggegevens niet automatisch voor nieuwsbrieven of advertenties.</p>"
    ),
    "Rechtsgrond": (
        "<p>De verwerking is nodig om op uw verzoek stappen te ondernemen voordat een "
        "overeenkomst wordt gesloten. Voor het beantwoorden van gewone vragen kan ook ons "
        "gerechtvaardigd belang bij zakelijke communicatie van toepassing zijn. "
        "Wettelijke administratieverplichtingen worden afzonderlijk nageleefd.</p>"
    ),
    "Met wie we gegevens delen": (
        "<p>De website wordt als statische preview aangeboden via GitHub Pages. De hostingpartij "
        "kan technische gegevens verwerken om de site te leveren en te beveiligen. "
        "Kiest u voor aanvragen via WhatsApp, dan opent WhatsApp een bericht met de door u "
        "ingevoerde informatie. <strong>U beslist zelf of u dat bericht daadwerkelijk verzendt.</strong> "
        "Voor het gebruik van WhatsApp geldt daarnaast het privacybeleid van WhatsApp. "
        "Zodra een aparte formulier- en e-maildienst wordt aangesloten, passen wij deze "
        "verklaring aan op die daadwerkelijk gebruikte dienst.</p>"
    ),
    "Hoe lang we gegevens bewaren": (
        "<p>Wij bewaren ontvangen contact- en offertegegevens niet langer dan nodig voor de "
        "behandeling van de aanvraag en eventuele vervolgafspraken. Als gegevens onderdeel "
        "worden van een administratie waarvoor wettelijke bewaarplichten gelden, bewaren "
        "wij die gedurende de toepasselijke wettelijke termijn.</p>"
    ),
    "Beveiliging": (
        "<p>De website gebruikt een beveiligde HTTPS-verbinding. Wij beperken de toegang tot "
        "ontvangen aanvragen tot personen die deze voor hun werkzaamheden nodig hebben. "
        "De beveiliging van externe communicatiekanalen is mede afhankelijk van die dienst.</p>"
    ),
    "Rechten van betrokkenen": (
        "<p>U kunt vragen om inzage, verbetering, verwijdering of beperking van uw "
        "persoonsgegevens. Ook kunt u waar van toepassing bezwaar maken of uw gegevens "
        "opvragen voor overdracht. Niet elk verzoek kan worden uitgevoerd wanneer een "
        "wettelijke bewaarplicht geldt. U kunt ook een klacht indienen bij de "
        "<a href=\"https://autoriteitpersoonsgegevens.nl/\" target=\"_blank\" rel=\"noopener noreferrer\">"
        "Autoriteit Persoonsgegevens</a>.</p>"
    ),
    "Contact over privacy": (
        "<p>Voor vragen over persoonsgegevens of een verzoek betreffende uw privacy kunt u "
        "JM Betonservice bellen op <a href=\"tel:+31648381164\">06 48 38 11 64</a>. "
        "Een zakelijk e-mailadres wordt toegevoegd zodra dit is ingericht.</p>"
    ),
    "Cookies en statistieken": (
        "<p>Deze preview is niet bedoeld voor gepersonaliseerde advertenties. Er worden "
        "door deze afrondingspatch geen analyse- of marketingcookies toegevoegd. "
        "Wanneer later een statistiek- of advertentiedienst wordt geactiveerd, beoordelen "
        "wij vooraf welke cookie-informatie en toestemming vereist zijn.</p>"
    ),
    "Wijzigingen": (
        "<p>Deze verklaring is bijgewerkt op 22 november 2026. Wanneer contactkanalen, "
        "formulieren of verwerkingsdiensten veranderen, werken wij deze informatie bij.</p>"
    ),
}

style = """<style id="jm-final-contact-style">
.jm-legal-details{font-size:.86rem;line-height:1.6;margin:.65rem 0 0;opacity:.88}
.jm-contact-note{font-size:.92rem;line-height:1.55;margin:.8rem 0}
.jm-contact-status{padding:1rem;margin-top:1rem;border:1px solid currentColor;border-radius:8px}
.doc-text p{margin:0 0 .6rem;line-height:1.75}

/* Refined warm card edges and responsive information presentation. */
.cards .card,.svc-list .svc-row,.info-box,.pricebox,.form-card,.article__side{
  border:1px solid rgba(83,66,54,.15);
  border-radius:clamp(12px,1.25vw,18px);
  box-shadow:0 4px 18px rgba(55,38,29,.045);
  min-width:0;
}
.cards .card{transition:box-shadow .18s ease,transform .18s ease,border-color .18s ease;overflow:hidden}
.cards .card:hover{transform:translateY(-2px);border-color:rgba(133,55,45,.28);box-shadow:0 10px 26px rgba(55,38,29,.09)}
.card__body,.svc-row>* ,.form-card>*,.info-box>*{min-width:0}
.card__body p,.svc-row p,.info-box p{overflow-wrap:break-word}
.info-box,.pricebox{overflow:hidden}
.info-box h2,.pricebox h2{max-width:100%;text-wrap:balance}
.doc-section{padding:clamp(.8rem,2vw,1.15rem) 0;border-bottom:1px solid rgba(83,66,54,.13)}
.doc-section:last-child{border-bottom:0}
.doc-text a{overflow-wrap:anywhere}
.jm-table-scroll{max-width:100%;overflow-x:auto;overscroll-behavior-x:contain;border:1px solid rgba(83,66,54,.16);border-radius:12px}
.jm-table-scroll table{border-collapse:separate;border-spacing:0;width:100%;min-width:400px}
.jm-table-scroll th,.jm-table-scroll td{padding:clamp(.65rem,1.4vw,1rem);vertical-align:top;text-align:left;border-bottom:1px solid rgba(83,66,54,.14)}
.jm-table-scroll th{background:rgba(149,105,77,.075);font-weight:700}
.jm-table-scroll tr:last-child td{border-bottom:0}
.jm-upload-card{padding:clamp(1rem,2.2vw,1.4rem);border:1px dashed rgba(115,74,63,.45);background:#fbf9f5;border-radius:14px;margin:1.1rem 0}
.jm-upload-card:focus-within{outline:2px solid #8c453e;outline-offset:2px}
.jm-upload-card label{display:block;font-weight:700;margin-bottom:.45rem}
.jm-upload-card input[type=file]{display:block;width:100%;max-width:100%;padding:.5rem 0;font:inherit}
.jm-upload-card .hint{font-size:.88rem;line-height:1.55;margin:.25rem 0 .8rem;color:#61574e}
.jm-upload-feedback{display:block;font-size:.9rem;line-height:1.5;overflow-wrap:anywhere;margin:.5rem 0}
.jm-photo-previews{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,125px),1fr));gap:.7rem;margin-top:.8rem}
.jm-photo-item{display:flex;flex-direction:column;gap:.35rem;min-width:0;padding:.4rem;background:#fff;border:1px solid rgba(90,70,55,.14);border-radius:10px}
.jm-photo-item img{display:block;max-width:100%;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:6px}
.jm-photo-name{font-size:.78rem;line-height:1.3;overflow-wrap:anywhere;color:#4c4139}
.jm-upload-error{color:#a12727;font-weight:600}
@media(max-width:480px){.jm-upload-card{padding:.85rem}.jm-photo-previews{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(prefers-reduced-motion:reduce){.cards .card{transition:none}.cards .card:hover{transform:none}}
</style>"""

# The inline controller uses the existing fields and layout, with no third-party JS library.
# WhatsApp is a transparent user-controlled handoff until an email endpoint exists.
controller = r'''<script id="jm-final-contact-script">
(function(){
  "use strict";
  var form=document.querySelector("form.lead-form");
  if(!form) return;
  var endpoint=__JM_FORM_ENDPOINT__;
  var waNumber="31648381164";
  var mainFields=form.querySelector("fieldset");
  function enable(){ if(mainFields) mainFields.disabled=false; }
  enable();
  document.addEventListener("DOMContentLoaded",enable);
  window.addEventListener("load",enable);

  var button=form.querySelector("[data-submit]");
  var status=document.getElementById("jm-contact-handoff-status");
  var summary=form.querySelector("[data-error-summary]");
  var errorList=form.querySelector("[data-error-list]");
  var originalFail=form.querySelector("[data-fail]");
  var originalBusy=form.querySelector("[data-busy]");
  if(originalFail) originalFail.hidden=true;
  if(originalBusy) originalBusy.hidden=true;
  if(button) button.textContent=endpoint ? "Verstuur mijn aanvraag" : "Ga verder via WhatsApp";


  // In-memory photo selection. No personal files are stored or uploaded at this stage.
  var photoInput=document.getElementById("jm-fotos");
  var photoFeedback=document.getElementById("jm-file-feedback");
  var photoPreviews=document.getElementById("jm-photo-previews");
  var photoUrls=[];
  var photoValid=true;
  var MAX_FILES=5,MAX_TOTAL=10*1024*1024,MAX_ONE=8*1024*1024;
  var allowedExt=/\.(jpe?g|png|webp|heic|heif)$/i;
  function clearPreviews(){
    photoUrls.forEach(function(url){URL.revokeObjectURL(url);});
    photoUrls=[];
    if(photoPreviews)photoPreviews.replaceChildren();
  }
  function selectedPhotos(){
    return photoInput?Array.from(photoInput.files||[]):[];
  }
  function refreshPhotos(){
    clearPreviews();
    var photos=selectedPhotos();
    var size=photos.reduce(function(sum,file){return sum+file.size;},0);
    var issue="";
    if(photos.length>MAX_FILES)issue="Selecteer maximaal 5 foto's.";
    else if(photos.some(function(f){return f.size>MAX_ONE;}))issue="Een foto is groter dan 8 MB.";
    else if(size>MAX_TOTAL)issue="De geselecteerde foto's zijn samen groter dan 10 MB.";
    else if(photos.some(function(f){return !(f.type.startsWith("image/")||allowedExt.test(f.name));}))
      issue="Selecteer uitsluitend afbeeldingen (JPG, PNG, WebP of HEIC).";
    photoValid=!issue;
    if(photoFeedback){
      photoFeedback.textContent=issue||(photos.length?photos.length+" foto('s) geselecteerd ("+(size/(1024*1024)).toFixed(1)+" MB).":"Nog geen foto's geselecteerd.");
      photoFeedback.classList.toggle("jm-upload-error",!!issue);
    }
    photos.slice(0,MAX_FILES).forEach(function(file){
      if(!photoPreviews)return;
      var item=document.createElement("div");
      item.className="jm-photo-item";
      var src=URL.createObjectURL(file);
      photoUrls.push(src);
      var img=document.createElement("img");
      img.src=src;
      img.alt="Voorbeeld: "+file.name;
      img.loading="lazy";
      img.onerror=function(){img.replaceWith(document.createTextNode("Afbeeldingsvoorbeeld niet beschikbaar"));};
      var name=document.createElement("span");
      name.className="jm-photo-name";
      name.textContent=file.name;
      item.append(img,name);
      photoPreviews.appendChild(item);
    });
    return photoValid;
  }
  if(photoInput)photoInput.addEventListener("change",refreshPhotos);
  // Preserve table semantics while allowing horizontal scrolling on narrow screens.
  document.querySelectorAll("main table").forEach(function(table){
    if(table.closest(".jm-table-scroll"))return;
    var wrap=document.createElement("div");
    wrap.className="jm-table-scroll";
    wrap.tabIndex=0;
    wrap.setAttribute("role","region");
    wrap.setAttribute("aria-label","Horizontaal scrollbare tabel");
    table.parentNode.insertBefore(wrap,table);
    wrap.appendChild(table);
  });

  function feedback(message,isError){
    if(!status) return;
    status.textContent=message;
    status.hidden=false;
    status.style.borderColor=isError?"#a42424":"#315e42";
    status.focus();
  }
  function field(name){return form.elements.namedItem(name);}
  function val(name){
    var f=field(name);
    if(!f)return "";
    if(f instanceof RadioNodeList) return String(f.value||"").trim();
    return String(f.value||"").trim();
  }
  function validate(){
    var faults=[];
    if(!refreshPhotos()) faults.push(["jm-fotos","Controleer uw foto's."]);
    if(!val("naam")) faults.push(["naam","Vul uw naam in."]);
    if(!val("plaats")) faults.push(["plaats","Vul de plaats van de klus in."]);
    if(!val("dienst")) faults.push(["dienst","Kies een dienst."]);
    if(!val("omschrijving")) faults.push(["omschrijving","Beschrijf uw klus."]);
    if(!val("telefoon")&&!val("email")) faults.push(["telefoon","Vul een telefoonnummer of e-mailadres in."]);
    var email=val("email");
    if(email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) faults.push(["email","Controleer uw e-mailadres."]);
    var tel=val("telefoon");
    if(tel && !/^[+0-9\s().-]{6,30}$/.test(tel)) faults.push(["telefoon","Controleer het telefoonnummer."]);
    Array.from(form.querySelectorAll("[aria-invalid]")).forEach(function(f){f.removeAttribute("aria-invalid");});
    if(errorList)errorList.textContent="";
    faults.forEach(function(e){
      var f=field(e[0]);
      if(f && f.setAttribute) f.setAttribute("aria-invalid","true");
      if(errorList){var li=document.createElement("li");li.textContent=e[1];errorList.appendChild(li);}
    });
    if(summary){summary.hidden=faults.length===0; if(faults.length) summary.focus();}
    if(faults.length){var first=field(faults[0][0]);if(first&&first.focus)first.focus();}
    return faults.length===0;
  }
  var names={
    doelgroep:"Aanvrager",naam:"Naam",telefoon:"Telefoon",email:"E-mail",
    plaats:"Plaats/postcode",dienst:"Werkzaamheden",bedrijfsnaam:"Bedrijf",
    type_ruimte:"Type ruimte",ondergrond:"Huidige ondergrond",
    gebruik_vloer:"Gebruik vloer",omschrijving:"Projectomschrijving",
    gewenste_periode:"Gewenste planning",oppervlakte:"Oppervlakte"
  };

  form.addEventListener("submit",async function(event){
    event.preventDefault();
    event.stopImmediatePropagation();
    enable();
    if(!validate())return;
    var photos=selectedPhotos();
    var data=new FormData(form);
    var bot=String(data.get("bot-field")||"").trim();
    if(bot){feedback("Controleer uw gegevens en probeer het opnieuw.",true);return;}
    if(endpoint){
      // FormSubmit attachments require a native multipart POST, not the AJAX route.
      if(/^https:\/\/formsubmit\.co\//i.test(endpoint)){
        var nativeEndpoint=endpoint.replace("formsubmit.co/ajax/","formsubmit.co/");
        feedback("Uw aanvraag en eventuele foto's worden naar de formulierdienst verstuurd.",false);
        form.action=nativeEndpoint;
        form.method="POST";
        form.enctype="multipart/form-data";
        // Native submission includes the file input without serializing it in a URL.
        HTMLFormElement.prototype.submit.call(form);
        return;
      }
      if(button)button.disabled=true;
      feedback("Uw aanvraag en eventuele foto's worden verzonden…",false);
      try{
        var response=await fetch(endpoint,{method:"POST",body:data,headers:{"Accept":"application/json"}});
        if(!response.ok)throw new Error("Formulierdienst reageert met status "+response.status);
        var result=await response.json().catch(function(){return null;});
        if(!result || !(result.success===true||result.success==="true"||result.accepted===true||result.ref))
          throw new Error("Ontvanger heeft de aanvraag niet bevestigd.");
        feedback("Uw aanvraag is door de formulierdienst geaccepteerd. Wij nemen contact met u op.",false);
        form.reset();
        refreshPhotos();
      }catch(err){
        feedback("Verzenden is niet gelukt. Uw gegevens staan nog in het formulier. Probeer opnieuw of bel ons.",true);
      }finally{if(button)button.disabled=false;}
      return;
    }
    var lines=["Offerteaanvraag via website JM Betonservice",""];
    Object.keys(names).forEach(function(key){
      var value=val(key);
      if(value)lines.push(names[key]+": "+value);
    });
    var message=lines.join("\n");
    if(message.length>3000){
      feedback("Uw projectomschrijving is te lang voor een WhatsApp-link. Verkort de tekst enigszins en probeer opnieuw.",true);
      return;
    }
    var url="https://wa.me/"+waNumber+"?text="+encodeURIComponent(message);
    if(photos.length){
      feedback("Uw foto's zijn geselecteerd maar nog niet verzonden. WhatsApp kan deze websitebestanden niet automatisch bijvoegen. Voeg de foto's in WhatsApp zelf toe nadat u de tekst heeft verstuurd.",false);
      var continueLink=document.createElement("a");
      continueLink.className="btn btn--primary";
      continueLink.href=url;
      continueLink.target="_blank";
      continueLink.rel="noopener noreferrer";
      continueLink.textContent="Open WhatsApp en voeg foto's toe";
      status.appendChild(document.createElement("p")).appendChild(continueLink);
      return;
    }
    feedback("WhatsApp wordt geopend met uw ingevulde aanvraag. Controleer het bericht en druk daar zelf op Verzenden; uw aanvraag is nog niet automatisch verstuurd.",false);
    window.location.assign(url);
  },true);
})();
</script>'''

pages=sorted(root.rglob("*.html"))
if len(pages)<20:
    raise RuntimeError("Onverwacht weinig gegenereerde HTML-pagina's: "+str(len(pages)))

footer_anchor = '<h2><a class="jm-footer-contact" href="/Jm-betonservice/contact/">Contact</a></h2>'
footer_replacement = (footer_anchor +
    '<p class="jm-legal-details">JM Betonservice · KvK 67385524'
    '<a href="tel:+31648381164" style="display:block">06 48 38 11 64</a></p>')
footer_count=0
for path in pages:
    source=path.read_text(encoding="utf-8")
    if 'id="jm-final-contact-style"' in source:
        raise RuntimeError("Finalization applied twice: "+str(path))
    if footer_anchor not in source:
        raise RuntimeError("Expected footer not found: "+str(path))
    source=source.replace(footer_anchor,footer_replacement,1)
    footer_count+=1
    source=source.replace("</head>",style+"</head>",1)
    path.write_text(source,encoding="utf-8")

privacy_file=root/"privacy/index.html"
if not privacy_file.is_file():
    raise RuntimeError("Privacy page missing")
source=privacy_file.read_text(encoding="utf-8")
source,count=re.subn(r'<div class="draft-banner"><div class="container"><p>.*?</p></div></div>',"",source,count=1,flags=re.S)
if count!=1: raise RuntimeError("Privacy preview banner structure changed.")
for title,body in privacy_sections.items():
    pattern=r'(<div class="doc-section"><h2>'+re.escape(title)+r'</h2>)<div class="todo-note">.*?</div>(</div>)'
    source,count=re.subn(pattern,lambda m:m.group(1)+'<div class="doc-text">'+body+'</div>'+m.group(2),source,count=1,flags=re.S)
    if count!=1:raise RuntimeError("Privacy section missing: "+title)
if "Nog in te vullen" in source:raise RuntimeError("Privacy still contains todo.")
privacy_file.write_text(source,encoding="utf-8")

contact_file=root/"contact/index.html"
if not contact_file.is_file():raise RuntimeError("Contact page missing")
source=contact_file.read_text(encoding="utf-8")
if 'class="lead-form"' not in source or 'data-form-enabled="false"' not in source:
    raise RuntimeError("Unexpected lead form.")
source=source.replace('data-form-enabled="false"','data-form-enabled="true"',1)
source=source.replace('action="/Jm-betonservice/bedankt/"','action="#"',1)
source=source.replace('data-netlify="true"','',1)
source=source.replace('data-netlify-honeypot="bot-field"','',1)
source=source.replace('<fieldset disabled>','<fieldset>',1)
source=source.replace(
    '<div class="upload" aria-disabled="true"><p class="upload__title">Foto van de huidige situatie <span class="opt">(optioneel)</span></p><p class="hint">Een foto maakt uw situatie makkelijker te beoordelen. Foto toevoegen is nog niet beschikbaar: eventuele foto\'s kunt u later met ons delen.</p><button class="btn btn--secondary" type="button" disabled>Foto toevoegen</button></div>',
    '''<div class="jm-upload-card" data-photo-upload>
       <label for="jm-fotos">Foto's van de huidige situatie <span class="opt">(optioneel)</span></label>
       <p class="hint" id="jm-upload-hint">Kies maximaal 5 foto's (JPG, PNG, WebP of HEIC), samen maximaal 10 MB. Bekijk uw selectie hieronder. Bij een aanvraag via WhatsApp moet u de foto's zelf nog toevoegen. Zodra een formulierontvanger is aangesloten, kunnen de foto's met het formulier worden meegestuurd.</p>
       <input type="file" name="attachment" id="jm-fotos" accept="image/*,.heic,.heif" multiple aria-describedby="jm-upload-hint jm-file-feedback">
       <output id="jm-file-feedback" class="jm-upload-feedback" aria-live="polite">Nog geen foto's geselecteerd.</output>
       <div class="jm-photo-previews" id="jm-photo-previews" aria-label="Voorbeeld geselecteerde foto's"></div>
    </div>''',
    1
)
source=source.replace(
    'We gebruiken uw gegevens uitsluitend om contact op te nemen over uw aanvraag. Lees onze',
    'We gebruiken uw gegevens om uw aanvraag te behandelen. Zonder ingeschakelde formulierontvanger opent de aanvraag in WhatsApp. Geselecteerde foto’s worden daarbij niet automatisch meegestuurd; u voegt deze zelf toe. Lees onze ',
    1
)
source=source.replace('Online aanvragen is nog niet ingeschakeld','Aanvragen verlopen momenteel via WhatsApp')
source=source.replace('<button class="btn btn--primary" type="submit" data-submit>Verstuur mijn aanvraag</button>',
    '<button class="btn btn--primary" type="submit" data-submit>Ga verder via WhatsApp</button>',1)
if 'data-submit>Ga verder via WhatsApp' not in source:
    raise RuntimeError("Submit button not found")
source=source.replace('</form>','<p class="jm-contact-status" id="jm-contact-handoff-status" role="status" aria-live="polite" tabindex="-1" hidden></p></form>',1)
source=source.replace('</body>',controller.replace('__JM_FORM_ENDPOINT__',json.dumps(endpoint,ensure_ascii=False))+'</body>',1)
contact_file.write_text(source,encoding="utf-8")

print(f"JM finalization: {footer_count} footers, 11 privacy sections, 1 functional contact form.")
print("JM form mode:", "HTTPS provider endpoint configured" if endpoint else "user-confirmed WhatsApp handoff")
