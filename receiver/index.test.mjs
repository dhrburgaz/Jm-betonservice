import assert from 'node:assert/strict';
import { test } from 'node:test';
import receiver from './index.mjs';

const origin = 'https://www.jmbetonservice.nl';
const ref = 'a3a4e258-4df3-4f6a-9119-7010dc9a4bd7';
const png = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/lZYAAAAASUVORK5CYII=';
const env = {
  TURNSTILE_SECRET: 'test-only',
  RESEND_API_KEY: 'test-only',
  MAIL_FROM: 'offerte@formulier.jmbetonservice.nl',
  QUOTE_LIMIT: { limit: async () => ({ success: true }) },
};
function request(options = {}) {
  const data = new FormData();
  for (const [key, value] of Object.entries({
    doelgroep: 'Particulier', naam: 'SYNTHETISCHE TEST', plaats: 'Dordrecht',
    dienst: 'Gietvloer', email: 'test@example.org', omschrijving: 'Foto-overdracht testen',
    submission_id: ref, 'cf-turnstile-response': 'test-token', ...options.fields,
  })) data.set(key, value);
  for (const file of options.files ?? []) data.append('attachment', file);
  return new Request('https://receiver.example/offerte', {
    method: 'POST', body: data,
    headers: { Origin: options.origin ?? origin, 'CF-Connecting-IP': '192.0.2.1' },
  });
}

test('multipart, validatie, spamcontrole, mailcontract en herstel', async t => {
  const attempts = [];
  let challenge = { success: true, action: 'offerte', hostname: 'www.jmbetonservice.nl' };
  let mailReply = () => Response.json({ id: 'email-test-id' });
  t.mock.method(globalThis, 'fetch', async (url, options) => {
    if (url.includes('siteverify')) {
      assert.equal(options.body.get('response'), 'test-token');
      return Response.json(challenge);
    }
    assert.equal(url, 'https://api.resend.com/emails');
    attempts.push({ key: options.headers['Idempotency-Key'], email: JSON.parse(options.body) });
    return mailReply();
  });
  const send = options => receiver.fetch(request(options), env);
  const photo = new File([Buffer.from(png, 'base64')], 'originele naam.png', { type: 'image/png' });
  const result = await send({ files: [photo] });
  assert.equal(result.status, 202);
  assert.equal(result.headers.get('Access-Control-Allow-Origin'), origin);
  assert.deepEqual(await result.json(), { accepted: true, reference: ref });
  assert.deepEqual(attempts[0].email.attachments, [{ filename: 'projectfoto-1.png', content: png }]);
  assert.deepEqual(attempts[0].email.to, ['info@jmbetonservice.nl']);
  assert.equal(attempts[0].email.reply_to, 'test@example.org');
  assert.match(attempts[0].email.text, /SYNTHETISCHE TEST/);
  assert.equal((await send({ origin: 'https://other.example' })).status, 403);
  assert.equal((await send({ fields: { 'bot-field': 'filled' } })).status, 400);
  assert.equal((await send({ fields: { email: '', telefoon: '' } })).status, 400);
  assert.equal((await send({ files: [new File(['<svg/>'], 'fake.png', { type: 'image/png' })] })).status, 415);
  assert.equal((await send({ files: Array(6).fill(photo) })).status, 413);
  assert.equal((await send({ files: [new File([], 'empty.png')] })).status, 413);
  const large = new File([new Uint8Array(8 * 1024 * 1024)], 'large.png');
  assert.equal((await send({ files: [large, large] })).status, 413);
  assert.equal((await receiver.fetch(request(), {
    ...env, QUOTE_LIMIT: { limit: async () => ({ success: false }) },
  })).status, 429);
  challenge = { ...challenge, hostname: 'other.example' };
  assert.equal((await send()).status, 400);
  assert.equal(attempts.length, 1);
  challenge.hostname = 'www.jmbetonservice.nl';
  mailReply = () => Response.json({}, { status: 503 });
  assert.equal((await send({ files: [photo] })).status, 503);
  mailReply = () => { throw new DOMException('Timeout', 'TimeoutError'); };
  assert.equal((await send({ files: [photo] })).status, 503);
  mailReply = () => Response.json({ success: true });
  assert.equal((await send({ files: [photo] })).status, 503);
  mailReply = () => Response.json({ id: 'email-test-id' });
  assert.equal((await send({ files: [photo] })).status, 202);
  assert.ok(attempts.every(attempt => attempt.key === 'jm-offerte/' + ref));
  assert.ok(attempts.every(attempt => JSON.stringify(attempt.email) === JSON.stringify(attempts[0].email)));
});
