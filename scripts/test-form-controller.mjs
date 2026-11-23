import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';

// Dependency-free browser-behavior checks against the ACTUAL generated controller.
const page=fs.readFileSync(process.argv[2] ?? '_site/contact/index.html','utf8');
const match=page.match(/<script id="jm-final-contact-script">([\s\S]*?)<\/script>/);
assert.ok(match,'Contact controller is missing');
// Exercise the WhatsApp fallback even if a form endpoint is configured later.
const code=match[1].replace(/var endpoint=.*?;/, 'var endpoint="";');
class Element {
  constructor(value=''){this.value=value;this.hidden=true;this.textContent='';this.children=[];this.files=[];this.attrs={};this.style={};this.classList={toggle(){}};}
  addEventListener(name,callback){this[`on_${name}`]=callback;}
  focus(){this.focused=true;}
  setAttribute(name,value){this.attrs[name]=value;}
  removeAttribute(name){delete this.attrs[name];}
  replaceChildren(){this.children=[];}
  append(...nodes){this.children.push(...nodes);}
  appendChild(node){this.children.push(node);return node;}
  replaceWith(){}
}
async function scenario(values={},photos=[],canShare=()=>false){
  const fields=Object.fromEntries(Object.entries(values).map(([k,v])=>[k,new Element(v)]));
  const fileInput=new Element();fileInput.files=photos;fields['jm-fotos']=fileInput;
  const button=new Element();const status=new Element();const summary=new Element();const errors=new Element();
  const uploadFeedback=new Element();const photoPreviews=new Element();const shareButton=new Element();
  const fieldset=new Element();fieldset.disabled=true;
  const form={noValidate:false,elements:{namedItem:n=>fields[n]??null},
    querySelector(selector){return {'fieldset':fieldset,'[data-submit]':button,'[data-error-summary]':summary,'[data-error-list]':errors,'[data-fail]':new Element(),'[data-busy]':new Element()}[selector]??null;},
    querySelectorAll(){return []},addEventListener(n,cb){this[`on_${n}`]=cb;}};
  const ids={'jm-fotos':fileInput,'jm-file-feedback':uploadFeedback,'jm-photo-previews':photoPreviews,'jm-share-photos':shareButton,'jm-contact-handoff-status':status};
  const locations=[];
  const ctx={
    document:{querySelector:n=>n==='form.lead-form'?form:null,querySelectorAll:()=>[],getElementById:id=>ids[id]??null,createElement:()=>new Element(),addEventListener(){}},
    window:{addEventListener(){},location:{assign:u=>locations.push(u)}},
    navigator:{share:async()=>{},canShare},
    URL:{createObjectURL:()=>`blob:fake`,revokeObjectURL(){}},
    FormData:class {get(){return '';}},
    RadioNodeList:class{},
  };
  vm.runInNewContext(code,ctx,{timeout:1000});
  assert.equal(form.noValidate,true,'native validation must not suppress custom errors');
  assert.equal(fieldset.disabled,false,'form must be enabled');
  assert.ok(form.on_submit,'submit listener must exist');
  await form.on_submit({preventDefault(){},stopImmediatePropagation(){}});
  return {locations,status,summary,errors,uploadFeedback,shareButton,photoPreviews};
}
const valid={naam:'Test Klant',plaats:'Dordrecht',dienst:'Gietvloer',omschrijving:'Vloer behandelen',telefoon:'0612345678'};
let r=await scenario();
assert.equal(r.locations.length,0,'blank form cannot proceed');
assert.equal(r.summary.hidden,false,'blank form must show custom error summary');
assert.ok(r.errors.children.length>=4,'blank form must show field errors');
r=await scenario(valid);
assert.equal(r.locations.length,1,'valid WhatsApp form must open message');
assert.ok(r.locations[0].includes('wa.me/31648381164'));
r=await scenario({...valid,email:'bad-email'});
assert.equal(r.locations.length,0,'malformed email must be rejected');
r=await scenario(valid,[{name:'evil.jpg',type:'image/svg+xml',size:1000}]);
assert.match(r.uploadFeedback.textContent,/uitsluitend afbeeldingen/,'disguised SVG must be rejected');
assert.equal(r.locations.length,0,'rejected SVG cannot proceed');
assert.equal(r.photoPreviews.children.length,0,'rejected SVG must not be previewed');
r=await scenario(valid,[{name:'project.jpg',type:'image/jpeg',size:1000}],()=>{throw new Error('Share API unsupported')});
assert.ok(r.status.textContent.includes('nog niet verzonden'),'photo should not be claimed as sent');
assert.equal(r.shareButton.hidden,true,'unsupported sharing must be hidden');
r=await scenario(valid,Array.from({length:6},(_,i)=>({name:`foto${i}.jpg`,type:'image/jpeg',size:1000})));
assert.match(r.uploadFeedback.textContent,/maximaal 5/);
r=await scenario(valid,[{name:'groot.jpg',type:'image/jpeg',size:9*1024*1024}]);
assert.match(r.uploadFeedback.textContent,/groter dan 8 MB/);
console.log('JM controller behavior PASS: blank form, valid WhatsApp, email, SVG, share errors, photo count and size.');
