import { Buffer } from 'node:buffer';

const origin = 'https://www.jmbetonservice.nl';
const hostname = new URL(origin).hostname;
const recipient = 'info@jmbetonservice.nl';
const mb = 1024 * 1024;
const fields = {
  doelgroep: ['Aanvrager', 20], naam: ['Naam', 100], telefoon: ['Telefoon', 30],
  email: ['E-mail', 120], plaats: ['Plaats/postcode', 80], dienst: ['Werkzaamheden', 80],
  bedrijfsnaam: ['Bedrijf', 100], type_ruimte: ['Type ruimte', 100],
  ondergrond: ['Huidige ondergrond', 150], gebruik_vloer: ['Gebruik vloer', 200],
  omschrijving: ['Projectomschrijving', 2000], gewenste_periode: ['Planning', 100],
  oppervlakte: ['Oppervlakte', 40],
};
const services = new Set([
  'Gietvloer', 'Balkonvloer', 'Betonreparatie', 'Epoxyvloer / bedrijfsvloer',
  'Vloercoating', 'Egaliseren', 'Grindvloer', 'Injectiewerk / vocht', 'Ik weet het nog niet',
]);

function reply(status, body) {
  return new Response(body ? JSON.stringify(body) : null, {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store',
      'Access-Control-Allow-Origin': origin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Max-Age': '600',
      Vary: 'Origin',
    },
  });
}

function reject(status, message) {
  throw reply(status, { message });
}

async function readForm(request) {
  const maxBody = 10 * mb + 64 * 1024;
  if (Number(request.headers.get('Content-Length')) > maxBody) {
    reject(413, "Kies samen maximaal 10 MB aan foto's.");
  }
  const headers = { 'Content-Type': request.headers.get('Content-Type') ?? '' };
  if (!/^multipart\/form-data\s*;/i.test(headers['Content-Type']) || !request.body) {
    reject(415, 'Verstuur uw aanvraag via het offerteformulier.');
  }
  const reader = request.body.getReader();
  const chunks = [];
  let size = 0;
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > maxBody) reject(413, "Kies samen maximaal 10 MB aan foto's.");
      chunks.push(value);
    }
    return await new Response(new Blob(chunks), { headers }).formData();
  } catch (error) {
    if (error instanceof Response) throw error;
    reject(400, 'De aanvraag kon niet worden gelezen. Probeer opnieuw.');
  } finally {
    await reader.cancel().catch(() => {});
  }
}

function readText(data, key, max) {
  const values = data.getAll(key);
  const value = values[0] ?? '';
  if (values.length > 1 || typeof value !== 'string' || value.length > max) {
    reject(400, 'Controleer de ingevulde velden.');
  }
  return value.trim();
}

function imageType(bytes) {
  const head = String.fromCharCode(...bytes.subarray(0, 32));
  if (bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) return 'jpeg';
  if (head.startsWith('\x89PNG\r\n\x1a\n')) return 'png';
  if (head.startsWith('RIFF') && head.slice(8, 12) === 'WEBP') return 'webp';
  if (head.slice(4, 8) === 'ftyp') {
    if (/^(heic|heix|hevc|hevx)$/.test(head.slice(8, 12))) return 'heic';
    if (/^(mif1|msf1)$/.test(head.slice(8, 12))) return 'heif';
  }
}

async function readPhotos(data) {
  const entries = data.getAll('attachment');
  const files = entries.filter(file => !(file instanceof File && !file.name && !file.size));
  if (entries.length > 5 || files.some(file => !(file instanceof File) || !file.size || file.size > 8 * mb)
      || files.reduce((sum, file) => sum + file.size, 0) > 10 * mb) {
    reject(413, "Kies maximaal 5 foto's, maximaal 8 MB per foto en 10 MB samen.");
  }
  const attachments = [];
  for (const file of files) {
    const bytes = new Uint8Array(await file.arrayBuffer());
    const type = imageType(bytes);
    const extension = /\.([^.]+)$/.exec(file.name)?.[1].toLowerCase().replace(/^jpg$/, 'jpeg');
    const allowed = type && (type === extension || (
      ['heic', 'heif'].includes(type) && ['heic', 'heif'].includes(extension)
    ));
    if (!allowed || !['', 'application/octet-stream', 'image/' + type, 'image/' + extension].includes(file.type)) {
      reject(415, "Kies geldige foto's in JPG, PNG, WebP of HEIC/HEIF.");
    }
    attachments.push({ filename: 'projectfoto-' + (attachments.length + 1) + '.' + type, content: Buffer.from(bytes).toString('base64') });
  }
  return attachments;
}

