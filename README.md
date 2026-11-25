# SilkRoad Exchange

Buy. Sell. Exchange.

Teams in Kazakhstan post spare FTC parts through a Telegram bot; the public
website lists them and deals happen in Telegram private messages.

This repository contains the **bot** (the only way to post a listing), the
**database schema**, and the **website** in `site/` that reads from it.

- Website: https://silkroadexchange.vercel.app
- Bot: [@ftc_silkroad_bot](https://t.me/ftc_silkroad_bot)
- Stack: Python + aiogram 3, Supabase (PostgreSQL + file storage)

## What the bot does

| Step | Flow |
| --- | --- |
| `/start` | Registers the user with a team: program (FTC/FLL) and team number. Teams on the [USTEM Connect](https://connect.ustem.kz/teams) list are found straight away. A team that isn't on it sends its name and city to the moderators, who approve or reject it with one tap; the user can post once it's approved. Telegram @username is taken automatically. |
| ➕ New listing | Type (trade / sell / wanted / give away) → part from the catalog or free text → what you want in return or the price → condition → up to 3 photos → optional note → preview → publish. |
| 📋 My listings | Shows active listings with Edit (part, price, condition, note, photos) and Close. |
| `/cancel`, `/help` | Stop the current step, short explanation. |
| 🌐 Website, `/site` | A button that opens the website (only when `SITE_URL` is set). |

Photos are uploaded to Supabase Storage, so the website can show them straight
from the database. A closed listing disappears from the site.

## Setup

1. **Database.** In the Supabase SQL editor run `supabase/schema.sql`, then
   `supabase/seed_parts.sql` (≈170 standard REV, goBILDA, Studica and
   electronics parts) and `supabase/seed_teams.sql` (733 teams from USTEM
   Connect). All three are safe to re-run.
2. **Config.** Copy `bot/.env.example` to `bot/.env` and fill in:
   - `BOT_TOKEN` — from @BotFather
   - `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` — Supabase → Project settings → API
     (the `service_role` key; it is secret, `.env` is git-ignored)
   - `ADMIN_IDS` — Telegram user IDs of moderators, comma separated. They get
     requests from teams that aren't on the USTEM Connect list.
   - `SITE_URL` — optional, the website (https). When set, the menu gets a 🌐 Website
     button and a `/site` command, and every published listing and every entry in
     📋 My listings gets a button that opens that listing on the site (`/?listing=<id>`).
3. **Run.**
   ```bash
   cd bot
   python -m venv .venv
   .venv/Scripts/activate        # Linux/macOS: source .venv/bin/activate
   pip install -r requirements.txt
   python -m app.main
   ```

Deploy the same command on Railway, Render or a small VPS (long polling, no
public URL needed).

## Data for the website

See [docs/site-integration.md](docs/site-integration.md) for the handoff: keys,
every field of the view, filter queries and a card checklist.

The site reads the `listings_public` view with the anon key: one row per
listing with `have`, `want`, `price_kzt`, `condition`, `photos`, category,
team number, team name, city and `username` for the `t.me/<username>` link.
Filter it by `status = 'active'`. The `parts` table is also readable with the
anon key for the category and part filters.

The anon key can only read those two things; every write goes through the bot.

## Team list

`supabase/seed_teams.sql` holds the FTC and FLL teams from the public
[USTEM Connect catalog](https://connect.ustem.kz/teams): program, number, name
and city, nothing else. Refresh it with `python scripts/ustem_teams.py`, then
run the file again in the SQL editor; existing teams keep their names and
are only marked as on the list.

## Running on Vercel

The bot runs on Vercel as a webhook (project `silkroad-bot`, https://silkroad-bot.vercel.app):

- `bot/api/telegram.py` receives updates from Telegram and refuses any request
  without the `WEBHOOK_SECRET` header Telegram was given.
- Conversation state (which step a user is on) lives in the `bot_fsm` table,
  because each message may run in a fresh process.
- Environment variables on the Vercel project: `BOT_TOKEN`, `SUPABASE_URL`,
  `SUPABASE_SERVICE_KEY`, `SITE_URL`, `WEBHOOK_SECRET`, optional `ADMIN_IDS`.
- Deploy: `scripts/deploy-vercel.sh bot`. After the first deploy, or a domain
  change, register the webhook once:
  `curl -H "X-Setup-Secret: <WEBHOOK_SECRET>" https://silkroad-bot.vercel.app/api/setup`

`python -m app.main` (long polling) still works for local testing, but it
removes the webhook: run one or the other, never both.
