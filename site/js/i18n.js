// Interface language: Kazakh, Russian or English.
// Every interface string lives in DICT below. The HTML keeps the English text as a
// fallback and marks each string with data-i18n* attributes; applyStatic() swaps it.
// Part names, brands, SKUs, team names, cities and users' notes are never translated.
//
// The language is picked once per page load: ?lang=, then the saved choice, then the
// browser's languages, else English. Switching saves the choice and reloads.

export const LANGS = /** @type {const} */ (['kk', 'ru', 'en']);
const STORAGE_KEY = 'almasu-lang';

/** BCP 47 locale per language, for dates. */
const LOCALES = { en: 'en-GB', ru: 'ru-RU', kk: 'kk-KZ' };

/**
 * A plural entry is an object of Intl.PluralRules categories. Russian uses
 * one / few / many; Kazakh nouns stay singular after a number, so it needs one form.
 * @typedef {{ one?: string, few?: string, many?: string, other: string }} PluralForms
 */

/** @type {Record<'en'|'ru'|'kk', Record<string, string | PluralForms>>} */
export const DICT = {
  en: {
    // Page titles and descriptions
    'meta.landing.title': 'Almasu: buy, sell, exchange robot parts',
    'meta.landing.description': 'Almasu is where FTC and FLL teams in Kazakhstan buy, sell and exchange spare robot parts: goBILDA, REV, Studica, LEGO SPIKE and more. Post through the Telegram bot, find parts here, agree in a private chat.',
    'meta.listings.title': 'Listings, Almasu',
    'meta.listings.description': 'Find spare robot parts from FTC and FLL teams across Kazakhstan: goBILDA, REV, Studica, LEGO SPIKE and more. Message the team on Telegram to trade, buy or pick up for free.',
    'meta.catalog.title': 'Parts catalog, Almasu',
    'meta.catalog.description': 'Standard names and part numbers for common FTC parts (goBILDA, REV Robotics, Studica and others) and FLL parts (LEGO Education SPIKE), with the listings for each part.',
    'meta.og.description': 'Spare FTC parts from teams across Kazakhstan. Search by part, city or team, then message the team on Telegram.',

    // Shared chrome
    'skip.content': 'Skip to content',
    'skip.listings': 'Skip to listings',
    'skip.catalog': 'Skip to catalog',
    'nav.main': 'Main',
    'nav.listings': 'Listings',
    'nav.catalog': 'Parts catalog',
    'nav.how': 'How it works',
    'lang.group': 'Language',
    'common.close': 'Close',
    'common.all': 'All',
    'program.group': 'Program',
    'footer.payments': 'Almasu doesn’t handle payments or delivery. Teams agree on both in Telegram.',
    'footer.photosLanding': 'Catalog photos load from the part maker’s website and belong to that maker.',
    'footer.photosListings': 'Pictures marked “Catalog photo” load from the part maker’s website and belong to that maker. They show the product, not the team’s actual part.',
    'footer.photosCatalog': 'Product photos load from each maker’s own website and belong to that maker. Each part name links to its product page.',
    'footer.partNumbers': 'Part numbers are copied from the vendors’ sites. If one is wrong or a part is missing, tell the channel admins.',
    'footer.community1': 'A community project by FTC teams in Kazakhstan. Not affiliated with',
    'footer.community2': ', LEGO®, goBILDA, REV Robotics or Studica.',
    'footer.credit': 'by FTC team Quattuor #24881',

    // How it works
    'how.title': 'How it works',
    'how.step1.title': 'Post in the Telegram bot',
    'how.step1.landing': 'The bot asks what you have, what you want for it, and for a photo. No photo? Use the official catalog one. Your team name and city come from your team’s registration.',
    'how.step1.listings': 'The bot asks what you have, what you want for it, and for a photo. Your team name, city and Telegram username come from your team’s registration.',
    'how.step2.title': 'Teams find it here',
    'how.step2.text': 'Every active listing shows on this site. Anyone can search by part, city or team, without an account.',
    'how.step3.title': 'Agree in a private chat',
    'how.step3.text': 'Tap Message on a listing to open a Telegram chat with that team. You agree on the price and the hand-over between yourselves.',
    'bot.ctaBefore': 'To post a part, open ',
    'bot.ctaAfter': ' in Telegram.',
    'bot.missing': 'The posting bot isn’t public yet. Ask in the FTC Kazakhstan parts channel for the link.',

    // Landing
    'landing.eyebrow': 'FTC · FLL · Kazakhstan',
    'landing.slogan': 'Buy. Sell. Exchange.',
    'landing.sub': 'Spare robot parts between FTC and FLL teams across Kazakhstan. Find the part here, then settle it with the team in a Telegram chat.',
    'landing.browse': 'Browse listings',
    'landing.post': 'Post through the bot',
    'landing.searchLabel': 'Looking for something?',
    'intro.open': 'Watch the 30-second intro',
    'intro.label': 'Almasu intro video',
    'intro.pause': 'Pause',
    'intro.play': 'Play',
    'intro.soundOn': 'Sound on',
    'intro.soundOff': 'Sound off',
    'stats.label': 'Almasu in numbers',
    'stats.listings': { one: 'listing live now', other: 'listings live now' },
    'stats.parts': { one: 'part in the catalog', other: 'parts in the catalog' },
    'stats.brands': { one: 'brand, from goBILDA to LEGO', other: 'brands, from goBILDA to LEGO' },
    'stats.fees': 'fees: teams deal directly',
    'latest.title': 'Fresh on the exchange',
    'latest.all': 'All listings →',
    'latest.empty': 'No listings yet. Be the first: post a part through the bot.',
    'programs.label': 'Programs',
    'programs.ftc.title': 'Metal, motors, hubs',
    'programs.ftc.text': 'goBILDA, REV Robotics, Studica, AndyMark, Axon and TETRIX: channels, Yellow Jackets, Control Hubs, servos, wheels and slides.',
    'programs.ftc.link': 'FTC listings →',
    'programs.fll.title': 'LEGO, sets, fields',
    'programs.fll.text': 'SPIKE Prime and Essential, EV3, Technic beams, axles and gears, season sets and field mats.',
    'programs.fll.link': 'FLL listings →',
    'teaser.title': 'One name for every part',
    'teaser.link': 'Open the catalog →',
    'teaser.sub': 'The bot offers parts from a catalog checked against the makers’ sites, so a Yellow Jacket is called the same in every listing. Photos come from the makers.',

    // Listing types, conditions, prices
    'type.trade': 'Trade',
    'type.sell': 'For sale',
    'type.wanted': 'Wanted',
    'type.giveaway': 'Free',
    'condition.new': 'New',
    'condition.like_new': 'Like new',
    'condition.used': 'Used, works',
    'condition.for_parts': 'For parts',
    'price.negotiable': 'Price negotiable',
    'price.free': 'Free',
    'price.budget': 'Budget {price}',
    'price.for': 'For {want}',
    'price.openToOffers': 'Open to offers',
    'want.or': '{item} or {price}',
    'part.fallback': 'Part',
    'verified.title': 'Verified team',
    'verified.label': 'verified team',

    // Listings page
    'listings.title': 'Spare robot parts from FTC and FLL teams across Kazakhstan',
    'listings.sub': 'Find the part, then message the team on Telegram. Trade, buy, or pick it up for free.',
    'listings.searchLabel': 'Search by part, SKU, team or city',
    'listings.demo': 'These are example listings, so the teams and Telegram links are made up. Real listings appear here once teams start posting through the bot.',
    'filters.label': 'Filters',
    'filters.title': 'Filters',
    'filters.clearAll': 'Clear all',
    'filters.close': 'Close filters',
    'filters.type': 'Listing type',
    'filters.city': 'City',
    'filters.anyCity': 'Any city',
    'filters.brand': 'Brand',
    'filters.anyBrand': 'Any brand',
    'filters.category': 'Category',
    'filters.anyCategory': 'Any category',
    'filters.condition': 'Condition',
    'filters.anyCondition': 'Any condition',
    'filters.team': 'Team',
    'filters.anyTeam': 'Any team',
    'filters.showListings': 'Show listings',
    'filters.withCount': 'Filters ({n})',
    'filters.show': { one: 'Show {n} listing', other: 'Show {n} listings' },
    'filters.noMatch': 'No listings match',
    'results.loading': 'Loading listings…',
    'results.someOf': { one: '{shown} of {n} listing', other: '{shown} of {n} listings' },
    'count.listings': { one: '{n} listing', other: '{n} listings' },
    'sort.label': 'Sort',
    'sort.newest': 'Newest first',
    'sort.price': 'Price, low to high',
    'empty.title': 'No listings match',
    'empty.text': 'Try a shorter search or clear a filter. If nobody has the part yet, post a “wanted” listing in the bot so teams who have it can find you.',
    'empty.clear': 'Clear filters',
    'activePart.before': 'Listings with ',
    'activePart.after': '',
    'activePart.showAll': 'Show all parts',
    'photo.listing': 'Listing photo',
    'photo.catalogAlt': '{part}, catalog photo',
    'photo.catalogCaption': 'Catalog photo, {source}',
    'photo.nth': '{title}, photo {n}',
    'photo.creditBefore': 'The photo is the maker’s catalog picture, not this team’s part. Source: ',
    'photo.creditAfter': '.',
    'contact.example': 'Example listing',
    'contact.noUsername': 'No Telegram username',
    'contact.message': 'Message {team}',
    'detail.lookingFor': 'Looking for',
    'detail.has': 'Has',
    'detail.canTrade': 'Can trade',
    'detail.budget': 'Budget',
    'detail.price': 'Price',
    'detail.wants': 'Wants',
    'detail.team': 'Team',
    'detail.city': 'City',
    'detail.condition': 'Condition',
    'detail.partNumber': 'Part number',
    'detail.posted': 'Posted',
    'detail.otherListings': 'Other listings with this part',
    'error.listings': 'Listings didn’t load. Check your connection and reload the page.',

    // Catalog page
    'catalog.title': 'Parts catalog',
    'catalog.sub': 'The bot offers these names when a team posts, so the same motor is called the same thing in every listing. Anything missing can still be posted as free text.',
    'catalog.searchLabel': 'Filter the catalog',
    'catalog.placeholder': 'Part name, part number or nickname',
    'catalog.ftc': 'FTC parts',
    'catalog.fll': 'FLL parts (LEGO)',
    'catalog.brands': 'Brands',
    'brand.other': 'Other',
    'catalog.loading': 'Loading catalog…',
    'catalog.emptyTitle': 'No parts match',
    'catalog.emptyText': 'Try the part number from the vendor’s site, or a shorter name. Parts that aren’t in the catalog can still be posted in the bot as free text.',
    'catalog.total': '{parts} from {brands}',
    'catalog.someOf': { one: '{shown} of {n} part', other: '{shown} of {n} parts' },
    'catalog.noListings': 'No listings',
    'catalog.productPage': 'Product page on the maker’s site',
    'count.parts': { one: '{n} part', other: '{n} parts' },
    'count.brands': { one: '{n} brand', other: '{n} brands' },
    'error.catalog': 'The catalog didn’t load. Check your connection and reload the page.',

    // Dates, for browsers without this language's Intl data
    'age.today': 'today',
    'age.yesterday': 'yesterday',
    'age.daysAgo': { one: '{n} day ago', other: '{n} days ago' },
    'age.date': '{d} {month} {y}',
    'month.0': 'January',
    'month.1': 'February',
    'month.2': 'March',
    'month.3': 'April',
    'month.4': 'May',
    'month.5': 'June',
    'month.6': 'July',
    'month.7': 'August',
    'month.8': 'September',
    'month.9': 'October',
    'month.10': 'November',
    'month.11': 'December',

    // Catalog categories, by id
    'category.sets': 'Complete sets',
    'category.field': 'Field and missions',
    'category.motors': 'Motors',
    'category.servos': 'Servos',
    'category.control': 'Control & Power',
    'category.sensors': 'Sensors',
    'category.batteries': 'Batteries & Chargers',
    'category.structure': 'Structure',
    'category.motion': 'Motion',
    'category.wheels': 'Wheels',
    'category.linear': 'Linear Motion',
    'category.hardware': 'Hardware',
    'category.cables': 'Cables & Connectors',
    'category.other': 'Other',
  },

  ru: {
    'meta.landing.title': 'Almasu: покупка, продажа и обмен деталей для роботов',
    'meta.landing.description': 'Almasu — площадка, где команды FTC и FLL из Казахстана покупают, продают и меняют запасные детали для роботов: goBILDA, REV, Studica, LEGO SPIKE и другие. Публикуйте через Telegram-бота, ищите здесь, договаривайтесь в личном чате.',
    'meta.listings.title': 'Объявления — Almasu',
    'meta.listings.description': 'Запчасти для роботов от команд FTC и FLL со всего Казахстана: goBILDA, REV, Studica, LEGO SPIKE и другие. Напишите команде в Telegram, чтобы обменять, купить или забрать бесплатно.',
    'meta.catalog.title': 'Каталог деталей — Almasu',
    'meta.catalog.description': 'Единые названия и артикулы популярных деталей FTC (goBILDA, REV Robotics, Studica и другие) и FLL (LEGO Education SPIKE) с объявлениями по каждой детали.',
    'meta.og.description': 'Запчасти FTC от команд со всего Казахстана. Ищите по детали, городу или команде и пишите команде в Telegram.',

    'skip.content': 'Перейти к содержимому',
    'skip.listings': 'Перейти к объявлениям',
    'skip.catalog': 'Перейти к каталогу',
    'nav.main': 'Главное меню',
    'nav.listings': 'Объявления',
    'nav.catalog': 'Каталог деталей',
    'nav.how': 'Как это работает',
    'lang.group': 'Язык',
    'common.close': 'Закрыть',
    'common.all': 'Все',
    'program.group': 'Программа',
    'footer.payments': 'Almasu не занимается оплатой и доставкой. Команды договариваются об этом в Telegram.',
    'footer.photosLanding': 'Фото из каталога загружаются с сайта производителя детали и принадлежат ему.',
    'footer.photosListings': 'Снимки с пометкой «Фото из каталога» загружаются с сайта производителя и принадлежат ему. На них товар, а не реальная деталь команды.',
    'footer.photosCatalog': 'Фото товаров загружаются с сайтов производителей и принадлежат им. Название каждой детали ведёт на страницу товара.',
    'footer.partNumbers': 'Артикулы взяты с сайтов производителей. Если какой-то неверен или детали не хватает, напишите администраторам канала.',
    'footer.community1': 'Некоммерческий проект FTC-команд Казахстана. Не связан с',
    'footer.community2': ', LEGO®, goBILDA, REV Robotics и Studica.',
    'footer.credit': 'Сделано FTC-командой Quattuor #24881',

    'how.title': 'Как это работает',
    'how.step1.title': 'Разместите объявление в Telegram-боте',
    'how.step1.landing': 'Бот спросит, что у вас есть, что вы хотите взамен, и попросит фото. Нет фото — возьмите официальное из каталога. Название команды и город подставятся из регистрации команды.',
    'how.step1.listings': 'Бот спросит, что у вас есть, что вы хотите взамен, и попросит фото. Название команды, город и имя в Telegram подставятся из регистрации команды.',
    'how.step2.title': 'Команды находят его здесь',
    'how.step2.text': 'Все активные объявления видны на этом сайте. Искать по детали, городу или команде может любой, без регистрации.',
    'how.step3.title': 'Договоритесь в личном чате',
    'how.step3.text': 'Нажмите «Написать» в объявлении, и откроется чат с командой в Telegram. О цене и передаче вы договариваетесь между собой.',
    'bot.ctaBefore': 'Чтобы разместить деталь, откройте ',
    'bot.ctaAfter': ' в Telegram.',
    'bot.missing': 'Бот для объявлений пока закрыт. Ссылку можно попросить в канале FTC Kazakhstan о запчастях.',

    'landing.eyebrow': 'FTC · FLL · Казахстан',
    'landing.slogan': 'Покупай. Продавай. Меняй.',
    'landing.sub': 'Запчасти для роботов между командами FTC и FLL по всему Казахстану. Найдите деталь здесь и договоритесь с командой в Telegram.',
    'landing.browse': 'Смотреть объявления',
    'landing.post': 'Разместить через бота',
    'landing.searchLabel': 'Что ищете?',
    'intro.open': 'Смотреть видео за 30 секунд',
    'intro.label': 'Видео об Almasu',
    'intro.pause': 'Пауза',
    'intro.play': 'Смотреть',
    'intro.soundOn': 'Включить звук',
    'intro.soundOff': 'Выключить звук',
    'stats.label': 'Almasu в цифрах',
    'stats.listings': { one: 'активное объявление', few: 'активных объявления', many: 'активных объявлений', other: 'активного объявления' },
    'stats.parts': { one: 'деталь в каталоге', few: 'детали в каталоге', many: 'деталей в каталоге', other: 'детали в каталоге' },
    'stats.brands': { one: 'бренд, от goBILDA до LEGO', few: 'бренда, от goBILDA до LEGO', many: 'брендов, от goBILDA до LEGO', other: 'бренда, от goBILDA до LEGO' },
    'stats.fees': 'комиссий: команды договариваются напрямую',
    'latest.title': 'Свежие объявления',
    'latest.all': 'Все объявления →',
    'latest.empty': 'Объявлений пока нет. Будьте первыми: разместите деталь через бота.',
    'programs.label': 'Программы',
    'programs.ftc.title': 'Металл, моторы, хабы',
    'programs.ftc.text': 'goBILDA, REV Robotics, Studica, AndyMark, Axon и TETRIX: швеллеры, Yellow Jacket, Control Hub, сервоприводы, колёса и слайдеры.',
    'programs.ftc.link': 'Объявления FTC →',
    'programs.fll.title': 'LEGO, наборы, поля',
    'programs.fll.text': 'SPIKE Prime и Essential, EV3, балки, оси и шестерни Technic, сезонные наборы и маты для поля.',
    'programs.fll.link': 'Объявления FLL →',
    'teaser.title': 'Одно название для каждой детали',
    'teaser.link': 'Открыть каталог →',
    'teaser.sub': 'Бот предлагает детали из каталога, сверенного с сайтами производителей, поэтому Yellow Jacket во всех объявлениях называется одинаково. Фото — от производителей.',

    'type.trade': 'Обмен',
    'type.sell': 'Продажа',
    'type.wanted': 'Ищу',
    'type.giveaway': 'Даром',
    'condition.new': 'Новое',
    'condition.like_new': 'Как новое',
    'condition.used': 'Б/у, рабочее',
    'condition.for_parts': 'На запчасти',
    'price.negotiable': 'Цена договорная',
    'price.free': 'Бесплатно',
    'price.budget': 'Бюджет {price}',
    'price.for': 'Взамен: {want}',
    'price.openToOffers': 'Рассмотрю предложения',
    'want.or': '{item} или {price}',
    'part.fallback': 'Деталь',
    'verified.title': 'Проверенная команда',
    'verified.label': 'проверенная команда',

    'listings.title': 'Запчасти для роботов от команд FTC и FLL со всего Казахстана',
    'listings.sub': 'Найдите деталь и напишите команде в Telegram. Обменяйте, купите или заберите бесплатно.',
    'listings.searchLabel': 'Поиск по детали, артикулу, команде или городу',
    'listings.demo': 'Это примеры объявлений: команды и ссылки на Telegram выдуманы. Настоящие объявления появятся здесь, когда команды начнут публиковать их через бота.',
    'filters.label': 'Фильтры',
    'filters.title': 'Фильтры',
    'filters.clearAll': 'Сбросить всё',
    'filters.close': 'Закрыть фильтры',
    'filters.type': 'Тип объявления',
    'filters.city': 'Город',
    'filters.anyCity': 'Любой город',
    'filters.brand': 'Бренд',
    'filters.anyBrand': 'Любой бренд',
    'filters.category': 'Категория',
    'filters.anyCategory': 'Любая категория',
    'filters.condition': 'Состояние',
    'filters.anyCondition': 'Любое состояние',
    'filters.team': 'Команда',
    'filters.anyTeam': 'Любая команда',
    'filters.showListings': 'Показать объявления',
    'filters.withCount': 'Фильтры ({n})',
    'filters.show': { one: 'Показать {n} объявление', few: 'Показать {n} объявления', many: 'Показать {n} объявлений', other: 'Показать {n} объявления' },
    'filters.noMatch': 'Ничего не найдено',
    'results.loading': 'Загружаем объявления…',
    'results.someOf': { one: '{shown} из {n} объявления', other: '{shown} из {n} объявлений' },
    'count.listings': { one: '{n} объявление', few: '{n} объявления', many: '{n} объявлений', other: '{n} объявления' },
    'sort.label': 'Сортировка',
    'sort.newest': 'Сначала новые',
    'sort.price': 'Сначала дешёвые',
    'empty.title': 'Подходящих объявлений нет',
    'empty.text': 'Сократите запрос или снимите фильтр. Если детали пока ни у кого нет, разместите в боте объявление «Ищу» — команды, у которых она есть, вас найдут.',
    'empty.clear': 'Сбросить фильтры',
    'activePart.before': 'Объявления с деталью ',
    'activePart.after': '',
    'activePart.showAll': 'Показать все детали',
    'photo.listing': 'Фото объявления',
    'photo.catalogAlt': '{part}, фото из каталога',
    'photo.catalogCaption': 'Фото из каталога, {source}',
    'photo.nth': '{title}, фото {n}',
    'photo.creditBefore': 'Это фото из каталога производителя, а не деталь этой команды. Источник: ',
    'photo.creditAfter': '.',
    'contact.example': 'Пример объявления',
    'contact.noUsername': 'Нет имени в Telegram',
    'contact.message': 'Написать команде {team}',
    'detail.lookingFor': 'Ищет',
    'detail.has': 'Предлагает',
    'detail.canTrade': 'Может дать взамен',
    'detail.budget': 'Бюджет',
    'detail.price': 'Цена',
    'detail.wants': 'Хочет взамен',
    'detail.team': 'Команда',
    'detail.city': 'Город',
    'detail.condition': 'Состояние',
    'detail.partNumber': 'Артикул',
    'detail.posted': 'Опубликовано',
    'detail.otherListings': 'Другие объявления с этой деталью',
    'error.listings': 'Не удалось загрузить объявления. Проверьте подключение и обновите страницу.',

    'catalog.title': 'Каталог деталей',
    'catalog.sub': 'Бот предлагает эти названия, когда команда размещает объявление, поэтому один и тот же мотор везде называется одинаково. Чего нет в каталоге, можно разместить свободным текстом.',
    'catalog.searchLabel': 'Поиск по каталогу',
    'catalog.placeholder': 'Название, артикул или прозвище',
    'catalog.ftc': 'Детали FTC',
    'catalog.fll': 'Детали FLL (LEGO)',
    'catalog.brands': 'Бренды',
    'brand.other': 'Другое',
    'catalog.loading': 'Загружаем каталог…',
    'catalog.emptyTitle': 'Ничего не найдено',
    'catalog.emptyText': 'Попробуйте артикул с сайта производителя или название покороче. Деталь, которой нет в каталоге, всё равно можно разместить в боте свободным текстом.',
    'catalog.total': '{parts}, {brands}',
    'catalog.someOf': { one: '{shown} из {n} детали', other: '{shown} из {n} деталей' },
    'catalog.noListings': 'Нет объявлений',
    'catalog.productPage': 'Страница товара на сайте производителя',
    'count.parts': { one: '{n} деталь', few: '{n} детали', many: '{n} деталей', other: '{n} детали' },
    'count.brands': { one: '{n} бренд', few: '{n} бренда', many: '{n} брендов', other: '{n} бренда' },
    'error.catalog': 'Не удалось загрузить каталог. Проверьте подключение и обновите страницу.',

    // Dates, for browsers without this language's Intl data
    'age.today': 'сегодня',
    'age.yesterday': 'вчера',
    'age.daysAgo': { one: '{n} день назад', few: '{n} дня назад', many: '{n} дней назад', other: '{n} дня назад' },
    'age.date': '{d} {month} {y} г.',
    'month.0': 'января',
    'month.1': 'февраля',
    'month.2': 'марта',
    'month.3': 'апреля',
    'month.4': 'мая',
    'month.5': 'июня',
    'month.6': 'июля',
    'month.7': 'августа',
    'month.8': 'сентября',
    'month.9': 'октября',
    'month.10': 'ноября',
    'month.11': 'декабря',

    'category.sets': 'Готовые наборы',
    'category.field': 'Поле и миссии',
    'category.motors': 'Моторы',
    'category.servos': 'Сервоприводы',
    'category.control': 'Управление и питание',
    'category.sensors': 'Датчики',
    'category.batteries': 'Аккумуляторы и зарядки',
    'category.structure': 'Конструкция',
    'category.motion': 'Передачи',
    'category.wheels': 'Колёса',
    'category.linear': 'Линейное движение',
    'category.hardware': 'Крепёж',
    'category.cables': 'Кабели и разъёмы',
    'category.other': 'Другое',
  },

  kk: {
    'meta.landing.title': 'Almasu: робот бөлшектерін сату, сатып алу және айырбастау',
    'meta.landing.description': 'Almasu — Қазақстандағы FTC және FLL командалары артық робот бөлшектерін сатып, сатып алып, айырбастайтын алаң: goBILDA, REV, Studica, LEGO SPIKE және басқалары. Telegram-бот арқылы жариялаңыз, бөлшекті осы жерден табыңыз, жеке чатта келісіңіз.',
    'meta.listings.title': 'Хабарландырулар — Almasu',
    'meta.listings.description': 'Қазақстан бойынша FTC және FLL командаларының артық робот бөлшектері: goBILDA, REV, Studica, LEGO SPIKE және басқалары. Айырбастау, сатып алу немесе тегін алу үшін командаға Telegram-да жазыңыз.',
    'meta.catalog.title': 'Бөлшектер каталогы — Almasu',
    'meta.catalog.description': 'FTC (goBILDA, REV Robotics, Studica және басқалары) және FLL (LEGO Education SPIKE) бөлшектерінің бірыңғай атаулары мен артикулдары, әр бөлшек бойынша хабарландырулар.',
    'meta.og.description': 'Қазақстан бойынша командалардың артық FTC бөлшектері. Бөлшек, қала немесе команда бойынша іздеп, командаға Telegram-да жазыңыз.',

    'skip.content': 'Негізгі мазмұнға өту',
    'skip.listings': 'Хабарландыруларға өту',
    'skip.catalog': 'Каталогқа өту',
    'nav.main': 'Негізгі мәзір',
    'nav.listings': 'Хабарландырулар',
    'nav.catalog': 'Бөлшектер каталогы',
    'nav.how': 'Қалай жұмыс істейді',
    'lang.group': 'Тіл',
    'common.close': 'Жабу',
    'common.all': 'Барлығы',
    'program.group': 'Бағдарлама',
    'footer.payments': 'Almasu төлем мен жеткізумен айналыспайды. Командалар екеуін де Telegram-да өзара келіседі.',
    'footer.photosLanding': 'Каталог суреттері бөлшек өндірушісінің сайтынан жүктеледі және сол өндірушіге тиесілі.',
    'footer.photosListings': '«Каталог суреті» деп белгіленген суреттер өндірушінің сайтынан жүктеледі және соған тиесілі. Оларда команданың нақты бөлшегі емес, тауардың өзі көрсетілген.',
    'footer.photosCatalog': 'Тауар суреттері әр өндірушінің өз сайтынан жүктеледі және соған тиесілі. Әр бөлшектің атауы тауар бетіне апарады.',
    'footer.partNumbers': 'Артикулдар өндірушілердің сайттарынан алынған. Қате тапсаңыз немесе бөлшек жетіспесе, арна әкімшілеріне жазыңыз.',
    'footer.community1': 'Қазақстандағы FTC командаларының коммерциялық емес жобасы.',
    'footer.community2': ', LEGO®, goBILDA, REV Robotics және Studica компанияларына қатысы жоқ.',
    'footer.credit': 'Жасаған: FTC Quattuor #24881 командасы',

    'how.title': 'Қалай жұмыс істейді',
    'how.step1.title': 'Telegram-ботта хабарландыру беріңіз',
    'how.step1.landing': 'Бот сізде не бар екенін, орнына не қалайтыныңызды сұрап, сурет сұрайды. Сурет жоқ па? Каталогтағы ресми суретті алыңыз. Команда атауы мен қала команданың тіркеуінен алынады.',
    'how.step1.listings': 'Бот сізде не бар екенін, орнына не қалайтыныңызды сұрап, сурет сұрайды. Команда атауы, қала және Telegram аты команданың тіркеуінен алынады.',
    'how.step2.title': 'Командалар оны осы жерден табады',
    'how.step2.text': 'Барлық белсенді хабарландыру осы сайтта көрінеді. Бөлшек, қала немесе команда бойынша кез келген адам тіркелмей-ақ іздей алады.',
    'how.step3.title': 'Командамен Telegram-да келісіңіз',
    'how.step3.text': 'Хабарландырудағы «Жазу» батырмасын басыңыз, сол командамен Telegram чаты ашылады. Баға мен бөлшекті қалай беретініңізді өзара келісесіздер.',
    'bot.ctaBefore': 'Бөлшекті жариялау үшін Telegram-да ',
    'bot.ctaAfter': ' ботын ашыңыз.',
    'bot.missing': 'Хабарландыру боты әзірге жабық. Сілтемені FTC Kazakhstan бөлшектер арнасынан сұраңыз.',

    'landing.eyebrow': 'FTC · FLL · Қазақстан',
    'landing.slogan': 'Сат. Сатып ал. Айырбаста.',
    'landing.sub': 'Қазақстандағы FTC және FLL командалары арасында робот бөлшектерімен алмасу. Бөлшекті осы жерден тауып, командамен Telegram-да келісіңіз.',
    'landing.browse': 'Хабарландыруларды қарау',
    'landing.post': 'Бот арқылы жариялау',
    'landing.searchLabel': 'Не іздеп жүрсіз?',
    'intro.open': '30 секундтық бейнені көру',
    'intro.label': 'Almasu туралы бейне',
    'intro.pause': 'Кідірту',
    'intro.play': 'Ойнату',
    'intro.soundOn': 'Дыбысты қосу',
    'intro.soundOff': 'Дыбысты өшіру',
    'stats.label': 'Almasu сандармен',
    'stats.listings': { other: 'белсенді хабарландыру' },
    'stats.parts': { other: 'бөлшек каталогта' },
    'stats.brands': { other: 'бренд, goBILDA-дан LEGO-ға дейін' },
    'stats.fees': 'комиссия: командалар тікелей келіседі',
    'latest.title': 'Жаңа хабарландырулар',
    'latest.all': 'Барлық хабарландыру →',
    'latest.empty': 'Әзірге хабарландыру жоқ. Бірінші болыңыз: бөлшекті бот арқылы жариялаңыз.',
    'programs.label': 'Бағдарламалар',
    'programs.ftc.title': 'Металл, қозғалтқыштар, хабтар',
    'programs.ftc.text': 'goBILDA, REV Robotics, Studica, AndyMark, Axon және TETRIX: швеллерлер, Yellow Jacket, Control Hub, сервожетектер, дөңгелектер мен слайдерлер.',
    'programs.ftc.link': 'FTC хабарландырулары →',
    'programs.fll.title': 'LEGO, жинақтар, алаңдар',
    'programs.fll.text': 'SPIKE Prime және Essential, EV3, Technic арқалықтары, осьтері мен тісті дөңгелектері, маусым жинақтары мен алаң төсеніштері.',
    'programs.fll.link': 'FLL хабарландырулары →',
    'teaser.title': 'Әр бөлшекке бір атау',
    'teaser.link': 'Каталогты ашу →',
    'teaser.sub': 'Бот өндірушілердің сайттарымен салыстырылған каталогтан бөлшек ұсынады, сондықтан Yellow Jacket барлық хабарландыруда бірдей аталады. Суреттер өндірушілерден алынған.',

    'type.trade': 'Айырбас',
    'type.sell': 'Сатылады',
    'type.wanted': 'Іздеймін',
    'type.giveaway': 'Тегін',
    'condition.new': 'Жаңа',
    'condition.like_new': 'Жаңадай',
    'condition.used': 'Қолданылған, жұмыс істейді',
    'condition.for_parts': 'Бөлшекке ғана',
    'price.negotiable': 'Бағасы келісімді',
    'price.free': 'Тегін',
    'price.budget': 'Бюджеті {price}',
    'price.for': 'Орнына: {want}',
    'price.openToOffers': 'Ұсыныстарды қарастырамын',
    'want.or': '{item} немесе {price}',
    'part.fallback': 'Бөлшек',
    'verified.title': 'Тексерілген команда',
    'verified.label': 'тексерілген команда',

    'listings.title': 'Қазақстандағы FTC және FLL командаларының артық робот бөлшектері',
    'listings.sub': 'Бөлшекті тауып, командаға Telegram-да жазыңыз. Айырбастаңыз, сатып алыңыз немесе тегін алып кетіңіз.',
    'listings.searchLabel': 'Бөлшек, артикул, команда немесе қала бойынша іздеу',
    'listings.demo': 'Бұл — үлгі хабарландырулар: командалар мен Telegram сілтемелері ойдан алынған. Командалар бот арқылы жариялай бастағанда, мұнда нақты хабарландырулар шығады.',
    'filters.label': 'Сүзгілер',
    'filters.title': 'Сүзгілер',
    'filters.clearAll': 'Барлығын тазарту',
    'filters.close': 'Сүзгілерді жабу',
    'filters.type': 'Хабарландыру түрі',
    'filters.city': 'Қала',
    'filters.anyCity': 'Кез келген қала',
    'filters.brand': 'Бренд',
    'filters.anyBrand': 'Кез келген бренд',
    'filters.category': 'Санат',
    'filters.anyCategory': 'Кез келген санат',
    'filters.condition': 'Күйі',
    'filters.anyCondition': 'Кез келген күй',
    'filters.team': 'Команда',
    'filters.anyTeam': 'Кез келген команда',
    'filters.showListings': 'Хабарландыруларды көрсету',
    'filters.withCount': 'Сүзгілер ({n})',
    'filters.show': { other: '{n} хабарландыруды көрсету' },
    'filters.noMatch': 'Ештеңе табылмады',
    'results.loading': 'Хабарландырулар жүктелуде…',
    'results.someOf': { other: '{n} хабарландыру ішінен {shown}' },
    'count.listings': { other: '{n} хабарландыру' },
    'sort.label': 'Сұрыптау',
    'sort.newest': 'Алдымен жаңалары',
    'sort.price': 'Алдымен арзандары',
    'empty.title': 'Сәйкес хабарландыру жоқ',
    'empty.text': 'Сұрауды қысқартып көріңіз немесе бір сүзгіні алып тастаңыз. Бөлшек әлі ешкімде болмаса, ботқа «Іздеймін» хабарландыруын беріңіз — ол бар командалар сізді табады.',
    'empty.clear': 'Сүзгілерді тазарту',
    'activePart.before': '',
    'activePart.after': ' бар хабарландырулар',
    'activePart.showAll': 'Барлық бөлшекті көрсету',
    'photo.listing': 'Хабарландыру суреті',
    'photo.catalogAlt': '{part}, каталог суреті',
    'photo.catalogCaption': 'Каталог суреті, {source}',
    'photo.nth': '{title}, {n}-сурет',
    'photo.creditBefore': 'Бұл — өндірушінің каталогтағы суреті, команданың өз бөлшегі емес. Дереккөзі: ',
    'photo.creditAfter': '.',
    'contact.example': 'Үлгі хабарландыру',
    'contact.noUsername': 'Telegram аты жоқ',
    'contact.message': '{team} командасына жазу',
    'detail.lookingFor': 'Іздейді',
    'detail.has': 'Ұсынады',
    'detail.canTrade': 'Орнына бере алады',
    'detail.budget': 'Бюджеті',
    'detail.price': 'Бағасы',
    'detail.wants': 'Орнына қалайды',
    'detail.team': 'Команда',
    'detail.city': 'Қала',
    'detail.condition': 'Күйі',
    'detail.partNumber': 'Артикул',
    'detail.posted': 'Жарияланды',
    'detail.otherListings': 'Осы бөлшек бар басқа хабарландырулар',
    'error.listings': 'Хабарландырулар жүктелмеді. Интернетті тексеріп, бетті қайта жүктеңіз.',

    'catalog.title': 'Бөлшектер каталогы',
    'catalog.sub': 'Команда хабарландыру бергенде бот осы атауларды ұсынады, сондықтан бір қозғалтқыш барлық хабарландыруда бірдей аталады. Каталогта жоқ бөлшекті еркін мәтінмен жариялауға болады.',
    'catalog.searchLabel': 'Каталогтан іздеу',
    'catalog.placeholder': 'Атауы, артикулы немесе лақап аты',
    'catalog.ftc': 'FTC бөлшектері',
    'catalog.fll': 'FLL бөлшектері (LEGO)',
    'catalog.brands': 'Брендтер',
    'brand.other': 'Басқалары',
    'catalog.loading': 'Каталог жүктелуде…',
    'catalog.emptyTitle': 'Сәйкес бөлшек жоқ',
    'catalog.emptyText': 'Өндіруші сайтындағы артикулмен немесе қысқарақ атаумен іздеп көріңіз. Каталогта жоқ бөлшекті ботта еркін мәтінмен жариялауға болады.',
    'catalog.total': '{parts}, {brands}',
    'catalog.someOf': { other: '{n} бөлшек ішінен {shown}' },
    'catalog.noListings': 'Хабарландыру жоқ',
    'catalog.productPage': 'Өндіруші сайтындағы тауар беті',
    'count.parts': { other: '{n} бөлшек' },
    'count.brands': { other: '{n} бренд' },
    'error.catalog': 'Каталог жүктелмеді. Интернетті тексеріп, бетті қайта жүктеңіз.',

    // Dates, for browsers without this language's Intl data
    'age.today': 'бүгін',
    'age.yesterday': 'кеше',
    'age.daysAgo': { other: '{n} күн бұрын' },
    'age.date': '{y} ж. {d} {month}',
    'month.0': 'қаңтар',
    'month.1': 'ақпан',
    'month.2': 'наурыз',
    'month.3': 'сәуір',
    'month.4': 'мамыр',
    'month.5': 'маусым',
    'month.6': 'шілде',
    'month.7': 'тамыз',
    'month.8': 'қыркүйек',
    'month.9': 'қазан',
    'month.10': 'қараша',
    'month.11': 'желтоқсан',

    'category.sets': 'Толық жинақтар',
    'category.field': 'Алаң және миссиялар',
    'category.motors': 'Қозғалтқыштар',
    'category.servos': 'Сервожетектер',
    'category.control': 'Басқару және қуат',
    'category.sensors': 'Датчиктер',
    'category.batteries': 'Аккумуляторлар мен зарядтағыштар',
    'category.structure': 'Конструкция',
    'category.motion': 'Берілістер',
    'category.wheels': 'Дөңгелектер',
    'category.linear': 'Сызықтық қозғалыс',
    'category.hardware': 'Бекіткіштер',
    'category.cables': 'Кабельдер мен қосқыштар',
    'category.other': 'Басқалары',
  },
};

