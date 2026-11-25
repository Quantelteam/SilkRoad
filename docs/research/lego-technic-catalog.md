# LEGO Technic catalog: sources and notes

Companion to `lego-technic.json` (SilkRoad Exchange spare-parts catalog). Built 2026-11-25.

## Scope

Every entry is an element that appears in the inventory of the LEGO Education SPIKE Prime Set (45678) and/or the SPIKE Prime Expansion Set (45681), limited to loose Technic structure, motion, hardware and wheel parts. Electronics (hub, motors, sensors, battery, cable), System bricks/plates/tiles, stickers and storage parts are left out. Colour variants are grouped under one design number.

## Sources actually loaded

LEGO.com (403), Rebrickable web pages (Cloudflare challenge, 403/402) and BrickLink (bot check, 405) all refused automated requests, so no LEGO.com page, Rebrickable part page or BrickLink page was loaded. Two sources were used instead:

1. **Rebrickable database downloads** (the official Rebrickable data dump on its CDN): `https://cdn.rebrickable.com/media/downloads/inventory_parts.csv.gz`, `https://cdn.rebrickable.com/media/downloads/inventories.csv.gz`, `https://cdn.rebrickable.com/media/downloads/parts.csv.gz`, `https://cdn.rebrickable.com/media/downloads/part_relationships.csv.gz`, `https://cdn.rebrickable.com/media/downloads/elements.csv.gz`, `https://cdn.rebrickable.com/media/downloads/sets.csv.gz`. Set inventories used: inventory id 34280 (45678-1 version 1), 109612 (45678-1 version 2), 107280 (45681-1, which Rebrickable titles "SPIKE Prime Expansion Set (v2)"). Spare-part rows were ignored. **Every `sku` in the JSON appears as a `part_num` in these files and in at least one of those three inventories.**
2. **Brickset**, which publishes LEGO's own element and design IDs: set inventories https://brickset.com/inventories/45678-1 and https://brickset.com/inventories/45681-1, plus one design page per entry (`https://brickset.com/parts/design-<number>`). The JSON `url` is that design page; each one was loaded and lists at least one LEGO element under that design number with a matching LEGO description.

Cross-check method: each element ID on the Brickset set inventories was mapped through Rebrickable `elements.csv` to a Rebrickable part number, so both sources agree that the same physical part is in the set. **BrickLink could not be checked** (unreachable); the numbers are Rebrickable's, which usually but not always match BrickLink's. Spot-check a few on BrickLink before launch.

## Number conflicts and how they were resolved

- `sku` is the Rebrickable part number. LEGO has re-numbered many Technic designs (for new moulds), so the current LEGO design ID shown on Brickset's set inventory often differs. Both numbers are given in the table below (column "LEGO design ID in set (Brickset)"). The Rebrickable number is used because it is the one printed in the community catalogs teams search, and Brickset also has a LEGO design page under that older number (except the two cases below).
- **3713 (bush)** and **3749 (tan axle pin)**: Brickset has no elements under these numbers; LEGO uses 42798 and 6562 for the parts in the sets. The JSON `url` for these two points to the Brickset page for 42798 / 6562, and the number 3713 / 3749 itself was confirmed only in the Rebrickable data files.
- Mould variants merged into one entry (Rebrickable lists them as separate parts linked by a 'mould' relationship; to a team they are the same piece): 2780 + 61332 (black friction pin), 48989 + 65489 (3L pin connector with 4 pins), 55615 + 49130 (3×3 bent connector with 4 pins). The older number is the sku.
- Rebrickable suffixes dropped to the LEGO design number: 32123b → 32123 (half bush), 39367pat0001 → 39367 (56 mm wheel), 49295pat0001 → 49295 (88 mm wheel). 39367 and 49295 exist as base parts in Rebrickable `parts.csv` ("[Plain]" integral-tyre wheels). Rebrickable has no plain 32123, only 32123a/32123b, so 32123 is confirmed only by its Brickset design page (LEGO "1/2 BUSH"); the part in 45681 is Rebrickable 32123b / LEGO 42136.
- Small turntable: Rebrickable calls 99010 "base, 28 tooth" and 99009 "top"; LEGO (Brickset) calls the 28-tooth part the "upper part". The catalog names avoid top/base and say "28 tooth part" / "plain part".
- Brickset (LEGO data) also lists newer mould numbers alongside the older ones in these sets: 42924 (with 6558), 65304 (with 32054), 88738 (with 18938), 69819 (for 41678). These are noted in the table but not given separate entries.

