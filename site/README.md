# Almasu website

Live at **https://almasu.vercel.app** (Vercel project `silkroad-exchange`).

Plain HTML, CSS and JavaScript modules with no build step and no npm dependencies (see `../docs/adr-001-website-stack.md` for why). It reads the bot's `listings_public` view from Supabase with the public key and shows active listings with search and filters. Each listing links to the poster's Telegram chat.

## Run it

```bash
npm run serve      # from the repo root, then open http://localhost:8080
npm test           # Node 22+, built-in test runner, no dependencies
```

## Files

| Path | What it is |
| --- | --- |
| `index.html` | Listings: search, filters, cards, detail dialog, intro video slot |
| `catalog.html` | Parts catalog by brand and category, with official vendor photos |
| `js/config.js` | Supabase URL, publishable key, bot username |
| `js/data.js` | Loads and validates listings; `normalizeBotRow()` maps the bot's fields |
| `js/filter.js` | Search, filters, sorting and URL state (pure, unit-tested in `../tests`) |
| `js/format.js` | Interface wording for listings, in one place for translation |
| `js/intro.js` | Header video; hidden until `assets/intro.mp4` exists |
| `data/parts-catalog.json` | 213 parts with part numbers checked on the vendors' sites |
| `data/demo-listings.json` | Example listings, used only when no Supabase key is set |
| `vercel.json` | Security headers (CSP, HSTS and others) |

## Keys

`js/config.js` holds the publishable (anon) key. It is meant to be public: the bot's Row Level Security only lets it read `listings_public` and `parts`, and writes with it are refused. The `service_role` key belongs to the bot's server only.

## Deploy

`scripts/deploy-vercel.sh` uploads `site/` to Vercel production with only `curl` (set `VERCEL_TOKEN`). Or connect the repo in the Vercel dashboard: framework "Other", root directory `site`, no build command, no output directory. Then set the bot's `SITE_URL` to the site's https address so its Website buttons work.

## Product photos

Catalog photos load from each maker's own site and belong to them. No maker grants permission to show them elsewhere, so the site hotlinks instead of copying, credits the source, and falls back to a drawing if an image fails. `../docs/research/official-part-photos.md` has the details and suggests asking the makers for permission.