/** @param {unknown} code @returns {'kk'|'ru'|'en'|null} */
function normalize(code) {
  if (typeof code !== 'string') return null;
  const c = code.trim().toLowerCase();
  if (c.startsWith('kk') || c === 'kz') return 'kk';
  if (c.startsWith('ru')) return 'ru';
  if (c.startsWith('en')) return 'en';
  return null;
}

/**
 * Picks the language from what the browser offers. Pure, so it runs in tests.
 * An explicit choice (the URL, then the saved one) must be one of LANGS; from the
 * browser's list only Kazakh or Russian count, and the first of those wins.
 * @param {{ param?: string|null, stored?: string|null, languages?: readonly string[] }} sources
 * @returns {'kk'|'ru'|'en'}
 */
export function resolveLang({ param = null, stored = null, languages = [] } = {}) {
  const explicit = normalize(param) ?? normalize(stored);
  if (explicit) return explicit;
  for (const l of languages) {
    const n = normalize(l);
    if (n === 'kk' || n === 'ru') return n;
  }
  return 'en';
}

function readStored() {
  try {
    return globalThis.localStorage?.getItem(STORAGE_KEY) ?? null;
  } catch {
    return null; // storage blocked (private mode, sandboxed frame)
  }
}

function store(code) {
  try {
    globalThis.localStorage?.setItem(STORAGE_KEY, code);
  } catch {
    // Not allowed here: the choice holds for this page only.
  }
}