async function handle(request, env) {
  if (new URL(request.url).pathname !== '/offerte') return reply(404);
  if (request.headers.get('Origin') !== origin) return reply(403);
  if (request.method === 'OPTIONS') return reply(204);
  if (request.method !== 'POST') return reply(405);

  const ip = request.headers.get('CF-Connecting-IP');
  if (!ip || !env.TURNSTILE_SECRET || !env.RESEND_API_KEY || !env.MAIL_FROM) {
    reject(503, 'Het formulier is tijdelijk niet beschikbaar.');
  }
  const limit = await env.QUOTE_LIMIT.limit({ key: ip });
  if (!limit.success) reject(429, 'Te veel pogingen. Wacht een minuut en probeer opnieuw.');

  const data = await readForm(request);
  const token = readText(data, 'cf-turnstile-response', 2048);
  const submission = readText(data, 'submission_id', 36);
  if (readText(data, 'bot-field', 200) || !token || !/^[0-9a-f-]{36}$/.test(submission)) {
    reject(400, 'Rond de beveiligingscontrole af en probeer opnieuw.');
  }

  const values = Object.fromEntries(Object.entries(fields).map(([name, [, max]]) => [name, readText(data, name, max)]));
  if (!values.naam || !values.plaats || !values.omschrijving || !services.has(values.dienst)
      || !['Particulier', 'Bedrijf'].includes(values.doelgroep) || (!values.email && !values.telefoon)
      || (values.email && !/^[^\s@,<>]+@[^\s@,<>]+\.[^\s@,<>]+$/.test(values.email))
      || (values.telefoon && !/^[+0-9\s().-]{6,30}$/.test(values.telefoon))) {
    reject(400, 'Controleer de verplichte velden en uw contactgegevens.');
  }

  const verification = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: token, remoteip: ip }),
    signal: AbortSignal.timeout(5000),
  });
  if (!verification.ok) reject(503, 'De beveiligingscontrole is tijdelijk niet beschikbaar.');
  const challenge = await verification.json();
  if (challenge.success !== true || challenge.hostname !== hostname || challenge.action !== 'offerte') {
    reject(400, 'De beveiligingscontrole is verlopen. Probeer opnieuw.');
  }

  const attachments = await readPhotos(data);
  const lines = Object.entries(fields).filter(([key]) => values[key])
    .map(([key, [label]]) => label + ': ' + values[key]);
  const text = ['Aanvraagkenmerk: ' + submission, ...lines].join('\n');
  const email = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: 'Bearer ' + env.RESEND_API_KEY,
      'Content-Type': 'application/json',
      'Idempotency-Key': 'jm-offerte/' + submission,
    },
    body: JSON.stringify({
      from: env.MAIL_FROM, to: [recipient],
      subject: 'Nieuwe websiteaanvraag JM Betonservice', text, attachments,
      ...(values.email && { reply_to: values.email }),
    }),
    signal: AbortSignal.timeout(12000),
  });
  if (!email.ok) reject(503, 'De aanvraag kon niet worden bevestigd. Probeer opnieuw of bel ons.');
  const accepted = await email.json();
  if (typeof accepted.id !== 'string' || !accepted.id) {
    reject(503, 'De aanvraag kon niet worden bevestigd. Probeer opnieuw of bel ons.');
  }
  return reply(202, { accepted: true, reference: submission });
}

export default {
  async fetch(request, env) {
    try {
      return await handle(request, env);
    } catch (error) {
      if (error instanceof Response) return error;
      return reply(503, { message: 'Het formulier is tijdelijk niet beschikbaar. Probeer opnieuw of bel ons.' });
    }
  },
};
