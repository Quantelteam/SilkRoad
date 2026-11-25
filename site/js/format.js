// Display text for listings. The wording itself lives in i18n.js; part names, brands
// and team names are shown as the teams and makers wrote them.
import { lang, t, translate } from './i18n.js';
import { LISTING_TYPES, CONDITIONS } from './data.js';

export const TYPE_LABELS = Object.fromEntries(LISTING_TYPES.map((k) => [k, t(`type.${k}`)]));
export const CONDITION_LABELS = Object.fromEntries(CONDITIONS.map((k) => [k, t(`condition.${k}`)]));

const priceFormat = new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 0 });

/** 15000 → "15 000 ₸" */
export function formatPrice(kzt) {
  return `${priceFormat.format(kzt)} ₸`;
}

const DAY = 86_400_000;
const DATE_LOCALES = { en: 'en-GB', ru: 'ru-RU', kk: 'kk-KZ' };

const CYRILLIC = /\p{Script=Cyrillic}/u;

/**
 * Intl output in Russian or Kazakh, or null when the browser lacks that language's
 * data and quietly answers in English (Chromium's built-in ICU has no Kazakh dates).
 * @param {string} code @param {() => string} format
 */
function intlText(code, format) {
  const text = format();
  return code === 'en' || CYRILLIC.test(text) ? text : null;
}

/** "today", "yesterday", "5 days ago" (in the page language), then a date after a month. */
export function formatAge(iso, now = Date.now(), code = lang) {
  const relative = new Intl.RelativeTimeFormat(code, { numeric: 'auto' });
  const days = Math.max(0, Math.floor((now - Date.parse(iso)) / DAY));
  if (days < 31) {
    return intlText(code, () => relative.format(-days, 'day'))
      ?? (days === 0 ? translate(code, 'age.today') : days === 1 ? translate(code, 'age.yesterday') : translate(code, 'age.daysAgo', { n: days }));
  }
  const date = new Date(iso);
  return intlText(code, () => date.toLocaleDateString(DATE_LOCALES[code] ?? code, { day: 'numeric', month: 'short', year: 'numeric' }))
    ?? translate(code, 'age.date', { d: date.getDate(), month: translate(code, `month.${date.getMonth()}`), y: date.getFullYear() });
}

/** "goBILDA Grid plate…", but "Axon MAX servo" (not "Axon Axon…") and no "Other" prefix. */
export function partLabel(part) {
  if (part.brand === 'Other' || part.name.toLowerCase().startsWith(part.brand.toLowerCase())) return part.name;
  return `${part.brand} ${part.name}`;
}

/** What a listing offers, as one line. */
export function haveLabel(listing) {
  const h = listing.have;
  if (!h) return null;
  return h.part ? partLabel(h.part) : h.text;
}

/**
 * What a listing asks for, as one line. For trades and sales that's a part, a price,
 * or "part or price". For a wanted listing it's only the part; its price is a budget
 * (see budgetLabel). A giveaway asks for nothing; the "Free" chip says so.
 */
export function wantLabel(listing, code = lang) {
  const w = listing.want;
  if (!w) return null;
  const item = w.part ? partLabel(w.part) : w.text;
  if (listing.type === 'wanted') return item;
  if (w.priceKzt === null) return item;
  return item ? translate(code, 'want.or', { item, price: formatPrice(w.priceKzt) }) : formatPrice(w.priceKzt);
}

/** A wanted listing's price is what the team can pay. */
export function budgetLabel(listing) {
  return listing.type === 'wanted' && listing.want?.priceKzt != null ? formatPrice(listing.want.priceKzt) : null;
}

/** "FTC 12345 Steppe Gears", the way the bot shows a team; no program for the examples. */
export function teamLabel(team) {
  const number = team.number ? `${team.number} ` : '';
  return `${team.program ? `${team.program} ` : ''}${number}${team.name}`;
}

/** A catalog category's name in the page language, by its id. */
export function categoryLabel(category) {
  const key = `category.${category.id}`;
  const label = t(key);
  return label === key ? category.name : label;
}

/** Brand names stay as the makers write them; only the catch-all "Other" is translated. */
export function brandLabel(brand) {
  return brand === 'Other' ? t('brand.other') : brand;
}
