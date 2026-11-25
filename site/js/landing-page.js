// The landing page: what Almasu is, live numbers, the newest listings and a peek at
// the catalog. Listings live on listings.html; old links to the root with a query
// (the bot's "?listing=17", shared searches) are sent there unchanged.
import { config } from './config.js';
import { loadCatalog, loadListings, telegramLink } from './data.js';
import { h, byId as $, drawIconPlaceholders, imageOrFallback, svg, teamNode } from './dom.js';
import { iconForCategory, UI_ICONS } from './icons.js';
import { TYPE_LABELS, formatAge, haveLabel, wantLabel, budgetLabel, teamLabel, partLabel } from './format.js';
import { t, applyStatic, bindLangSwitch } from './i18n.js';

// ?lang= is for this page (i18n.js has already saved it); anything else goes to listings.
const query = new URLSearchParams(location.search);
query.delete('lang');
if (query.toString()) location.replace(`listings.html?${query}${location.hash}`);

const LATEST = 3;
// Teaser parts: one recognisable part per kind, picked by catalog id.
const TEASER_IDS = [
  'gobilda-5203-2402-0019', 'rev-31-1595', 'axon-2004-0025-0002',
  'gobilda-3210-0003-0004', 'gobilda-3625-0202-0104', 'rev-31-1557',
];

applyStatic();
bindLangSwitch();
drawIconPlaceholders(UI_ICONS);
botLinks();
start();

async function start() {
  let catalog;
  try {
    catalog = await loadCatalog();
  } catch {
    return; // the numbers stay as dashes; the rest of the page still works
  }
  const brands = new Set(catalog.parts.map((p) => p.brand).filter((b) => b !== 'Other')).size;
  setStat('parts', catalog.parts.length);
  setStat('brands', brands);
  renderTeaser(catalog);

  try {
    const { listings, demo } = await loadListings(catalog, config);
    if (!demo) setStat('listings', listings.length);
    renderLatest(demo ? [] : listings.slice(0, LATEST));
  } catch {
    renderLatest([]);
  }
}

/** A number and its label, which agrees with it ("1 listing", "21 объявление"). */
function setStat(name, n) {
  $(`stat-${name}`).textContent = String(n);
  $(`stat-${name}-label`).textContent = t(`stats.${name}`, { n });
}

function botLinks() {
  const href = config.botUsername ? telegramLink(config.botUsername) : null;
  for (const a of document.querySelectorAll('a.bot-link')) {
    if (href) a.setAttribute('href', href);
  }
  const cta = $('bot-cta');
  if (href) cta.append(t('bot.ctaBefore'), h('a', { href, rel: 'noopener' }, `@${config.botUsername}`), t('bot.ctaAfter'));
}

function renderLatest(listings) {
  $('latest-empty').hidden = listings.length > 0;
  $('latest').replaceChildren(...listings.map((l) => {
    const want = l.type === 'giveaway' ? t('price.free') : (budgetLabel(l) ? t('price.budget', { price: budgetLabel(l) }) : wantLabel(l));
    const title = l.type === 'wanted' ? wantLabel(l) : haveLabel(l);
    return h('li', null, h('a', { class: 'latest-card', href: `listings.html?listing=${encodeURIComponent(l.id)}` },
      h('span', { class: `chip type-${l.type}` }, TYPE_LABELS[l.type]),
      h('span', { class: 'latest-title' }, title ?? t('part.fallback')),
      want && l.type !== 'wanted' ? h('span', { class: 'latest-want' }, want) : null,
      h('span', { class: 'latest-meta' }, teamNode(l.team, teamLabel(l.team)), ` · ${l.city} · ${formatAge(l.createdAt)}`)));
  }));
}

function renderTeaser(catalog) {
  const byId = new Map(catalog.parts.map((p) => [p.id, p]));
  const parts = TEASER_IDS.map((id) => byId.get(id)).filter((p) => p && p.image);
  $('teaser').replaceChildren(...parts.map((p) => {
    const glyph = () => h('div', { class: 'teaser-glyph' }, svg(iconForCategory(p.category), { size: 56 }));
    return h('li', null, h('a', { class: 'teaser-card', href: 'catalog.html' },
      imageOrFallback({ src: p.image, alt: '', loading: 'eager', width: 240, height: 240 },
        h('div', { class: 'teaser-img' }), glyph),
      h('span', { class: 'teaser-name' }, partLabel(p))));
  }));
}
