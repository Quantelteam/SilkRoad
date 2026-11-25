# LEGO EV3 and FLL Challenge field catalog: sources

Companion to `lego-ev3-field.json` (23 items: 16 EV3, 7 FLL Challenge season sets). Every number below was read on an official page or file loaded on 2026-11-25. www.lego.com returned 403, so no lego.com pages were used.

## Main sources

- **[P] LEGO Education "Product Images" page**: https://education.lego.com/en-us/support/product-images/
  Lists each item as "SKU: <internal code> | Part: <item number>" plus a name. The **Part** value is the item number used here. The SKU column (for example 6034300 for the brick) is an internal code, not the box number, and is not used.
- **[C] EV3 Core Set product page (retired)**: https://education.lego.com/en-us/products/lego-mindstorms-education-ev3-core-set/5003400/
  Shows the US bundle number **5003400** (status "Retired - contact us"). It is the same set as 45544 and is kept as an alias.
- **[W] EV3 "What's In the Box" page**: https://education.lego.com/en-us/product-resources/mindstorms-ev3/downloads/whats-in-the-box/
  Says "MINDSTORMS EV3 Core Set (45544)", "Expansion Set (45560)" and "Space Challenge (45570)".
- **[R] Retired EV3 curriculum downloads**: https://education.lego.com/en-us/downloads/retiredproducts/mindstorms-ev3/curriculum/
  Says "EV3 Core Set (45544)", "EV3 Space Challenge Set (45570)" and "Temperature Sensor (9749)".
- **[F] FIRST past challenges page**: https://www.firstinspires.org/resources/library/fll/past-challenges
  Has a section for each season (e.g. "2025/2026 - UNEARTHED") that links the season's building-instruction PDFs on firstinspires.blob.core.windows.net. The set number is printed in those PDFs.

## EV3 items

| id | name | number confirmed on |
|---|---|---|
| lego-45544 | LEGO MINDSTORMS Education EV3 Core Set | [P] "Part: 45544 LEGO MINDSTORMS Core Set"; [W]; [R]. US bundle 5003400 on [C] |
| lego-45560 | LEGO MINDSTORMS Education EV3 Expansion Set | [P] "Part: 45560 LEGO MINDSTORMS Expansion Set"; [W] |
| lego-45570 | LEGO MINDSTORMS Education EV3 Space Challenge Set | [P] "Part: 45570 EV3 Space Challenge Set"; [W]; [R] |
| lego-45500 | EV3 Intelligent Brick | [P] "Part: 45500 EV3 Intelligent Brick" |
| lego-45501 | EV3 Rechargeable DC Battery | [P] "Part: 45501 EV3 Rechargeable DC Battery" |
| lego-45502 | EV3 Large Servo Motor | [P] "Part: 45502 EV3 Large Servo Motor" |
| lego-45503 | EV3 Medium Servo Motor | [P] "Part: 45503 EV3 Medium Servo Motor" |
| lego-45504 | EV3 Ultrasonic Sensor | [P] "Part: 45504 EV3 Ultrasonic Sensor" |
| lego-45505 | EV3 Gyro Sensor | [P] "Part: 45505 EV3 Gyro Sensor" |
| lego-45506 | EV3 Color Sensor | [P] "Part: 45506 EV3 Color Sensor" |
| lego-45507 | EV3 Touch Sensor | [P] "Part: 45507 EV3 Touch Sensor" |
| lego-45508 | EV3 Infrared Beacon | [P] "Part: 45508 EV3 Infrared Beacon" |
| lego-45509 | EV3 Infrared Sensor | [P] "Part: 45509 EV3 Infrared Sensor" |
| lego-45514 | EV3 Cable Pack | [P] "Part: 45514 EV3 Cable Pack" |
| lego-45517 | EV3 Transformer 10V DC | [P] "Part: 45517 EV3 Transformer 10V DC" |
| lego-9749 | EV3 Temperature Sensor | [P] "Part: 9749 EV3 Temperature Sensor"; also [R] "Temperature Sensor (9749)" |

