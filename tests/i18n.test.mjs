import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { DICT, LANGS, resolveLang, translate, pluralFor, lang, t } from '../site/js/i18n.js';
import { formatAge, wantLabel, formatPrice } from '../site/js/format.js';

test('language: ?lang, then the saved choice, then the first kk/ru browser language, else English', () => {
  assert.equal(resolveLang({}), 'en');
  assert.equal(resolveLang({ param: 'kk', stored: 'ru', languages: ['en'] }), 'kk');
  assert.equal(resolveLang({ param: 'xx', stored: 'ru', languages: ['kk-KZ'] }), 'ru');
  assert.equal(resolveLang({ param: 'EN', languages: ['ru-RU'] }), 'en');
  assert.equal(resolveLang({ stored: null, languages: ['de-DE', 'kk-KZ', 'ru-RU'] }), 'kk');
  assert.equal(resolveLang({ languages: ['en-US', 'ru'] }), 'ru');
  assert.equal(resolveLang({ languages: ['de', 'fr'] }), 'en');
  // English in the browser list doesn't stop the search for kk/ru further down.
  assert.equal(resolveLang({ languages: ['en-GB', 'kk'] }), 'kk');
});

test('outside a browser the language is English', () => {
  assert.equal(lang, 'en');
  assert.equal(t('nav.listings'), 'Listings');
});

test('every language has the same keys, and plural entries stay plural', () => {
  const en = Object.keys(DICT.en).sort();
  for (const code of LANGS) {
    assert.deepEqual(Object.keys(DICT[code]).sort(), en, `${code} keys differ from en`);
    for (const key of en) {
      assert.equal(typeof DICT[code][key], typeof DICT.en[key], `${code} ${key}`);
      if (typeof DICT[code][key] === 'object') assert.ok(DICT[code][key].other, `${code} ${key} needs an "other" form`);
    }
  }
});

test('placeholders are filled, unknown keys fall back to the key', () => {
  assert.equal(translate('ru', 'price.budget', { price: '5 000 ₸' }), 'Бюджет 5 000 ₸');
  assert.equal(translate('kk', 'contact.message', { team: 'Quattuor' }), 'Quattuor командасына жазу');
  assert.equal(translate('ru', 'no.such.key'), 'no.such.key');
});

test('plurals follow Intl.PluralRules: Russian one/few/many, Kazakh one form', () => {
  const ru = DICT.ru['count.listings'];
  assert.equal(pluralFor('ru', 1, ru), '1 объявление');
  assert.equal(pluralFor('ru', 3, ru), '3 объявления');
  assert.equal(pluralFor('ru', 5, ru), '5 объявлений');
  assert.equal(pluralFor('ru', 21, ru), '21 объявление');
  assert.equal(pluralFor('ru', 112, ru), '112 объявлений');
  assert.equal(translate('ru', 'count.parts', { n: 24 }), '24 детали');
  assert.equal(translate('kk', 'count.listings', { n: 1 }), '1 хабарландыру');
  assert.equal(translate('kk', 'count.listings', { n: 7 }), '7 хабарландыру');
  assert.equal(translate('en', 'count.listings', { n: 1 }), '1 listing');
  assert.equal(translate('en', 'count.listings', { n: 2 }), '2 listings');
  // "из" takes the genitive: 1 из 21 объявления, 3 из 5 объявлений.
  assert.equal(translate('ru', 'results.someOf', { shown: 1, n: 21 }), '1 из 21 объявления');
  assert.equal(translate('ru', 'results.someOf', { shown: 3, n: 5 }), '3 из 5 объявлений');
  assert.equal(translate('kk', 'results.someOf', { shown: 3, n: 5 }), '5 хабарландыру ішінен 3');
  assert.equal(translate('en', 'catalog.someOf', { shown: 3, n: 40 }), '3 of 40 parts');
  // No count yet (static HTML): the general form.
  assert.equal(translate('ru', 'stats.listings'), 'активных объявлений');
});

test('ages and "or" read naturally in each language', () => {
  const now = Date.parse('2026-11-24T12:00:00Z');
  assert.equal(formatAge('2026-11-24T08:00:00Z', now, 'ru'), 'сегодня');
  assert.equal(formatAge('2026-11-23T08:00:00Z', now, 'ru'), 'вчера');
  assert.equal(formatAge('2026-11-19T08:00:00Z', now, 'ru'), '5 дней назад');
  assert.equal(formatAge('2026-11-24T08:00:00Z', now, 'kk'), 'бүгін');
  assert.equal(formatAge('2026-11-23T08:00:00Z', now, 'kk'), 'кеше');
  const listing = { type: 'trade', want: { part: null, text: 'Core Hex', priceKzt: 9000 } };
  assert.equal(wantLabel(listing, 'ru'), `Core Hex или ${formatPrice(9000)}`);
  assert.equal(wantLabel(listing, 'kk'), `Core Hex немесе ${formatPrice(9000)}`);
});

test('every data-i18n key in the pages exists, and the English fallback in the HTML matches', () => {
  for (const page of ['index', 'listings', 'catalog']) {
    const html = readFileSync(new URL(`../site/${page}.html`, import.meta.url), 'utf8');
    for (const [, key] of html.matchAll(/data-i18n(?:-placeholder|-aria-label|-title)?="([^"]+)"/g)) {
      assert.ok(key in DICT.en, `${page}.html: unknown key ${key}`);
    }
    // Plain text elements: the HTML text is the English entry.
    for (const [, key, text] of html.matchAll(/data-i18n="([^"]+)"[^>]*>([^<]*)</g)) {
      const entry = DICT.en[key];
      const expected = typeof entry === 'object' ? entry.other : entry;
      assert.equal(text.replace(/\s+/g, ' ').trim(), expected.trim(), `${page}.html: ${key}`);
    }
    const pageKey = page === 'index' ? 'landing' : page;
    assert.match(html, new RegExp(`data-page="${pageKey}"`));
    assert.ok(html.includes(`<title>${DICT.en[`meta.${pageKey}.title`]}</title>`), `${page}.html title`);
  }
});
