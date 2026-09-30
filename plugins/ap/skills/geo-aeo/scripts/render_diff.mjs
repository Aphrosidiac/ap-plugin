// render_diff.mjs — how much of each page exists only after JavaScript runs?
//
//   node render_diff.mjs https://example.com/ [more urls...] [--json out.json]
//
// Loads every URL twice in headless Chromium: once with JavaScript DISABLED (what GPTBot,
// OAI-SearchBot, ClaudeBot, PerplexityBot and the user-triggered fetchers get — they read
// server HTML) and once rendered (what Googlebot and Applebot eventually index). Reports the
// share of rendered words missing from the no-JS view, plus head tags (title, canonical,
// meta robots, JSON-LD) that only appear after hydration.
//
// Rule of thumb: > 10% of the main content missing without JS is a rendering defect for AI
// search; head tags that only exist after JS are a defect for everyone but Google.
//
// Playwright resolves from the current project (npm i -D playwright && npx playwright install
// chromium) or from $PLAYWRIGHT_DIR.
import { createRequire } from 'node:module';
import path from 'node:path';
import fs from 'node:fs';

const tryReq = (dir) => { try { return createRequire(path.join(dir, 'noop.js'))('playwright'); } catch { return null; } };
const pw = tryReq(process.cwd()) || (process.env.PLAYWRIGHT_DIR && tryReq(process.env.PLAYWRIGHT_DIR));
if (!pw) {
  console.error('playwright not found. In the project: npm i -D playwright && npx playwright install chromium\n' +
    'or point PLAYWRIGHT_DIR at any folder whose node_modules has playwright.');
  process.exit(2);
}

const args = process.argv.slice(2);
const jsonIdx = args.indexOf('--json');
const jsonOut = jsonIdx >= 0 ? args.splice(jsonIdx, 2)[1] : null;
const urls = args.filter((a) => !a.startsWith('--')).map((u) => (u.startsWith('http') ? u : `https://${u}`));
if (!urls.length) { console.error('usage: node render_diff.mjs <url...> [--json out.json]'); process.exit(2); }

const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';

// Runs in the page. Returns main-content text and head facts.
const snapshot = () => {
  const pick = document.querySelector('main, article, [role=main]') || document.body;
  const clone = pick ? pick.cloneNode(true) : document.createElement('div');
  clone.querySelectorAll('script,style,noscript,template,svg,nav,header,footer,aside').forEach((n) => n.remove());
  const text = (clone.textContent || '').replace(/\s+/g, ' ').trim();
  const q = (s, a = 'content') => Array.from(document.querySelectorAll(s)).map((e) => e.getAttribute(a) || '');
  return {
    title: document.title,
    canonical: q('link[rel=canonical]', 'href'),
    robots: q('meta[name=robots],meta[name=googlebot]'),
    description: q('meta[name=description]'),
    jsonld: Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map((s) => s.textContent.length),
    h1: Array.from(document.querySelectorAll('h1')).map((h) => h.textContent.trim()).slice(0, 3),
    links: document.querySelectorAll('a[href]').length,
    text,
  };
};

const tokens = (s) => (s.toLowerCase().match(/[\p{L}\p{N}]+/gu) || []);

const browser = await pw.chromium.launch({ headless: true });
const results = [];
for (const url of urls) {
  const out = { url };
  for (const [label, js] of [['nojs', false], ['rendered', true]]) {
    const ctx = await browser.newContext({ javaScriptEnabled: js, userAgent: UA, viewport: { width: 1280, height: 900 } });
    const page = await ctx.newPage();
    try {
      const resp = await page.goto(url, { waitUntil: js ? 'networkidle' : 'domcontentloaded', timeout: 45000 });
      out[`${label}_status`] = resp ? resp.status() : 0;
      if (js) {
        // Trigger lazy sections: scroll to the bottom in steps.
        await page.evaluate(async () => {
          for (let y = 0; y < document.body.scrollHeight; y += 800) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); }
        });
        await page.waitForTimeout(800);
      }
      out[label] = await page.evaluate(snapshot);
    } catch (e) {
      out[label] = { error: String(e).slice(0, 200), text: '', title: '', canonical: [], robots: [], jsonld: [], h1: [], links: 0 };
    }
    await ctx.close();
  }
  const a = tokens(out.nojs.text); const b = tokens(out.rendered.text);
  const have = new Map(); for (const t of a) have.set(t, (have.get(t) || 0) + 1);
  let missing = 0;
  for (const t of b) { const n = have.get(t) || 0; if (n > 0) have.set(t, n - 1); else missing++; }
  out.words_nojs = a.length; out.words_rendered = b.length;
  out.missing_pct = b.length ? Math.round((missing / b.length) * 1000) / 10 : 0;
  const issues = [];
  if (out.missing_pct > 10) issues.push(`${out.missing_pct}% of rendered main-content words are absent without JS`);
  for (const k of ['title', 'canonical', 'robots', 'description', 'jsonld', 'h1']) {
    const x = JSON.stringify(out.nojs[k]); const y = JSON.stringify(out.rendered[k]);
    if (x !== y) issues.push(`${k} differs: no-JS ${x.slice(0, 90)} vs rendered ${y.slice(0, 90)}`);
  }
  if (out.rendered.links > out.nojs.links * 1.5 + 5) issues.push(`links: ${out.nojs.links} without JS vs ${out.rendered.links} rendered (JS-only navigation hides pages from crawlers)`);
  out.issues = issues;
  delete out.nojs.text; delete out.rendered.text;
  results.push(out);
  console.log(`\n${url}\n  words: ${out.words_nojs} no-JS vs ${out.words_rendered} rendered · missing without JS: ${out.missing_pct}%`);
  for (const i of issues) console.log(`  ! ${i}`);
  if (!issues.length) console.log('  ok — server HTML carries the content');
}
await browser.close();
if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(results, null, 1));