function detect() {
  // Outside a browser (Node tests) there is nothing to read: English.
  if (typeof window === 'undefined' || typeof location === 'undefined') return 'en';
  const param = new URLSearchParams(location.search).get('lang');
  const fromParam = normalize(param);
  // A ?lang= link also sets the saved choice, so the next page keeps the language.
  if (fromParam) store(fromParam);
  return resolveLang({ param, stored: readStored(), languages: navigator.languages ?? [navigator.language] });
}

/** The language of this page load. */
export const lang = detect();
/** Locale for dates in this language. */
export const locale = LOCALES[lang];

/**
 * The form of `forms` that Intl.PluralRules picks for n in `code`, with {n} filled in.
 * @param {string} code @param {number} n @param {PluralForms} forms
 */
export function pluralFor(code, n, forms) {
  const category = new Intl.PluralRules(code).select(n);
  const form = forms[category] ?? forms.other ?? forms.many ?? '';
  return form.replaceAll('{n}', String(n));
}

/** @param {number} n @param {PluralForms} forms */
export function plural(n, forms) {
  return pluralFor(lang, n, forms);
}

/**
 * Looks up `key` in `code`, falling back to English, then to the key itself.
 * {name} placeholders are filled from vars; a plural entry needs vars.n.
 * @param {string} code @param {string} key @param {Record<string, string|number>} [vars]
 */