## FLL Challenge season sets

Season headings come from [F]. Each set number was checked in the linked PDF, which is listed in that season's section of [F].

| id | season | evidence |
|---|---|---|
| lego-45829 | UNEARTHED 2025/2026 | https://firstinspires.blob.core.windows.net/fll/challenge/2025-26/fll-challenge-unearthed-prepack-nonverbal.pdf: "45829" printed on the pre-pack overview (PDF text) |
| lego-45826 | SUBMERGED 2024/2025 | https://firstinspires.blob.core.windows.net/fll/challenge/2024-25/fll-challenge-submerged-bi-prepack-nonverbal.pdf: "45826" printed on the pre-pack overview (PDF text) |
| lego-45823 | MASTERPIECE 2023/2024 | https://firstinspires.blob.core.windows.net/fll/challenge/2023-24/NonVerbal%20Challenge%20BI/fll-challenge-masterpiece-45823-bi-prepack-nonverbal.pdf: "45823" printed in the PDF and in the file name |
| lego-45820 | SUPERPOWERED 2022/2023 | https://firstinspires.blob.core.windows.net/fll/challenge/2022-23/building-instructions/nonverbal/fll-challenge-superpowered-45820-model-prepack-web-nonverbal.pdf: "45820" printed in the PDF and in the file name |
| lego-45816 | CARGO CONNECT 2021/2022 | https://firstinspires.blob.core.windows.net/fll/challenge/2021-22/building-instructions/nonverbal/fll-challenge-cargo-connect-45816-Book1-3104-web-nonverbal.pdf: "45816" printed next to the LEGO Education and FLL Challenge logos on page 1 (checked visually) |
| lego-45813 | RePLAY 2020/2021 | https://firstinspires.blob.core.windows.net/fll/challenge/2020-21/non-verbal-building-instructions/NonVerbal.zip: The zip holds 45813_Book1..9, EOP, model and pre-pack PDFs. "45813" is printed on the cover of 45813_Book1_3104_Web_NonVerbal.pdf next to the LEGO Education and FLL Challenge logos (checked visually) |
| lego-45809 | CITY SHAPER 2019/2020 | https://firstinspires.blob.core.windows.net/fll/challenge/2019-20/mission-models/non-verbal/45809_Book1_NonVerbal_19August2019.pdf: Weaker evidence: "45809" is in every CITY SHAPER build-file name linked from [F] and in the PDF text layer as the document name "45809_Book1_NonVerbal.indd", but it is not printed in the artwork. Included because FIRST names the files by set number |

The JSON `url` for every season set is the [F] page.

## Images

