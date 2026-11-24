# LEGO SPIKE catalog: sources and notes

Checked 2026-11-24. Every number below was read from an education.lego.com page loaded with curl. All www.lego.com pages (shop, service/help, replacement parts) returned HTTP 403 to curl and WebFetch, so nothing in the catalog relies on lego.com.

## How facts were confirmed
- **Product pages:** For each product page, the number, name and first gallery image come from the page's schema.org Product JSON-LD (`productID`, `name`, `image[0]`). SPIKE product pages have no og:image, so `image[0]` is used. Images take `&width=640`, and each one returned HTTP 200 with an image/* content type when fetched with curl and no Referer.
- **Product list:** The education.lego.com sitemap (https://education.lego.com/sitemap/sitemap-0.xml) gave the list of product pages.
- **FAQ cross-check:** The official FAQ lists of "products in the SPIKE family" were used to check the product list and to place each item in a kit.

## Sources per item
| Number | Source |
|---|---|
| 45678 | https://education.lego.com/en-us/products/lego-education-spike-prime-set/45678/ |
| 45681 | https://education.lego.com/en-us/products/lego-education-spike-prime-expansion-set/45681/ |
| 45680 | https://education.lego.com/en-us/support/product-images/ (lists "SKU 6254343, Part 45680, LEGO Technic SPIKE Prime Expansion Set"). The URL .../products/lego-education-spike-prime-expansion-set/45680/ redirects to 45681, so 45680 looks like the earlier version of the expansion set that 45681 replaced. |
| 5007439 | https://education.lego.com/en-us/products/spike-prime-class-pack/5007439/ (15 Prime sets + 30 Personal Learning Kits) |
| 5008796 | https://education.lego.com/en-us/products/spike-prime-combo-pack/5008796/ (15 Prime sets + 15 Expansion sets) |
| 45345 | https://education.lego.com/en-us/products/lego-education-spike-essential-set/45345/ |
| 5007438 | https://education.lego.com/en-us/products/spike-essential-class-pack/5007438/ |
| 45601 | https://education.lego.com/en-us/products/lego-technic-large-hub-for-spike-prime-/45601/ |
| 45609 | https://education.lego.com/en-us/products/lego-technic-small-hub/45609/ |
| 45602 | https://education.lego.com/en-us/products/lego-technic-large-angular-motor/45602/ |
| 45603 | https://education.lego.com/en-us/products/lego-technic-medium-angular-motor/45603/ |
| 45607 | https://education.lego.com/en-us/products/lego-technic-small-angular-motor/45607/ (page says it works with both the Small Hub 45609 and the Large Hub 45601) |
| 45604 | https://education.lego.com/en-us/products/lego-technic-distance-sensor/45604/ |
| 45605 | https://education.lego.com/en-us/products/lego-technic-color-sensor/45605/ (in both the Prime and Essential FAQ family lists) |
| 45606 | https://education.lego.com/en-us/products/lego-technic-force-sensor/45606/ |
| 45610 | https://education.lego.com/en-us/products/lego-technic-large-hub-battery/45610/ |
| 45612 | https://education.lego.com/en-us/products/lego-technic-small-hub-battery/45612/ |
| 45611 | https://education.lego.com/en-us/products/lego-technic-micro-usb-connector-cable/45611/ (both FAQs say it ships with the set and is sold separately) |
| 45608 | https://education.lego.com/en-us/products/lego-technic-color-light-matrix/45608/ |
| 2000719 | https://education.lego.com/en-us/products/lego-education-spike-prime-replacement-pack-/2000719/ |
| 2000722 | https://education.lego.com/en-us/products/lego-education-spike-essential-replacement-pack-1/2000722/ |
| 2000723 | https://education.lego.com/en-us/product-resources/45345-spike-essential-resource-page/troubleshooting/spike-essential-faqs/ (FAQ list only, no product page) |
| 2000727 | https://education.lego.com/en-us/products/lego-education-spike-essential-minifigures/2000727/ |
| 2000480 / 2000481 | https://education.lego.com/en-us/product-resources/spike-prime/troubleshooting/spike-prime-faqs/ and the SPIKE Essential FAQ (described as hybrid-learning "Personal Learning Kits"; no product page) |

**FAQ family lists:**
- Prime: https://education.lego.com/en-us/product-resources/spike-prime/troubleshooting/spike-prime-faqs/ says "1 core set and 10 supplement SKUs": 45681, 45601-45606, 45610, 45611, 2000719.
- Essential: https://education.lego.com/en-us/product-resources/45345-spike-essential-resource-page/troubleshooting/spike-essential-faqs/ says "1 core set and 7 supplemental SKUs": 45605, 45607, 45608, 45609, 45612, 2000722, 2000723. The FAQ prints the Small Hub Battery as "456012", which is a typo. The product page confirms 45612.

## Caveats
- **Retirement:** All SPIKE product pages are now marked `Discontinued` in their structured data. The 45678 and 45345 pages say SPIKE Prime and SPIKE Essential retired on 30 June 2026. Listings will be second-hand or old stock.
- **No images (null):** 45680, 2000723, 2000480 and 2000481 have no LEGO product page.
  - The support page for 45680 links a full-size LEGO CDN image (le-www-live-s.legocdn.com, Products/45680/45680_Prod_01). It is 14.7 MB at 6530x9184 and ignores width parameters, so it was not used.
- **Prime small motor:** No separate Small Motor exists for SPIKE Prime. The only small motor is 45607, which belongs to SPIKE Essential.
- **Light Matrix category:** 45608 is filed under `other` because it is an output device, not a sensor.
- **Not included:**
  - **Excluded, not SPIKE:** These come from the new LEGO Education Computer Science & AI and Science lines and use USB-C. None of their pages mention SPIKE.
    - 45650 Single Motor, 45651 Double Motor, 45652 Controller, 45653 Color Sensor, 45657 Connection Cards
    - 45623/45624 Multi-charger, 45656 AC Cable
    - 45545-45547 and 45654/45655 Replacement Packs
  - **Generic storage:** 45495 Small Sorting Top Trays and 45496 Medium Storage are generic LEGO Education storage. Their pages say only that they are "similar to" the SPIKE trays and boxes.
  - **BricQ Motion:** 45400/45401 and 2000470/2000471 are not SPIKE.
  - **Unconfirmed:** Nothing else was found on an official page. The individual-element spare-parts pages on lego.com could not be loaded.
