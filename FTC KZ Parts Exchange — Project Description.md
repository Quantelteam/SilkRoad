# FTC KZ Parts Exchange — Project Description

Nov 24, 2026 · @KairatNurtas

## Problem

Teams in Kazakhstan already trade parts, but the only place to do it is a Telegram channel that works like a plain chat. Demand is proven; the tool is not.

- **Listings get lost.** A post scrolls away within hours. A team that needs a servo next week never sees it.
- **No search or filters.** You cannot search by part, city, price or condition. Photos without part names are unsearchable.
- **No standard part names.** "Grey bracket" or "that motor" forces long back-and-forth messages.
- **No alerts.** Teams must check the chat constantly or miss what they need.
- **No trust signals.** You cannot see who a seller is, which team they are on, or whether past deals went well.
- **Slow imports.** REV, goBILDA and Studica parts come from abroad and take weeks. A broken motor before a qualifier can end a team's season, while another team in the same city has a spare in a drawer.

Before building, we confirm this with a short survey of 10–15 teams in the channel.

## Solution

Each part of the system does one job: the bot is the only way to post, the website is the only place to look, and the deal itself happens in Telegram private messages.

1. **Telegram bot — upload only.** Every listing goes through the bot. It asks step by step: what you have (X), what you want (Y — a part, a price, or nothing if giving away), photos, condition. Team name, city and Telegram username come from the team's registration automatically.
2. **Website — browse only.** A public site shows all active listings with search and filters by part, category, city, listing type and team. No account or login is needed to look.
3. **Telegram — contact.** Each listing shows the team name, city and the uploader's @username as a link. Tapping it opens a private Telegram chat where the two teams agree on the deal.

Optional: the bot can also repost each new listing to the existing FIRST parts channel with a link to the website, so people in the channel discover the site. Agree on this with the channel admins.

We do **not** handle money or delivery. The platform connects teams; they agree on payment and hand-over themselves.

## Features

Ship a small version that works in three weeks, then add features based on what teams ask for.

| Feature | Where | What it does | Version |
| --- | --- | --- | --- |
| Team registration | Bot | Team number, team name, city; Telegram username taken automatically | MVP |
| Create listing | Bot | Have X / want Y; trade, sell, wanted or give away; photos, condition | MVP |
| Parts catalog | Bot + site | 150–200 common REV, goBILDA, Studica and electronics parts so names are standard and searchable; free text for anything else | MVP |
| My listings | Bot | View, edit and close your own listings | MVP |
| Listings page | Site | All active listings as cards: photo, have, want, team, city, @username | MVP |
| Search and filters | Site | By part, category, city, listing type, team | MVP |
| Contact link | Site | @username opens a Telegram chat with the uploader | MVP |
| Auto-expiry | Bot | After 30 days the bot asks "still available?"; no answer hides the listing | v1.1 |
| Part alerts | Bot | Message me when someone posts a part I want | v1.1 |
| Report button | Site | Flags a scam or rule break to admins | v1.1 |
| Public statistics | Site | Parts exchanged, tenge saved, active teams | v1.1 |
| Channel repost | Bot | Optional repost of new listings to the FIRST parts channel | v1.1 |
| Languages | Bot + site | Kazakh, Russian, English | v1.2 |
| Team page | Site | All listings of one team in one place | v1.2 |
| Match suggestions | Site | "Team A has what you want and wants what you have" | v2 |

Out of scope on purpose: payments, delivery, in-app chat and a shopping cart. They add legal risk and work without solving the core problem.

## Technical architecture

The bot writes listings and the website only reads them. Both use one database, so a listing posted in the bot shows on the site immediately.

&#91;embedded content: system architecture · bot, Mini App, backend, storage\]

**Suggested stack** (free tiers are enough for this scale):

| Part | Technology | Why |
| --- | --- | --- |
| Bot | Python + aiogram, or TypeScript + grammY | Mature Telegram libraries, easy to learn |
| Website | Next.js (or React + Vite) | Fast public pages, easy search and filters, no login needed |
| Database and storage | Supabase (PostgreSQL + file storage) | Database, photo storage and API in one free service |
| Hosting | Vercel or Netlify for the website; Railway, Render or a small VPS for the bot | Free or a few dollars a month |
| Code | GitHub repository with README and issues | Lets future members and volunteers continue |

**Data model (main tables):**

- `teams` — id, program (FTC/FLL), team number, name, city, verified flag, coach contact (optional)
- `users` — Telegram ID, Telegram username, team id, role (member / admin)
- `parts` — id, name, brand, SKU, category, photo, typical price
- `listings` — id, team id, have (part id or free text), want (part id, price or free text), type (trade / sell / wanted / give away), condition, city, photos, status (active / closed), created date
- `subscriptions` — user id, part id or category, city
- `deals` — listing id, buyer team, seller team, closed date, outcome (traded / sold / given)
- `reports` — listing id, reporter, reason, status

**Key flows:**

1. A team posts through the bot. The bot checks the fields and saves the listing with the team's name, city and Telegram username.
2. The website reads active listings from the database and shows them with search and filters. No login.
3. A visitor taps the @username link (t.me/username) and the deal continues in Telegram.
4. The uploader closes the listing in the bot. It disappears from the site and counts in the statistics.
