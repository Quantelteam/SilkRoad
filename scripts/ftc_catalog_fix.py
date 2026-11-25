"""Brings the bot's FTC parts in line with the verified site catalog.

The bot's first FTC seed (182 parts) had many part numbers that point at a
different product or don't exist. This script maps each old bot row (by id) to
a verified part in site/data/parts-catalog.json, keeps generic and third-party
items the site doesn't list, and drops branded rows whose part number could not
be verified. Row ids stay the same, so existing listings keep their part.

Writes supabase/fix_ftc_catalog.sql, a one-off migration for the live database.
supabase/seed_parts.sql was regenerated from the database after it ran.

Run: python3 scripts/ftc_catalog_fix.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "site" / "data" / "parts-catalog.json"
MIGRATION = ROOT / "supabase" / "fix_ftc_catalog.sql"

# Site category -> the bot's FTC category names (site/js/data.js maps them back).
BOT_CATEGORY = {
    "motors": "Motors", "servos": "Servos", "control": "Control & Electronics",
    "sensors": "Sensors", "batteries": "Power", "structure": "Structure",
    "motion": "Motion", "linear": "Linear Motion", "wheels": "Wheels",
    "hardware": "Hardware", "cables": "Cables", "other": "Other",
}

# Old bot row id -> verified site part id.
MAPPED = {
    1: "gobilda-5203-2402-0003", 2: "gobilda-5203-2402-0005", 3: "gobilda-5203-2402-0014",
    4: "gobilda-5203-2402-0019", 5: "gobilda-5203-2402-0027", 6: "gobilda-5203-2402-0051",
    7: "gobilda-5203-2402-0071", 8: "gobilda-5203-2402-0100", 9: "gobilda-5203-2402-0188",
    12: "rev-41-1301", 14: "rev-41-1291", 15: "rev-41-1300", 16: "rev-41-1600",
    17: "rev-41-1601", 18: "rev-41-1602", 19: "rev-41-1603",
    21: "andymark-am-2964b", 22: "andymark-am-3103", 23: "andymark-am-3637b", 24: "tetrix-44260",
    28: "gobilda-2000-0025-0002", 29: "gobilda-2000-0025-0003", 32: "gobilda-2000-0025-0502",
    33: "rev-41-1097", 34: "rev-31-1108", 35: "axon-2004-0025-0002", 36: "axon-2004-0025-0001",
    44: "gobilda-3102-0001-0001", 45: "rev-31-1595", 46: "rev-31-1153", 47: "rev-31-1596",
    48: "rev-11-1144", 50: "rev-31-1293", 51: "other-940-000110",
    57: "rev-31-1412-pk4", 58: "rev-31-1407-pk4", 60: "rev-31-1392-pk2",
    67: "rev-31-1302", 68: "tetrix-39057", 70: "rev-31-1299", 72: "rev-31-1387",
    76: "rev-31-1505", 77: "rev-31-1557", 78: "rev-31-1425", 79: "rev-31-1462",
    80: "rev-11-1271", 82: "gobilda-3110-0001-0001", 83: "gobilda-3110-0002-0002",
    87: "other-ll-3a", 88: "other-960-000694",
    93: "gobilda-3213-3606-0002", 94: "gobilda-3625-0202-0104", 95: "gobilda-3624-0014-0096",
    102: "rev-41-1354-pk2", 104: "rev-45-1655",
    110: "gobilda-1120-0005-0144", 111: "gobilda-1120-0007-0192", 112: "gobilda-1120-0009-0240",
    113: "gobilda-1120-0011-0288", 114: "gobilda-1120-0013-0336", 115: "gobilda-1120-0017-0432",
    117: "gobilda-1121-0009-0240", 126: "rev-41-1432-pk4", 127: "rev-41-1480-pk8",
    136: "gobilda-2106-4008-0960", 140: "gobilda-1310-0016-4008", 141: "gobilda-1309-0016-4008",
    142: "gobilda-1611-0514-4008", 149: "rev-41-1365", 150: "rev-41-1717",
    156: "gobilda-3417-4008-0016", 157: "gobilda-3210-0003-0004", 159: "rev-45-1507",
    161: "gobilda-3501-0804-0300",
    166: "gobilda-2800-0004-0008", 167: "gobilda-2800-0004-0012", 168: "gobilda-2800-0004-0016",
}

# Kept rows: generic items and third-party parts the site doesn't list.
# Part numbers that could not be verified are cleared; a wrong brand is fixed.
KEPT_FIXES = {
    10: {"sku": None}, 20: {"sku": None}, 37: {"brand": "Axon", "sku": None},
    49: {"sku": None}, 56: {"sku": None}, 59: {"sku": None}, 61: {"sku": None},
    69: {"sku": None}, 71: {"sku": None}, 74: {"sku": None}, 91: {"sku": None},
    92: {"sku": None}, 105: {"sku": None}, 106: {"sku": None}, 107: {"sku": None},
}
KEPT = set(KEPT_FIXES) | {
    27, 38, 39, 40, 41, 42, 43, 52, 53, 54, 55, 62, 63, 64, 65, 66, 73, 75, 81, 85, 86,
    89, 90, 108, 133, 134, 135, 154, 160, 165, 171, 172, 176, 178, 179, 180, 181, 182,
}

# Everything else in ids 1..182 is dropped: duplicates of a mapped row, or branded
# parts whose part number doesn't exist (e.g. 1120-0003-0003, REV-45-1655-M).
OLD_IDS = range(1, 183)


def q(value):
    return "null" if value is None else "'" + str(value).replace("'", "''") + "'"


def main() -> None:
    parts = {p["id"]: p for p in json.loads(CATALOG.read_text(encoding="utf-8"))["parts"]
             if p.get("program", "FTC") == "FTC"}
    if len(set(MAPPED.values())) != len(MAPPED):
        raise SystemExit("Two bot rows map to the same catalog part")
    if missing := [v for v in MAPPED.values() if v not in parts]:
        raise SystemExit(f"Unknown catalog ids: {missing}")
    if overlap := KEPT & set(MAPPED):
        raise SystemExit(f"Rows both kept and mapped: {overlap}")
    dropped = [i for i in OLD_IDS if i not in MAPPED and i not in KEPT]

    def values(p):
        return (f"{q(p['name'])}, {q(p['brand'])}, {q(p.get('sku'))}, "
                f"{q(BOT_CATEGORY[p['category']])}, {q(p.get('image'))}")

    lines = [
        "-- Generated by scripts/ftc_catalog_fix.py. One-off fix of the bot's FTC catalog:",
        "-- verified names, part numbers and photos from site/data/parts-catalog.json.",
        "-- Row ids stay, so listings keep their part. Fails if a dropped row is in use.",
        "begin;",
        "",
        "do $$ begin",
        "  if exists (select 1 from listings where have_part_id in ({0}) or want_part_id in ({0})) then".format(
            ", ".join(map(str, dropped))),
        "    raise exception 'a part that would be dropped is used by a listing';",
        "  end if;",
        "end $$;",
        "",
        f"delete from parts where program = 'FTC' and id in ({', '.join(map(str, dropped))});",
        "",
    ]
    for bot_id, site_id in MAPPED.items():
        p = parts[site_id]
        lines.append(
            f"update parts set name = {q(p['name'])}, brand = {q(p['brand'])}, sku = {q(p.get('sku'))}, "
            f"category = {q(BOT_CATEGORY[p['category']])}, image = {q(p.get('image'))} "
            f"where id = {bot_id} and program = 'FTC';")
    lines.append("")
    for bot_id, fix in KEPT_FIXES.items():
        sets = ", ".join(f"{k} = {q(v)}" for k, v in fix.items())
        lines.append(f"update parts set {sets} where id = {bot_id} and program = 'FTC';")
    lines += ["", "insert into parts (name, brand, sku, category, image, program) values"]
    rest = [p for pid, p in parts.items() if pid not in set(MAPPED.values())]
    lines.append(",\n".join(f"  ({values(p)}, 'FTC')" for p in rest))
    lines += ["on conflict (name, coalesce(brand, '')) do nothing;", "", "commit;", ""]
    MIGRATION.write_text("\n".join(lines), encoding="utf-8")

    print(f"mapped {len(MAPPED)}, kept {len(KEPT)}, dropped {len(dropped)}, added {len(rest)}")


if __name__ == "__main__":
    main()