## Per-entry sources

Rebrickable column: part number(s) and quantity per inventory (45678 v1 / 45678 v2 / 45681). Source for that column is `inventory_parts.csv.gz` + `parts.csv.gz` above.

| id | name | category | JSON url (loaded) | Rebrickable part in set inventory | LEGO design ID in set (Brickset inventory) |
|---|---|---|---|---|---|
| lego-60483 | Technic liftarm beam 1×2 with pin hole and axle hole | structure | https://brickset.com/parts/design-60483 | 60483: 45678-1 v1 ×4, 45678-1 v2 ×4 | 40147 (45678) |
| lego-32523 | Technic liftarm beam 1×3 | structure | https://brickset.com/parts/design-32523 | 32523: 45678-1 v1 ×8, 45678-1 v2 ×8, 45681-1 v1 ×10 | 32523 (45678, 45681) |
| lego-32316 | Technic liftarm beam 1×5 | structure | https://brickset.com/parts/design-32316 | 32316: 45678-1 v1 ×5, 45678-1 v2 ×5, 45681-1 v1 ×8 | 32316 (45678, 45681) |
| lego-32524 | Technic liftarm beam 1×7 | structure | https://brickset.com/parts/design-32524 | 32524: 45678-1 v1 ×7, 45678-1 v2 ×7, 45681-1 v1 ×6 | 32524 (45678, 45681) |
| lego-40490 | Technic liftarm beam 1×9 | structure | https://brickset.com/parts/design-40490 | 40490: 45678-1 v1 ×5, 45678-1 v2 ×5, 45681-1 v1 ×8 | 64289 (45678, 45681) |
| lego-32525 | Technic liftarm beam 1×11 | structure | https://brickset.com/parts/design-32525 | 32525: 45678-1 v1 ×5, 45678-1 v2 ×5, 45681-1 v1 ×6 | 64290 (45678, 45681) |
| lego-41239 | Technic liftarm beam 1×13 | structure | https://brickset.com/parts/design-41239 | 41239: 45678-1 v1 ×4, 45678-1 v2 ×4, 45681-1 v1 ×6 | 41239 (45678, 45681) |
| lego-32278 | Technic liftarm beam 1×15 | structure | https://brickset.com/parts/design-32278 | 32278: 45678-1 v1 ×6, 45678-1 v2 ×6, 45681-1 v1 ×6 | 64871 (45678, 45681) |
| lego-32140 | Technic L-shaped liftarm 2×4 | structure | https://brickset.com/parts/design-32140 | 32140: 45678-1 v1 ×5, 45678-1 v2 ×5, 45681-1 v1 ×8 | 42137 (45678, 45681) |
| lego-32526 | Technic L-shaped liftarm 3×5 | structure | https://brickset.com/parts/design-32526 | 32526: 45678-1 v1 ×5, 45678-1 v2 ×5, 45681-1 v1 ×10 | 32526 (45678, 45681) |
| lego-14720 | Technic H-shaped liftarm 3×5 (offset centre holes) | structure | https://brickset.com/parts/design-14720 | 14720: 45678-1 v1 ×4, 45678-1 v2 ×4, 45681-1 v1 ×6 | 14720 (45678, 45681) |
| lego-60484 | Technic T-shaped liftarm 3×3 | structure | https://brickset.com/parts/design-60484 | 60484: 45678-1 v1 ×5, 45678-1 v2 ×5, 45681-1 v1 ×4 | 60484 (45678, 45681) |
| lego-32348 | Technic bent liftarm 1×7 (4-4) | structure | https://brickset.com/parts/design-32348 | 32348: 45678-1 v1 ×5, 45678-1 v2 ×5, 45681-1 v1 ×4 | 42165 (45678, 45681) |
| lego-32271 | Technic bent liftarm 1×9 (7-3) | structure | https://brickset.com/parts/design-32271 | 32271: 45678-1 v1 ×4, 45678-1 v2 ×4, 45681-1 v1 ×4 | 42160 (45678, 45681) |
| lego-32009 | Technic double bent liftarm 1×11.5 | structure | https://brickset.com/parts/design-32009 | 32009: 45678-1 v1 ×5, 45678-1 v2 ×5, 45681-1 v1 ×4 | 41486 (45678, 45681) |
| lego-99773 | Technic thin triangle liftarm | structure | https://brickset.com/parts/design-99773 | 99773: 45681-1 v1 ×4 | 65193 (45681) |
| lego-39793 | Technic connector frame 3×3 | structure | https://brickset.com/parts/design-39793 | 39793: 45678-1 v1 ×14, 45678-1 v2 ×14, 45681-1 v1 ×4 | 39793 (45678, 45681) |
| lego-64179 | Technic frame 5×7 (3×5 opening) | structure | https://brickset.com/parts/design-64179 | 64179: 45678-1 v1 ×2, 45678-1 v2 ×2, 45681-1 v1 ×8 | 64179 (45678, 45681) |
| lego-39794 | Technic frame 7×11 | structure | https://brickset.com/parts/design-39794 | 39794: 45678-1 v1 ×2, 45678-1 v2 ×2, 45681-1 v1 ×4 | 39794 (45678, 45681) |
| lego-39790 | Technic frame 11×15 | structure | https://brickset.com/parts/design-39790 | 39790: 45678-1 v1 ×2, 45678-1 v2 ×2, 45681-1 v1 ×2 | 39790 (45678, 45681) |
| lego-39369 | Technic base frame 11×19 | structure | https://brickset.com/parts/design-39369 | 39369: 45678-1 v1 ×2, 45678-1 v2 ×2 | 39369 (45678) |
| lego-65817 | Technic maker plate 11×15 (frame with internal structure) | structure | https://brickset.com/parts/design-65817 | 65817: 45681-1 v1 ×1 | 65817 (45681) |
| lego-11954 | Technic curved panel 11×3 | structure | https://brickset.com/parts/design-11954 | 11954: 45678-1 v1 ×2, 45678-1 v2 ×2 | 11954 (45678) |
| lego-15458 | Technic flat panel 3×11 | structure | https://brickset.com/parts/design-15458 | 15458: 45678-1 v1 ×2, 45678-1 v2 ×2 | 15458 (45678) |
| lego-32062 | Technic axle 2 (notched) | motion | https://brickset.com/parts/design-32062 | 32062: 45678-1 v1 ×12, 45678-1 v2 ×12, 45681-1 v1 ×8 | 32062 (45678, 45681) |
| lego-4519 | Technic axle 3 | motion | https://brickset.com/parts/design-4519 | 4519: 45678-1 v1 ×10, 45678-1 v2 ×10, 45681-1 v1 ×14 | 4519 (45678, 45681) |
| lego-3705 | Technic axle 4 | motion | https://brickset.com/parts/design-3705 | 3705: 45678-1 v1 ×4, 45678-1 v2 ×4, 45681-1 v1 ×4 | 3705 (45678, 45681) |
| lego-32073 | Technic axle 5 | motion | https://brickset.com/parts/design-32073 | 32073: 45678-1 v1 ×6, 45678-1 v2 ×6, 45681-1 v1 ×4 | 32073 (45678, 45681) |
| lego-3706 | Technic axle 6 | motion | https://brickset.com/parts/design-3706 | 3706: 45681-1 v1 ×4 | 3706 (45681) |
| lego-44294 | Technic axle 7 | motion | https://brickset.com/parts/design-44294 | 44294: 45678-1 v1 ×6, 45678-1 v2 ×6 | 44294 (45678) |
| lego-3707 | Technic axle 8 | motion | https://brickset.com/parts/design-3707 | 3707: 45678-1 v1 ×6, 45678-1 v2 ×6 | 3707 (45678) |
| lego-60485 | Technic axle 9 | motion | https://brickset.com/parts/design-60485 | 60485: 45678-1 v1 ×6, 45678-1 v2 ×6 | 60485 (45678) |
| lego-23948 | Technic axle 11 | motion | https://brickset.com/parts/design-23948 | 23948: 45678-1 v1 ×3, 45678-1 v2 ×3 | 23948 (45678) |
| lego-3708 | Technic axle 12 | motion | https://brickset.com/parts/design-3708 | 3708: 45681-1 v1 ×2 | 3708 (45681) |
| lego-50450 | Technic axle 32 | motion | https://brickset.com/parts/design-50450 | 50450: 45681-1 v1 ×2 | 13927 (45681) |
| lego-87083 | Technic axle 4 with stop | motion | https://brickset.com/parts/design-87083 | 87083: 45681-1 v1 ×4 | 87083 (45681) |
| lego-15462 | Technic axle 5 with stop | motion | https://brickset.com/parts/design-15462 | 15462: 45681-1 v1 ×2 | 15462 (45681) |
| lego-55013 | Technic axle 8 with stop | motion | https://brickset.com/parts/design-55013 | 55013: 45681-1 v1 ×2 | 55013 (45681) |
| lego-6589 | Technic 12 tooth bevel gear | motion | https://brickset.com/parts/design-6589 | 6589: 45681-1 v1 ×4 | 6589 (45681) |
| lego-32270 | Technic 12 tooth double bevel gear | motion | https://brickset.com/parts/design-32270 | 32270: 45678-1 v1 ×3, 45678-1 v2 ×3, 45681-1 v1 ×2 | 32270 (45678, 45681) |
| lego-32198 | Technic 20 tooth bevel gear | motion | https://brickset.com/parts/design-32198 | 32198: 45681-1 v1 ×2 | 32198 (45681) |
| lego-18575 | Technic 20 tooth double bevel gear | motion | https://brickset.com/parts/design-18575 | 18575: 45678-1 v1 ×3, 45678-1 v2 ×3, 45681-1 v1 ×2 | 18575 (45678, 45681) |
| lego-35185 | Technic 20 tooth double bevel gear with clutch | motion | https://brickset.com/parts/design-35185 | 35185: 45681-1 v1 ×2 | 35185 (45681) |
| lego-46372 | Technic 28 tooth double bevel gear | motion | https://brickset.com/parts/design-46372 | 46372: 45678-1 v1 ×3, 45678-1 v2 ×3, 45681-1 v1 ×2 | 46372 (45678, 45681) |
| lego-32498 | Technic 36 tooth double bevel gear | motion | https://brickset.com/parts/design-32498 | 32498: 45678-1 v1 ×3, 45678-1 v2 ×3, 45681-1 v1 ×2 | 32498 (45678, 45681) |
| lego-24121 | Technic gear rack quarter circle 11×11 (35 tooth) | motion | https://brickset.com/parts/design-24121 | 24121: 45681-1 v1 ×8 | 43038 (45681) |
| lego-64781 | Technic gear rack 1×13 with axle and pin holes | motion | https://brickset.com/parts/design-64781 | 64781: 45678-1 v1 ×2, 45678-1 v2 ×2 | 53504 (45678) |
| lego-87761 | Technic gear rack 1×7 with axle and pin holes | motion | https://brickset.com/parts/design-87761 | 87761: 45681-1 v1 ×2 | 65127 (45681) |
| lego-18938 | Technic large turntable, top (60 tooth) | motion | https://brickset.com/parts/design-18938 | 18938: 45681-1 v1 ×2 | 18938 (45681); 88738 (45681) |
| lego-18939 | Technic large turntable, base | motion | https://brickset.com/parts/design-18939 | 18939: 45681-1 v1 ×2 | 18939 (45681) |
| lego-99010 | Technic small turntable, 28 tooth part | motion | https://brickset.com/parts/design-99010 | 99010: 45681-1 v1 ×2 | 39892 (45681) |
| lego-99009 | Technic small turntable, plain part | motion | https://brickset.com/parts/design-99009 | 99009: 45681-1 v1 ×2 | 99009 (45681) |
| lego-2780 | Technic pin with friction (black pin) | hardware | https://brickset.com/parts/design-2780 | 2780: 45678-1 v1 ×92; 61332: 45678-1 v2 ×92, 45681-1 v1 ×80 | 61332 (45678, 45681) |
| lego-3673 | Technic pin without friction (grey pin) | hardware | https://brickset.com/parts/design-3673 | 3673: 45681-1 v1 ×12 | 3673 (45681) |
| lego-6558 | Technic long pin with friction 3L (blue pin) | hardware | https://brickset.com/parts/design-6558 | 6558: 45678-1 v1 ×14, 45678-1 v2 ×14, 45681-1 v1 ×36 | 6558 (45678); 42924 (45678, 45681) |
| lego-39888 | Technic long pin without friction 3L | hardware | https://brickset.com/parts/design-39888 | 39888: 45681-1 v1 ×8 | 39888 (45681) |
| lego-32054 | Technic long pin with bushing (stop bush) | hardware | https://brickset.com/parts/design-32054 | 32054: 45678-1 v1 ×10, 45678-1 v2 ×10, 45681-1 v1 ×12 | 32054 (45678); 65304 (45678, 45681) |
| lego-4274 | Technic half pin 1/2 | hardware | https://brickset.com/parts/design-4274 | 4274: 45681-1 v1 ×16 | 4274 (45681) |
| lego-43093 | Technic axle pin with friction (blue axle pin) | hardware | https://brickset.com/parts/design-43093 | 43093: 45681-1 v1 ×24 | 43093 (45681) |
| lego-3749 | Technic axle pin without friction (tan axle pin) | hardware | https://brickset.com/parts/design-6562 | 3749: 45678-1 v1 ×30, 45678-1 v2 ×30 | 6562 (45678) |
| lego-18651 | Technic axle pin 3L with friction and 2L axle | hardware | https://brickset.com/parts/design-18651 | 18651: 45678-1 v1 ×15, 45678-1 v2 ×15 | 18651 (45678) |
| lego-11214 | Technic axle pin 3L with friction and 1L axle | hardware | https://brickset.com/parts/design-11214 | 11214: 45681-1 v1 ×8 | 11214 (45681) |
| lego-3713 | Technic bush (full bushing) | hardware | https://brickset.com/parts/design-42798 | 3713: 45678-1 v1 ×10, 45678-1 v2 ×10, 45681-1 v1 ×12 | 42798 (45678, 45681) |
| lego-32123 | Technic half bush | hardware | https://brickset.com/parts/design-32123 | 32123b: 45681-1 v1 ×16 | 42136 (45681) |
| lego-32013 | Technic angle connector #1 (0°) | hardware | https://brickset.com/parts/design-32013 | 32013: 45678-1 v1 ×5, 45678-1 v2 ×5 | 42127 (45678) |
| lego-32034 | Technic angle connector #2 (180°) | hardware | https://brickset.com/parts/design-32034 | 32034: 45678-1 v1 ×5, 45678-1 v2 ×5 | 42134 (45678) |
| lego-32016 | Technic angle connector #3 (157.5°) | hardware | https://brickset.com/parts/design-32016 | 32016: 45681-1 v1 ×4 | 42128 (45681) |
| lego-32192 | Technic angle connector #4 (135°) | hardware | https://brickset.com/parts/design-32192 | 32192: 45678-1 v1 ×5, 45678-1 v2 ×5 | 42156 (45678) |
| lego-32015 | Technic angle connector #5 (112.5°) | hardware | https://brickset.com/parts/design-32015 | 32015: 45681-1 v1 ×4 | 41488 (45681) |
| lego-32014 | Technic angle connector #6 (90°) | hardware | https://brickset.com/parts/design-32014 | 32014: 45678-1 v1 ×5, 45678-1 v2 ×5, 45681-1 v1 ×12 | 42155 (45678, 45681) |
| lego-6536 | Technic axle and pin connector perpendicular | hardware | https://brickset.com/parts/design-6536 | 6536: 45681-1 v1 ×16 | 40146 (45681) |
| lego-32184 | Technic axle and pin connector perpendicular 3L with centre pin hole | hardware | https://brickset.com/parts/design-32184 | 32184: 45678-1 v1 ×4, 45678-1 v2 ×4, 45681-1 v1 ×4 | 42142 (45678, 45681) |
| lego-42003 | Technic axle and pin connector perpendicular 3L with 2 pin holes | hardware | https://brickset.com/parts/design-42003 | 42003: 45681-1 v1 ×12 | 42796 (45681) |
| lego-32291 | Technic axle and pin connector perpendicular double | hardware | https://brickset.com/parts/design-32291 | 32291: 45681-1 v1 ×4 | 42163 (45681) |
| lego-41678 | Technic axle and pin connector perpendicular double split | hardware | https://brickset.com/parts/design-41678 | 41678: 45681-1 v1 ×4 | 69819 (45681) |
| lego-63869 | Technic axle and pin connector perpendicular triple | hardware | https://brickset.com/parts/design-63869 | 63869: 45681-1 v1 ×8 | 42191 (45681) |
| lego-42135 | Technic axle connector with axle hole (reinforced) | hardware | https://brickset.com/parts/design-42135 | 42135: 45681-1 v1 ×6 | 42135 (45681) |
| lego-59443 | Technic axle connector 2L (smooth) | hardware | https://brickset.com/parts/design-59443 | 59443: 45678-1 v1 ×3, 45678-1 v2 ×3, 45681-1 v1 ×8 | 59443 (45678, 45681) |
| lego-48989 | Technic pin connector perpendicular 3L with 4 pins | hardware | https://brickset.com/parts/design-48989 | 48989: 45678-1 v1 ×12, 45678-1 v2 ×12; 65489: 45681-1 v1 ×10 | 65489 (45678, 45681) |
| lego-55615 | Technic pin connector 3×3 bent with 4 pins (ridges across) | hardware | https://brickset.com/parts/design-55615 | 55615: 45678-1 v1 ×4, 45678-1 v2 ×4; 49130: 45681-1 v1 ×6 | 49130 (45678, 45681) |
| lego-39367 | Wheel 56 mm (57×14) with integral tyre | wheels | https://brickset.com/parts/design-39367 | 39367pat0001: 45678-1 v1 ×4, 45678-1 v2 ×4 | 39367 (45678) |
| lego-49295 | Wheel 88 mm (88×14) with integral tyre | wheels | https://brickset.com/parts/design-49295 | 49295pat0001: 45681-1 v1 ×4 | 49295 (45681) |
| lego-56903 | Wheel rim 18×8 with axle hole | wheels | https://brickset.com/parts/design-56903 | 56903: 45678-1 v1 ×3, 45678-1 v2 ×3 | 56903 (45678) |
| lego-61254 | Tyre 23×7 (for 18×8 rim) | wheels | https://brickset.com/parts/design-61254 | 61254: 45678-1 v1 ×3, 45678-1 v2 ×3 | 61254 (45678) |
| lego-4185 | Technic wedge belt wheel (pulley) | wheels | https://brickset.com/parts/design-4185 | 4185: 45678-1 v1 ×2, 45678-1 v2 ×2 | 49750 (45678) |
| lego-2815 | Tyre for wedge belt wheel | wheels | https://brickset.com/parts/design-2815 | 2815: 45678-1 v1 ×2, 45678-1 v2 ×2 | 2815 (45678) |
| lego-39370 | Technic beam 3×5 with ball cup (caster holder) | wheels | https://brickset.com/parts/design-39370 | 39370: 45678-1 v1 ×1, 45678-1 v2 ×1, 45681-1 v1 ×1 | 39370 (45678, 45681) |
| lego-52629 | Ball 19 mm (caster ball) | wheels | https://brickset.com/parts/design-52629 | 52629: 45678-1 v1 ×1, 45678-1 v2 ×1, 45681-1 v1 ×1 | 52629 (45678, 45681) |

