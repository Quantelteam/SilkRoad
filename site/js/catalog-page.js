import { config } from './config.js';
import { loadCatalog, loadListings } from './data.js';
import {
  h, svg, byId as $, debounce, showError, drawIconPlaceholders, imageOrFallback, replaceUrl, SEARCH_DEBOUNCE_MS,
} from './dom.js';
import { iconForCategory, UI_ICONS } from './icons.js';
import { fold, listingCountsByPart, CATEGORY_KEYWORDS } from './filter.js';
import { categoryLabel, brandLabel } from './format.js';
import { t, applyStatic, bindLangSwitch } from './i18n.js';

applyStatic();
bindLangSwitch();
drawIconPlaceholders(UI_ICONS);
init();

async function init() {
  let catalog;
  try {
    catalog = await loadCatalog();
  } catch (err) {
    console.error(err);
    $('catalog-count').textContent = '';
    showError('catalog-error', t('error.catalog'));
    return;
  }
  const counts = await loadListingCounts(catalog);
  const rows = searchableRows(catalog);
  const params = new URLSearchParams(location.search);
  const fromUrl = (params.get('program') ?? '').toUpperCase();
  let program = fromUrl === 'FTC' || fromUrl === 'FLL' ? fromUrl : '';

  const input = /** @type {HTMLInputElement} */ ($('cq'));
  // The FTC / FLL switch narrows rows and brands; the search box narrows within them.
  const render = () => {
    const shownRows = rows.filter((r) => !program || r.part.program === program);
    const brands = catalog.brands.filter((b) => shownRows.some((r) => r.part.brand === b));
    $('brand-nav').replaceChildren(
      h('ul', null, brands.map((b) => h('li', null, h('a', { href: `#${slug(b)}` }, brandLabel(b))))),
    );
    for (const btn of document.querySelectorAll('.program-btn')) {
      btn.setAttribute('aria-pressed', String(/** @type {HTMLElement} */ (btn).dataset.program === program));
    }
    renderCatalog({ rows: shownRows, brands, categories: catalog.categories, counts, query: input.value });
  };
  const syncUrl = () => {
    const q = input.value.trim();
    const next = new URLSearchParams();
    if (q) next.set('q', q);
    if (program) next.set('program', program);
    replaceUrl(next);
  };

  input.value = params.get('q') ?? '';
  input.addEventListener('input', debounce(() => {
    syncUrl();
    render();
  }, SEARCH_DEBOUNCE_MS));
  document.querySelector('.program-switch').addEventListener('click', (e) => {
    const btn = /** @type {HTMLElement} */ (e.target).closest('.program-btn');
    if (!btn) return;
    const next = /** @type {HTMLElement} */ (btn).dataset.program;
    program = next === 'FTC' || next === 'FLL' ? next : '';
    syncUrl();
    render();
  });
  $('catalog-search').addEventListener('submit', (e) => {
    e.preventDefault();
    $('catalog').focus();
  });
  render();
}

/** Listing counts per part. A bonus: the catalog still works if listings fail to load. */
async function loadListingCounts(catalog) {
  try {
    const { listings } = await loadListings(catalog, config);
    return listingCountsByPart(listings);
  } catch (err) {
    console.error(err);
    return new Map();
  }
}

/** Each part with the folded text a catalog search matches against. */
function searchableRows(catalog) {
  // The English category name and the one on screen both match.
  const categoryName = new Map(catalog.categories.map((c) => [c.id, `${c.name} ${categoryLabel(c)}`]));
  return catalog.parts.map((part) => ({
    part,
    text: fold([
      part.name, part.brand, part.sku ?? '', ...part.aliases,
      categoryName.get(part.category) ?? '', CATEGORY_KEYWORDS[part.category] ?? '',
    ].join(' ')),
  }));
}

function renderCatalog({ rows, brands, categories, counts, query }) {
  const tokens = fold(query.trim()).split(/\s+/).filter(Boolean);
  const shown = rows.filter((r) => tokens.every((t) => r.text.includes(t))).map((r) => r.part);
  $('catalog-count').textContent = shown.length === rows.length
    ? t('catalog.total', { parts: t('count.parts', { n: rows.length }), brands: t('count.brands', { n: brands.length }) })
    : t('catalog.someOf', { shown: shown.length, n: rows.length });
  $('brands').replaceChildren(...brands.map((b) => brandSection(b, shown, categories, counts)).filter(Boolean));
  $('catalog-empty').hidden = shown.length > 0;
}

function brandSection(brand, parts, categories, counts) {
  const brandParts = parts.filter((p) => p.brand === brand);
  if (!brandParts.length) return null;
  const groups = categories
    .map((category) => ({ category, parts: brandParts.filter((p) => p.category === category.id) }))
    .filter((group) => group.parts.length);
  const id = slug(brand);

  return h('section', { class: 'brand', id, 'aria-labelledby': `${id}-title` },
    h('h2', { id: `${id}-title` }, brandLabel(brand), h('span', { class: 'brand-count' }, t('count.parts', { n: brandParts.length }))),
    groups.map(({ category, parts: groupParts }) =>
      h('div', { class: 'cat-group' },
        h('h3', null, svg(iconForCategory(category.id), { size: 22 }), categoryLabel(category)),
        h('ul', { class: 'part-rows' }, groupParts.map((p) => partRow(p, counts.get(p.id) ?? 0))),
      )),
  );
}

function partRow(part, count) {
  const glyph = () => h('span', { class: 'part-thumb is-glyph' }, svg(iconForCategory(part.category), { size: 24 }));
  // The part name sits right next to the thumbnail, so the image itself is decorative (alt="").
  const thumb = part.image
    ? imageOrFallback({ src: part.image, alt: '', loading: 'lazy', width: 56, height: 56 }, h('span', { class: 'part-thumb' }), glyph)
    : glyph();
  return h('li', { class: 'part-row' },
    thumb,
    h('span', { class: 'part-name' },
      part.url ? h('a', { href: part.url, target: '_blank', rel: 'noopener noreferrer', title: t('catalog.productPage') }, part.name) : part.name),
    h('span', { class: 'part-sku' }, part.sku ?? ''),
    count
      ? h('a', { class: 'part-count', href: `listings.html?part=${encodeURIComponent(part.id)}` }, t('count.listings', { n: count }))
      : h('span', { class: 'part-count is-zero' }, t('catalog.noListings')),
  );
}

/** "REV Robotics" → "rev-robotics", for in-page brand anchors. */
function slug(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}