export function translate(code, key, vars = {}) {
  let entry = DICT[code]?.[key] ?? DICT.en[key];
  if (entry === undefined) return key;
  if (typeof entry === 'object') {
    // Without a count (static HTML before numbers load), use the "many" form.
    entry = typeof vars.n === 'number' ? pluralFor(code, vars.n, entry) : entry.many ?? entry.other;
  }
  return entry.replace(/\{(\w+)\}/g, (m, name) => (name in vars ? String(vars[name]) : m));
}

/** @param {string} key @param {Record<string, string|number>} [vars] */
export function t(key, vars) {
  return translate(lang, key, vars);
}

/** Saves the choice and reloads the page in that language, without ?lang= in the URL. */
export function setLang(code) {
  const next = normalize(code);
  if (!next) return;
  store(next);
  const url = new URL(location.href);
  url.searchParams.delete('lang');
  if (url.href === location.href) location.reload();
  else location.replace(url.href);
}

/**
 * Fills the page's static strings: data-i18n (text), data-i18n-placeholder,
 * data-i18n-aria-label and data-i18n-title; sets <html lang>, the title and the
 * description from the page's keys (body data-page="landing|listings|catalog").
 * @param {ParentNode} [root]
 */
export function applyStatic(root = document) {
  document.documentElement.lang = lang;
  const page = document.body?.dataset.page;
  if (page) {
    document.title = t(`meta.${page}.title`);
    document.querySelector('meta[name="description"]')?.setAttribute('content', t(`meta.${page}.description`));
    document.querySelector('meta[property="og:description"]')?.setAttribute('content', t('meta.og.description'));
  }
  for (const el of root.querySelectorAll('[data-i18n]')) el.textContent = t(/** @type {HTMLElement} */ (el).dataset.i18n);
  const attrs = [['i18nPlaceholder', 'placeholder'], ['i18nAriaLabel', 'aria-label'], ['i18nTitle', 'title']];
  for (const [prop, attr] of attrs) {
    const selector = `[data-${prop.replace(/[A-Z]/g, (c) => `-${c.toLowerCase()}`)}]`;
    for (const el of root.querySelectorAll(selector)) el.setAttribute(attr, t(/** @type {HTMLElement} */ (el).dataset[prop]));
  }
}

/** Wires the KZ / RU / EN buttons in the top bar. */
export function bindLangSwitch(root = document) {
  for (const btn of root.querySelectorAll('.lang-btn')) {
    const code = /** @type {HTMLElement} */ (btn).dataset.lang;
    btn.setAttribute('aria-pressed', String(code === lang));
    btn.addEventListener('click', () => { if (code !== lang) setLang(code); });
  }
}