- **lego-45544**: `https://assets.education.lego.com/v3/assets/blt293eea581807678a/bltb66bc8c585667ccb/5f50d2dc35453c33adce90e5/5003400_1050x1050_1_xx-xx.jpg?locale=en-us&width=640`. This is the main image in the [C] page's product JSON-LD. Fetched with curl (no Referer): HTTP 200, image/png, 640x640.
- **All other items: `image` is null.** The only official product photos for the EV3 elements are on [P], and they are hosted on `le-www-live-s.legocdn.com` (LEGO Education's CDN), not `assets.education.lego.com`. Each returned HTTP 200 with an image content type via curl with no Referer. They ignore `?width=` and are full size (about 0.1 to 9 MB). They are listed below in case you accept that host:
  - 45560: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45560/45560_1050x1050_1_xx-xx/ee59edd314747f1a4c788cc528ae7243/8f52d453-5297-4a6f-85c2-a58d00d7ccdc/original/8f52d453-5297-4a6f-85c2-a58d00d7ccdc/8f52d453-5297-4a6f-85c2-a58d00d7ccdc.jpg?output-format=jpg
  - 45570: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45570/45570_1050x1050_1_xx-xx/8a98a4814dde3332349a196021945e5b/4a6dacbb-0be6-4213-a35a-a58d00d7d376/original/4a6dacbb-0be6-4213-a35a-a58d00d7d376/4a6dacbb-0be6-4213-a35a-a58d00d7d376.jpg?output-format=jpg
  - 45500: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45500/45500_prod_P-brik_01_left/7ebc44b2a0e93783badb7dcfba86cc17/0ce5a65d-ff65-427e-b41a-a50900cfea74/original/0ce5a65d-ff65-427e-b41a-a50900cfea74/0ce5a65d-ff65-427e-b41a-a50900cfea74.jpg?output-format=jpg
  - 45501: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45501/45501_prod_rechargeble_batt_01_left/07e5a34f73cd58ad101e23c59488717c/2b6224dc-5b0c-4d64-852c-a50c00662c44/original/2b6224dc-5b0c-4d64-852c-a50c00662c44/2b6224dc-5b0c-4d64-852c-a50c00662c44.jpg?output-format=jpg
  - 45502: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45502/45502_prod_L_motor_01_left/cc9b4aae26bc35ad7ed701d2eab4c56a/2c3cd013-efc3-48fb-a62e-a50c006bdf25/original/2c3cd013-efc3-48fb-a62e-a50c006bdf25/2c3cd013-efc3-48fb-a62e-a50c006bdf25.jpg?output-format=jpg
  - 45503: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45503/45503_prod_M_motor_01_left/6823ba8c93306237ff7b426f7483b864/2f66b65e-2854-4b25-8aa0-a50c007159e9/original/2f66b65e-2854-4b25-8aa0-a50c007159e9/2f66b65e-2854-4b25-8aa0-a50c007159e9.jpg?output-format=jpg
  - 45504: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45504/45504_prod_ultrasonic_sensor_01_left/a9cb3286848b4943f9cad0f463be58fd/1a193bcc-9718-4bb3-91cc-a50c00715c78/original/1a193bcc-9718-4bb3-91cc-a50c00715c78/1a193bcc-9718-4bb3-91cc-a50c00715c78.jpg?output-format=jpg
  - 45505: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45505/45505_prod_gyro_sensor_01_left/0dcc4402abc3d4a1aa520d9be57d17d7/49358a65-7630-4c20-a92c-a50c00716061/original/49358a65-7630-4c20-a92c-a50c00716061/49358a65-7630-4c20-a92c-a50c00716061.jpg?output-format=jpg
  - 45506: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45506/45506_prod_Colour_sensor_01_left/ffeca02e3e49938ebe178bb4bad5422c/ed9f0177-aa02-4dce-9214-a50c007179a5/original/ed9f0177-aa02-4dce-9214-a50c007179a5/ed9f0177-aa02-4dce-9214-a50c007179a5.jpg?output-format=jpg
  - 45507: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45507/45507_prod_touch_sensor_01_left/68aa5d0ded2dbf5e42d8ded761b26e07/5e94ddcc-bd54-4b03-a5d2-a50c0080aaed/original/5e94ddcc-bd54-4b03-a5d2-a50c0080aaed/5e94ddcc-bd54-4b03-a5d2-a50c0080aaed.jpg?output-format=jpg
  - 45508: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45508/45508_prod_IR_beacon_01_left/d051f38aa9a6bf5db4a5a563d1cb73/457a0a7a-862f-4492-853a-a50c0080b728/original/457a0a7a-862f-4492-853a-a50c0080b728/457a0a7a-862f-4492-853a-a50c0080b728.jpg?output-format=jpg
  - 45509: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45509/45509_prod_IR_sensor_01_left/45079d75ab7b5edc6d027a7c4d998bd2/21a870f0-fbb3-4b7c-9ae7-a50c0080bc55/original/21a870f0-fbb3-4b7c-9ae7-a50c0080bc55/21a870f0-fbb3-4b7c-9ae7-a50c0080bc55.jpg?output-format=jpg
  - 45514: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45514/45514_prod_cable_pack_01_left_a/94aed5b384e7deab0242d1cf9f0058/ab1e6370-3c28-4ec7-aa16-a50c0080c2f3/original/ab1e6370-3c28-4ec7-aa16-a50c0080c2f3/ab1e6370-3c28-4ec7-aa16-a50c0080c2f3.jpg?output-format=jpg
  - 45517: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/45517/45517_1050x1050_1_xx-xx/6b0288b647593d57904cd5634eba8dea/cc673cd6-8036-4d4c-ae7d-a58700e4ccdf/original/cc673cd6-8036-4d4c-ae7d-a58700e4ccdf/cc673cd6-8036-4d4c-ae7d-a58700e4ccdf.jpg?output-format=jpg
  - 9749: https://le-www-live-s.legocdn.com/images/images/423923/live/sc/Products/9749/9749_prod_temperature_sensor_01/b7246060dc045afd4bc0ac964ad51421/fda4e0bc-326d-45a0-9ce2-a50800d62d96/original/fda4e0bc-326d-45a0-9ce2-a50800d62d96/fda4e0bc-326d-45a0-9ce2-a50800d62d96.jpg?output-format=jpg
- **FLL season sets**: firstinspires.org only has season logos (for example `/hubfs/submerged.png`), not product photos of the sets, so `image` is null.

## Left out or uncertain

- **BIOGLOW (2026/2027, current season)**: the season is confirmed on https://education.lego.com/en-us/first-lego-league/season-materials/ and the FIRST season-materials page. However, its building PDFs (`https://firstinspires.blob.core.windows.net/fll/challenge/2026-27/fll-challenge-bioglow-bi-enus-*.pdf`) show no set number in text, file names or artwork (checked book 01 and the pre-pack). No number was found, so it is left out.
- **Older Challenge sets with file-name-only evidence (not in JSON)**: FIRST's zip downloads on [F] use these numbers in their internal file names, but no page or printed artwork states them:
  - INTO ORBIT 2018/19: 45806 (`2018-19/mission-models/BuildInstructions-Nonverbal.zip`, files 45806_Bag_*.pdf, PDF title "45806_EOP_ENG.indd")
  - HYDRO DYNAMICS 2017/18: 45804 (`2017-18/fll-2017-build/NonVerbal.zip`, 45804_Bag_*.pdf)
  - ANIMAL ALLIES 2016/17: 45802 (`2016-17/mission-models.zip`, 45802_Bag*.pdf)
  - TRASH TREK 2015/16: 45801 (`2015-16/trash-trek-mission-model-build.zip`, 45801_Bag*.pdf)
  - NATURE'S FURY 2013/14: 9664 (`2013-14/natures-fury-mission-model.zip`, 9664_Bag_*_US.pdf)
  - WORLD CLASS 2014/15: no number in its zip file names or in the Bag 1 PDF text.
  Add these only if file-name evidence is enough for you.
- **Official FLL table or mat sold with its own number**: none found. LEGO Education and FIRST publish only table building instructions and mat files.
- **Out of scope but seen**: FLL Discover/Explore sets in FIRST file names (45818 Discover CARGO CONNECT, 45821 Explore SUPERPOWERED, 45822 Discover SUPERPOWERED). Also the Renewable Energy Add-on Set 9688 (NXT-era, used by the EV3 science curriculum on [R]).
- **Not listed by LEGO Education with a number**: EV3 USB cable, any Wi-Fi dongle and the retail (home edition) EV3 set. None appear on [P].
- **Naming**: the names use LEGO Education's spelling from [P] ("EV3 Large Servo Motor", "EV3 Transformer 10V DC"). For the three sets, the "LEGO MINDSTORMS Education EV3 ..." prefix is added to match [C] and [W]. [P] itself says "LEGO MINDSTORMS Core Set" and "LEGO MINDSTORMS Expansion Set".
- **Categories**: the Space Challenge Set (45570) is "other" because it has no electronics and is not an FLL item. The IR Beacon (45508) is "other" because it is a transmitter, not a sensor. The Temperature Sensor (9749) is "sensors": LEGO Education calls it "EV3 Temperature Sensor", although it began as an NXT-era sensor.