## Left out

**Not in either set inventory** (so outside the requested scope, even though teams use them): 8 tooth gear (Rebrickable 3647), 24 tooth gear (3648a/3648b), 40 tooth gear (3649), worm gear (4716), straight thin beams (e.g. 41677, 6632, 32449, 32063, 32065), even-length thick straight beams (1×4, 1×6, 1×8, 1×10, 1×12), axle 10 (3737). Numbers here were looked up in Rebrickable `parts.csv` only, to show they are absent from the set inventories; they are not in the JSON. Add them later from a set that contains them if teams ask.

**In the sets but dropped to keep the catalog to the common FLL parts (about 90 entries).** All appear in the Rebrickable inventories, and could be added back: 6629 bent beam 1×9 (6-4); 32005a link 1×6; 22961 pin connector hub with 1 axle; 18654 round pin connector 1L; 62462 round slotted pin connector; 87082 pin connector hub with 2 pins; 45590 flexible axle connector; 6553 pole reverser handle; 87408 toggle joint; 66906 pin with towball; 49283 wire clip; 24119 curved panel 7×3; 3738 Technic plate 2×8; 85543 / 85544 / 85546 rubber belts; 48267 Technic tooth; 57539 flexible hose; 98585 barrel with pin holes; and all System bricks, plates, tiles and minifigure parts.

**Uncertain:** nothing in the JSON is unconfirmed against the loaded files, but BrickLink numbers were not checked (see above). Names are plain English written for this catalog, not copied from either source.

