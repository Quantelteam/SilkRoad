# Connecting the website to the data

The bot and the website never call each other. The bot writes listings into
Supabase; the website reads them from Supabase. One view holds everything a
listing card needs, so the site needs no backend of its own.

## Credentials

```
NEXT_PUBLIC_SUPABASE_URL=https://oikyjgdaogqojhcjkrrd.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<publishable / anon key from Supabase → Project Settings → API>
```

The anon key is meant to be public — it can only **read** `listings_public` and
`parts`. Row level security blocks everything else, and all writes go through
the bot.

**Never put the `service_role` / secret key in the website.** It bypasses every
check. If it ever lands in frontend code or a public repo, rotate it in Supabase.

## The read model: `listings_public`

One row per listing, already joined with the part catalog, the team and the
uploader. Filter by `status = 'active'` — closed listings must not be shown.

| Field | Type | Notes |
| --- | --- | --- |
| `id` | number | Listing number, shown as `#123` |
| `type` | `trade` \| `sell` \| `wanted` \| `give` | Trade / For sale / Wanted / Give away |
| `status` | `active` \| `closed` | Always filter `status=active` |
| `have` | string \| null | What the team has. Catalog name, or the team's own text. `null` for `wanted` listings |
| `have_brand` | string \| null | `goBILDA`, `REV Robotics`, … `null` for free text |
| `have_category` | string \| null | Catalog category, `null` for free text |
| `want` | string \| null | What they want in return, or the part a `wanted` listing is looking for |
| `want_brand`, `want_category` | string \| null | Same as above for the wanted side |
| `price_kzt` | number \| null | Only for `sell`. `null` means negotiable |
| `condition` | `new` \| `used` \| `broken` \| null | New / Used — working / Broken — for parts |
| `note` | string \| null | Free text from the uploader |
| `photos` | string[] | Public image URLs, up to 3, may be empty |
| `city` | string | Team's city |
| `team_number`, `team_name`, `team_program` | number, string, `FTC`/`FLL` | Shown as `FTC #12345 Name` |
| `team_id` | number | For a future team page |
| `team_verified` | boolean | Admin-set trust flag, unused for now |
| `username` | string | Telegram username **without** `@`. Contact link: `https://t.me/${username}` |
| `created_at` | ISO timestamp | Sort newest first |

Photo URLs are already public — put them straight in `<img src>`.

## Reading it

```ts
// lib/supabase.ts
import { createClient } from "@supabase/supabase-js";

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
);
```

```ts
// Listings page, with the MVP filters
type Filters = {
  q?: string;        // free text
  category?: string; // have_category
  city?: string;
  type?: string;     // trade | sell | wanted | give
  team?: number;     // team_number
};

export async function getListings(f: Filters) {
  let query = supabase
    .from("listings_public")
    .select("*")
    .eq("status", "active")
    .order("created_at", { ascending: false })
    .limit(60);

  if (f.category) query = query.eq("have_category", f.category);
  if (f.city) query = query.eq("city", f.city);
  if (f.type) query = query.eq("type", f.type);
  if (f.team) query = query.eq("team_number", f.team);
  if (f.q) {
    const t = f.q.replace(/[,()%*\\]/g, " ").trim();
    query = query.or(
      `have.ilike.%${t}%,want.ilike.%${t}%,note.ilike.%${t}%,team_name.ilike.%${t}%`,
    );
  }

  const { data, error } = await query;
  if (error) throw error;
  return data;
}
```

Filter dropdown options:

```ts
// categories for the filter
const { data } = await supabase.from("parts").select("category");
const categories = [...new Set(data!.map((r) => r.category))].sort();

// cities actually in use
const { data: rows } = await supabase
  .from("listings_public").select("city").eq("status", "active");
const cities = [...new Set(rows!.map((r) => r.city))].sort();
```

The same query works as a plain HTTP call if the UI is not React:

```
GET https://oikyjgdaogqojhcjkrrd.supabase.co/rest/v1/listings_public
      ?status=eq.active&order=created_at.desc&limit=60
Headers: apikey: <anon key>
```

## Card checklist (from the project description)

Photo · what they have · what they want or the price · condition · team
`FTC #number Name` · city · `@username` as a `t.me` link. Nothing else is
needed: no login, no cart, no in-app chat.

## Local setup for the website

```bash
cd site
npm install
cp .env.local.example .env.local   # fill in the two values above
npm run dev
```

## Testing with real data

Post a listing through [@ftc_silkroad_bot](https://t.me/ftc_silkroad_bot) and
reload the page — it appears immediately. Close it in the bot and it is gone.
That is the whole contract between the two halves.
