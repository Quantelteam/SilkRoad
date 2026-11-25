-- Almasu: the language each Telegram user picked in the bot (kk, ru or en).
-- A separate table, not a column on users: users rows only exist after team
-- registration and are deleted when data is wiped, while the language is
-- chosen on the very first /start. Only the bot (service key) reads or writes
-- it, so row level security is on and there are no policies. Safe to re-run.

create table if not exists user_prefs (
  tg_id bigint primary key,
  lang text not null check (lang in ('kk', 'ru', 'en')),
  updated_at timestamptz not null default now()
);

alter table user_prefs enable row level security;
