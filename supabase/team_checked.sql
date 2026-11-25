-- Adds the admin-checked ✓ badge for teams and exposes it to the website.
alter table teams add column if not exists checked_at timestamptz;
alter table teams add column if not exists checked_by bigint;

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

grant select on listings_public to anon, authenticated;
