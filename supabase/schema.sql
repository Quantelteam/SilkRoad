-- FTC KZ Parts Exchange — database schema
-- Run once in the Supabase SQL editor.

create table if not exists teams (
    id         bigserial primary key,
    program    text        not null check (program in ('FTC', 'FLL')),
    number     integer     not null check (number > 0),
    name       text        not null,
    city       text        not null,
    verified   boolean     not null default false,
    created_at timestamptz not null default now(),
    unique (program, number)
);

create table if not exists users (
    tg_id      bigint      primary key,
    username   text,
    full_name  text,
    team_id    bigint      not null references teams (id),
    role       text        not null default 'member' check (role in ('member', 'admin')),
    created_at timestamptz not null default now()
);

create table if not exists parts (
    id       bigserial primary key,
    name     text not null,
    brand    text,
    sku      text,
    category text not null
);
-- official catalog photo, offered by the bot when a team has no photo of its own
alter table parts add column if not exists image text;

-- coalesce so that re-seeding does not duplicate parts without a brand
create unique index if not exists parts_unique_idx on parts (name, coalesce(brand, ''));

create table if not exists listings (
    id           bigserial primary key,
    team_id      bigint      not null references teams (id),
    user_tg_id   bigint      not null references users (tg_id),
    type         text        not null check (type in ('trade', 'sell', 'wanted', 'give')),
    have_part_id bigint      references parts (id),
    have_text    text,
    want_part_id bigint      references parts (id),
    want_text    text,
    price_kzt    integer     check (price_kzt >= 0),
    condition    text        check (condition in ('new', 'used', 'broken')),
    note         text,
    city         text        not null,
    photos       text[]      not null default '{}',
    status       text        not null default 'active' check (status in ('active', 'closed')),
    created_at   timestamptz not null default now(),
    updated_at   timestamptz not null default now(),
    -- a listing must say what it is about, either from the catalog or as free text
    check (have_part_id is not null or have_text is not null
           or want_part_id is not null or want_text is not null)
);

create index if not exists listings_active_idx on listings (status, created_at desc);
create index if not exists listings_user_idx on listings (user_tg_id, status);

-- Flat read model for the website.
create or replace view listings_public as
select l.id,
       l.type,
       l.status,
       l.condition,
       l.price_kzt,
       l.note,
       l.photos,
       l.created_at,
       coalesce(hp.name, l.have_text) as have,
       hp.brand                       as have_brand,
       hp.category                    as have_category,
       coalesce(wp.name, l.want_text) as want,
       wp.brand                       as want_brand,
       wp.category                    as want_category,
       t.id                           as team_id,
       t.program                      as team_program,
       t.number                       as team_number,
       t.name                         as team_name,
       t.checked_at is not null       as team_verified,
       l.city,
       u.username
from listings l
         join teams t on t.id = l.team_id
         join users u on u.tg_id = l.user_tg_id
         left join parts hp on hp.id = l.have_part_id
         left join parts wp on wp.id = l.want_part_id;

-- The bot talks to the database with the service key and bypasses RLS.
-- Nothing is readable with the anon key except the parts catalog and the
-- public listings view, which is what the website needs.
alter table teams enable row level security;
alter table users enable row level security;
alter table parts enable row level security;
alter table listings enable row level security;

drop policy if exists parts_public_read on parts;
create policy parts_public_read on parts for select to anon, authenticated using (true);

grant select on listings_public to anon, authenticated;

-- Public bucket for listing photos.
insert into storage.buckets (id, name, public)
values ('listings', 'listings', true)
on conflict (id) do nothing;

-- ---------------------------------------------------------------------------
-- Team list from USTEM Connect, and moderation for teams that are not on it.
-- Safe to re-run on an existing database.

-- Where a team came from: the USTEM Connect catalog (seed_teams.sql), a request
-- a moderator approved in the bot, or the bot before this list existed.
alter table teams add column if not exists source text not null default 'bot'
    check (source in ('ustem', 'request', 'bot'));

-- A team that is not on the USTEM list asks to be added; a moderator decides.
create table if not exists team_requests (
    id          bigserial primary key,
    program     text        not null check (program in ('FTC', 'FLL')),
    number      integer     not null check (number > 0),
    name        text        not null,
    city        text        not null,
    tg_id       bigint      not null,
    username    text,
    full_name   text,
    status      text        not null default 'pending'
                            check (status in ('pending', 'approved', 'rejected')),
    reviewed_by bigint,
    reviewed_at timestamptz,
    created_at  timestamptz not null default now()
);

-- One open request per Telegram user, and one per team.
create unique index if not exists team_requests_pending_user
    on team_requests (tg_id) where status = 'pending';
create unique index if not exists team_requests_pending_team
    on team_requests (program, number) where status = 'pending';

-- Only the bot (service key) reads or writes requests.
alter table team_requests enable row level security;

-- ---------------------------------------------------------------------------
-- FTC and FLL parts are separate catalogs: FTC teams pick from FTC parts,
-- FLL teams from LEGO Education SPIKE parts (seed_parts_fll.sql).
alter table parts add column if not exists program text not null default 'FTC'
    check (program in ('FTC', 'FLL'));
create index if not exists parts_program_idx on parts (program, category);

-- ---------------------------------------------------------------------------
-- Conversation state for the Vercel (webhook) bot: which step of a flow each
-- user is on. Only the bot (service key) reads or writes it.
create table if not exists bot_fsm (
    key        text        primary key,
    state      text,
    data       jsonb       not null default '{}'::jsonb,
    updated_at timestamptz not null default now()
);
alter table bot_fsm enable row level security;

-- ---------------------------------------------------------------------------
-- A user can exist without a team, e.g. a moderator who isn't on any team.
-- The bot treats such a user as not registered for posting.
alter table users alter column team_id drop not null;

-- The ✓ badge: an admin checked that the team's members are who they say. Separate
-- from teams.verified, which only means the team is on the USTEM Connect list.
alter table teams add column if not exists checked_at timestamptz;
alter table teams add column if not exists checked_by bigint;
