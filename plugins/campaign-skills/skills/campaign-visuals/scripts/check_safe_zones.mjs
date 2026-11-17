#!/usr/bin/env node
// Controleert een HTML-compositie (bv. HyperFrames) op safe zones en minimale lettergrootte.
//
// Rendert de pagina op het formaat van de placement, zoekt alle zichtbare tekst en meldt:
//   - tekst die (deels) in de safe zone valt waar de interface van het platform overheen ligt
//   - tekst kleiner dan min_lettergrootte_px_per_1080 (geschaald naar de breedte)
// Op meerdere tijdstippen: met --op 0,1500,4000 (ms). Een GSAP-timeline in window.__timelines
// (HyperFrames) of de globale GSAP-timeline wordt naar dat tijdstip gezet; anders wacht het script.
// Element bewust buiten de regels? Zet data-safe-zone="negeer" op het element of een ouder.
//
// Vereist Node 18+ en Playwright (npm i -D playwright; npx playwright install chromium).
// Exitcode 0 = schoon, 1 = overtredingen, 2 = gebruiksfout.
//
// Gebruik:
//   node check_safe_zones.mjs compositie.html --placement meta_reels_9x16
//   node check_safe_zones.mjs compositie.html --placement tiktok_9x16 --op 0,2000,5000 --specs creative_specs.json

import { readFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";

const here = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const opt = (name, fallback) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 && args[i + 1] ? args[i + 1] : fallback;
};
const file = args.find((a, i) => !a.startsWith("--") && !args[i - 1]?.startsWith("--"));
const placementKey = opt("placement");
const specsPath = opt("specs", resolve(here, "../assets/creative_specs.json"));
const times = opt("op", "0").split(",").map(Number);

if (!file || !placementKey || !existsSync(file)) {
  console.error("gebruik: node check_safe_zones.mjs <compositie.html> --placement <naam> [--op 0,1500] [--specs pad]");
  process.exit(2);
}
const specs = JSON.parse(readFileSync(specsPath, "utf8"));
const spec = specs.placements[placementKey];
if (!spec) {
  console.error(`fout: onbekende placement '${placementKey}'; kies uit ${Object.keys(specs.placements).join(", ")}`);
  process.exit(2);
}

let chromium;
try {
  ({ chromium } = await import("playwright"));
} catch {
  try {
    // Valt terug op require, dat ook NODE_PATH en de map van waaruit je het script draait doorzoekt.
    ({ chromium } = createRequire(resolve(process.cwd(), "noop.js"))("playwright"));
  } catch {
    chromium = null;
  }
}
if (!chromium) {
  console.error("fout: Playwright niet gevonden; installeer met 'npm i -D playwright' en 'npx playwright install chromium'");
  process.exit(2);
}

const { breedte: W, hoogte: H, safe_zone: zone } = spec;
const minFont = (specs.min_lettergrootte_px_per_1080 ?? 36) * (W / 1080);
const safe = { left: zone.links, top: zone.boven, right: W - zone.rechts, bottom: H - zone.onder };

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: W, height: H } });
await page.goto(pathToFileURL(resolve(file)).href, { waitUntil: "load" });
await page.evaluate(() => document.fonts?.ready);

const violations = [];
let previous = 0;
for (const t of times) {
  const seeked = await page.evaluate((ms) => {
    const tls = Object.values(window.__timelines ?? {}).filter((tl) => typeof tl?.seek === "function");
    if (tls.length) { tls.forEach((tl) => { tl.pause(); tl.seek(ms / 1000); }); return true; }
    if (window.gsap?.globalTimeline) { window.gsap.globalTimeline.pause(); window.gsap.globalTimeline.seek(ms / 1000); return true; }
    return false;
  }, t);
  if (!seeked && t > previous) await page.waitForTimeout(t - previous);
  previous = t;

  const texts = await page.evaluate(() => {
    const out = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const seen = new Set();
    while (walker.nextNode()) {
      const el = walker.currentNode.parentElement;
      if (!el || seen.has(el) || !walker.currentNode.textContent.trim()) continue;
      seen.add(el);
      if (el.closest('[data-safe-zone="negeer"], script, style, noscript')) continue;
      if (el.checkVisibility && !el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) continue;
      const r = el.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) continue;
      out.push({
        tekst: el.textContent.trim().replace(/\s+/g, " ").slice(0, 40),
        left: r.left, top: r.top, right: r.right, bottom: r.bottom,
        font: parseFloat(getComputedStyle(el).fontSize),
      });
    }
    return out;
  });

  for (const e of texts) {
    const outside = e.right <= 0 || e.bottom <= 0 || e.left >= W || e.top >= H;
    if (outside) continue;
    const sides = [];
    if (e.top < safe.top) sides.push("boven");
    if (e.bottom > safe.bottom) sides.push("onder");
    if (e.left < safe.left) sides.push("links");
    if (e.right > safe.right) sides.push("rechts");
    if (sides.length) violations.push(`${t}ms: "${e.tekst}" valt in de safe zone (${sides.join(", ")})`);
    if (e.font < minFont) violations.push(`${t}ms: "${e.tekst}" is ${e.font}px, minimaal ${Math.round(minFont)}px`);
  }
}
await browser.close();

console.log(`${file} op ${W}x${H} (${placementKey}), tijdstippen: ${times.join(", ")} ms`);
if (violations.length) {
  console.log(`\n${violations.length} overtreding(en):`);
  for (const v of [...new Set(violations)]) console.log(`  - ${v}`);
  process.exit(1);
}
console.log("Geen overtredingen.");
