"""Bot texts in Kazakh, Russian and English.

`t(key, lang, **kwargs)` returns the text for a key, filled in with str.format.
Strings go out in HTML parse mode: never put a bare < or & in them, and
escape user text before passing it in (the callers do, as before).

Left untranslated on purpose: the brand (Almasu, "Buy. Sell. Exchange."),
part names, brands and SKUs, team and city names users typed. Catalog
category names stay English in the database and are translated only for
display, through CATEGORY_NAMES.

This module must not import app.config or anything that needs env vars:
tests/test_i18n.py imports it on its own.
"""

LANGS = ("kk", "ru", "en")
DEFAULT_LANG = "en"

LANG_NAMES = {"kk": "🇰🇿 Қазақша", "ru": "🇷🇺 Русский", "en": "🇬🇧 English"}

# Shown before we know which language the user reads, so it is in all three.
LANG_PICKER_TEXT = "🌐 Тілді таңдаңыз · Выберите язык · Choose your language"

BRAND = "Almasu"
SLOGAN = "Buy. Sell. Exchange."

# Written per key so the three versions sit side by side; STRINGS below is the
# same data keyed by language.
_TEXTS: dict[str, dict[str, str]] = {
    # --- language ------------------------------------------------------------
    "lang_set": {
        "en": "✅ Language: {name}",
        "ru": "✅ Язык: {name}",
        "kk": "✅ Тіл: {name}",
    },

    # --- reply menu ------------------------------------------------------------
    "btn_new_listing": {
        "en": "➕ New listing",
        "ru": "➕ Новое объявление",
        "kk": "➕ Жаңа хабарландыру",
    },
    "btn_my_listings": {
        "en": "📋 My listings",
        "ru": "📋 Мои объявления",
        "kk": "📋 Менің хабарландыруларым",
    },
    "btn_website": {
        "en": "🌐 Website",
        "ru": "🌐 Сайт",
        "kk": "🌐 Сайт",
    },
    "btn_language": {
        "en": "🌐 Language",
        "ru": "🌐 Язык",
        "kk": "🌐 Тіл",
    },
    "menu_hint": {
        "en": "Use the menu below.",
        "ru": "Пользуйтесь меню ниже.",
        "kk": "Төмендегі мәзірді пайдаланыңыз.",
    },

    # --- Telegram command menu and bot profile --------------------------------
    "cmd_start": {
        "en": "Register or open the menu",
        "ru": "Регистрация или меню",
        "kk": "Тіркелу немесе мәзір",
    },
    "cmd_help": {
        "en": "How the exchange works",
        "ru": "Как устроен обмен",
        "kk": "Алмасу қалай жұмыс істейді",
    },
    "cmd_cancel": {
        "en": "Cancel the current step",
        "ru": "Отменить текущий шаг",
        "kk": "Ағымдағы қадамды тоқтату",
    },
    "cmd_lang": {
        "en": "Change the language",
        "ru": "Сменить язык",
        "kk": "Тілді ауыстыру",
    },
    "cmd_site": {
        "en": "Open the website",
        "ru": "Открыть сайт",
        "kk": "Сайтты ашу",
    },
    # Telegram limits: short description 120 characters, description 512.
    # The brand line (Almasu, the slogan) is added in code and not translated.
    "bot_short_description": {
        "en": "Spare FTC and FLL parts between teams in Kazakhstan.",
        "ru": "Запчасти FTC и FLL: обмен между командами Казахстана.",
        "kk": "FTC және FLL бөлшектері: Қазақстан командалары арасында алмасу.",
    },
    "bot_description": {
        "en": "Buy, sell and exchange spare FTC and FLL parts between teams in Kazakhstan.\n\n"
              "Post what your team has or needs here. Every listing also appears on the website, "
              "and deals happen in Telegram private messages.",
        "ru": "Покупайте, продавайте и обменивайте запасные детали FTC и FLL между командами Казахстана.\n\n"
              "Размещайте здесь то, что есть у вашей команды или что ей нужно. Каждое объявление "
              "появляется и на сайте, а договариваются в личных сообщениях Telegram.",
        "kk": "Қазақстан командалары арасында FTC және FLL қосалқы бөлшектерін сатып алыңыз, "
              "сатыңыз және айырбастаңыз.\n\n"
              "Командаңызда бар немесе қажет бөлшекті осында жариялаңыз. Әр хабарландыру сайтта да "
              "шығады, ал келісім Telegram-дағы жеке хабарламаларда жасалады.",
    },

    # --- common ---------------------------------------------------------------
    "help": {
        "en": "<b>Almasu</b>\n\n"
              "➕ New listing — post a part you have, need, sell or give away.\n"
              "📋 My listings — edit or close your listings.\n"
              "{site_line}"
              "\nDeals happen in Telegram: teams see your @username on the website and write to you.\n"
              "/lang — change the language.\n"
              "/cancel — stop what you are doing.",
        "ru": "<b>Almasu</b>\n\n"
              "➕ Новое объявление — разместите деталь, которая у вас есть, нужна, продаётся или "
              "отдаётся даром.\n"
              "📋 Мои объявления — изменить или закрыть ваши объявления.\n"
              "{site_line}"
              "\nСделки проходят в Telegram: команды видят ваш @username на сайте и пишут вам.\n"
              "/lang — сменить язык.\n"
              "/cancel — прервать текущее действие.",
        "kk": "<b>Almasu</b>\n\n"
              "➕ Жаңа хабарландыру — өзіңізде бар, керек, сатылатын немесе тегін берілетін "
              "бөлшекті жариялаңыз.\n"
              "📋 Менің хабарландыруларым — хабарландыруларыңызды өзгерту немесе жабу.\n"
              "{site_line}"
              "\nКелісім Telegram-да жасалады: командалар сайттан сіздің @username атыңызды көріп, "
              "сізге жазады.\n"
              "/lang — тілді ауыстыру.\n"
              "/cancel — ағымдағы әрекетті тоқтату.",
    },
    "help_site_line": {
        "en": "🌐 Website — search every team's listings: {url}\n",
        "ru": "🌐 Сайт — поиск по объявлениям всех команд: {url}\n",
        "kk": "🌐 Сайт — барлық командалардың хабарландыруларынан іздеу: {url}\n",
    },
    "site_offline": {
        "en": "The website isn't online yet.",
        "ru": "Сайт пока не работает.",
        "kk": "Сайт әлі іске қосылмаған.",
    },
    "site_intro": {
        "en": "Search every team's listings by part, city or team:",
        "ru": "Ищите объявления всех команд по детали, городу или команде:",
        "kk": "Барлық командалардың хабарландыруларын бөлшек, қала немесе команда бойынша іздеңіз:",
    },
    "btn_open_website": {
        "en": "🌐 Open the website",
        "ru": "🌐 Открыть сайт",
        "kk": "🌐 Сайтты ашу",
    },
    "cancelled": {
        "en": "Cancelled.",
        "ru": "Отменено.",
        "kk": "Тоқтатылды.",
    },
    "what_next": {
        "en": "What next?",
        "ru": "Что дальше?",
        "kk": "Енді не істейміз?",
    },
    "send_start": {
        "en": "Send /start to register your team.",
        "ru": "Отправьте /start, чтобы зарегистрировать команду.",
        "kk": "Командаңызды тіркеу үшін /start жіберіңіз.",
    },
    "use_menu": {
        "en": "Use the menu below or /help.",
        "ru": "Пользуйтесь меню ниже или /help.",
        "kk": "Төмендегі мәзірді немесе /help пайдаланыңыз.",
    },
    "stale_step": {
        "en": "That step is over, start again from the menu.",
        "ru": "Этот шаг уже завершён, начните заново из меню.",
        "kk": "Бұл қадам аяқталған, мәзірден қайта бастаңыз.",
    },
    "error_generic": {
        "en": "Something broke on our side. Try again or send /cancel.",
        "ru": "У нас что-то сломалось. Попробуйте ещё раз или отправьте /cancel.",
        "kk": "Біз жақта ақау шықты. Қайта көріңіз немесе /cancel жіберіңіз.",
    },

    # --- registration ---------------------------------------------------------
    # {site} is " (https://…)" or empty.
    "welcome": {
        "en": "<b>Almasu</b>\n"
              "Buy. Sell. Exchange.\n\n"
              "Post parts you have or need. Listings show up on the website{site}, "
              "where other teams can find them and write to you in Telegram.\n\n"
              "First, register your team.",
        "ru": "<b>Almasu</b>\n"
              "Buy. Sell. Exchange.\n\n"
              "Размещайте детали, которые у вас есть или которые нужны. Объявления появляются "
              "на сайте{site}, где их находят другие команды и пишут вам в Telegram.\n\n"
              "Для начала зарегистрируйте команду.",
        "kk": "<b>Almasu</b>\n"
              "Buy. Sell. Exchange.\n\n"
              "Өзіңізде бар немесе өзіңізге керек бөлшектерді жариялаңыз. Хабарландырулар "
              "сайтта{site} шығады, басқа командалар оларды сол жерден тауып, сізге Telegram-да жазады.\n\n"
              "Алдымен командаңызды тіркеңіз.",
    },
    "already_registered": {
        "en": "You are registered with {team}.",
        "ru": "Вы зарегистрированы в команде {team}.",
        "kk": "Сіз {team} командасында тіркелгенсіз.",
    },
    "pending_request": {
        "en": "Your request to add {team} is with the moderators. "
              "You'll get a message here when they decide.",
        "ru": "Ваша заявка на добавление {team} у модераторов. "
              "Когда они решат, вам придёт сообщение здесь.",
        "kk": "{team} командасын қосу туралы өтінішіңіз модераторларда. "
              "Олар шешім қабылдағанда, осы жерге хабарлама келеді.",
    },
    "no_username": {
        "en": "Your Telegram account has no @username. Other teams need it to contact you.\n"
              "Set one in Telegram → Settings → Username, then send /start again.",
        "ru": "У вашего аккаунта Telegram нет @username, а другим командам он нужен, чтобы связаться с вами.\n"
              "Задайте его в Telegram → Настройки → Имя пользователя и снова отправьте /start.",
        "kk": "Telegram аккаунтыңызда @username жоқ, ал басқа командалар сізбен сол арқылы байланысады.\n"
              "Оны Telegram → Баптаулар → Пайдаланушы аты бөлімінде қойып, /start командасын қайта жіберіңіз.",
    },
    "ask_team_number": {
        "en": "Send your team number (digits only).",
        "ru": "Отправьте номер команды (только цифры).",
        "kk": "Команда нөмірін жіберіңіз (тек цифрлар).",
    },
    "bad_team_number": {
        "en": "Team number must be digits only, for example 12345.",
        "ru": "Номер команды — только цифры, например 12345.",
        "kk": "Команда нөмірі тек цифрлардан тұрады, мысалы 12345.",
    },
    "found_team": {
        "en": "Found {team}. Is this your team?",
        "ru": "Нашлась команда {team}. Это ваша команда?",
        "kk": "{team} командасы табылды. Бұл сіздің командаңыз ба?",
    },
    "team_waiting": {
        "en": "{team} is already waiting for a moderator. When it's approved, send /start and join it.",
        "ru": "{team} уже ждёт решения модератора. Когда команду одобрят, отправьте /start и вступите в неё.",
        "kk": "{team} модератордың шешімін күтіп тұр. Команда мақұлданғанда, /start жіберіп, оған қосылыңыз.",
    },
    "not_on_ustem": {
        "en": "{team} isn't on the USTEM Connect team list ({url}). "
              "Check the number there. If it's right, send your team name and a moderator will add the team.",
        "ru": "{team} нет в списке команд USTEM Connect ({url}). "
              "Проверьте номер там. Если он верный, отправьте название команды, и модератор добавит её.",
        "kk": "{team} USTEM Connect командалар тізімінде жоқ ({url}). "
              "Нөмірді сол жерден тексеріңіз. Нөмір дұрыс болса, команда атауын жіберіңіз, модератор команданы қосады.",
    },
    "btn_join_yes": {
        "en": "Yes, that's my team",
        "ru": "Да, это моя команда",
        "kk": "Иә, бұл менің командам",
    },
    "btn_join_no": {
        "en": "No, start over",
        "ru": "Нет, начать заново",
        "kk": "Жоқ, қайта бастау",
    },
    "joined_team": {
        "en": "You joined the team.",
        "ru": "Вы вступили в команду.",
        "kk": "Сіз командаға қосылдыңыз.",
    },
    "ready_first_listing": {
        "en": "Ready. Post your first listing.",
        "ru": "Готово. Разместите первое объявление.",
        "kk": "Дайын. Алғашқы хабарландыруыңызды жариялаңыз.",
    },
    "which_program": {
        "en": "Which program is your team in?",
        "ru": "В какой программе ваша команда?",
        "kk": "Командаңыз қай бағдарламада?",
    },
    "bad_team_name": {
        "en": "Team name must be 2–60 characters.",
        "ru": "Название команды — от 2 до 60 символов.",
        "kk": "Команда атауы 2–60 таңбадан тұруы керек.",
    },
    "ask_city": {
        "en": "Send your city, for example Almaty.",
        "ru": "Отправьте ваш город, например Алматы.",
        "kk": "Қалаңызды жіберіңіз, мысалы Алматы.",
    },
    "bad_city": {
        "en": "City must be 2–40 characters.",
        "ru": "Название города — от 2 до 40 символов.",
        "kk": "Қала атауы 2–40 таңбадан тұруы керек.",
    },
    "registered": {
        "en": "Registered: {team}.",
        "ru": "Вы зарегистрированы: {team}.",
        "kk": "Тіркелдіңіз: {team}.",
    },
    "request_exists": {
        "en": "There's already an open request for you or for this team. "
              "You'll get a message here when a moderator decides.",
        "ru": "У вас или у этой команды уже есть открытая заявка. "
              "Когда модератор решит, вам придёт сообщение здесь.",
        "kk": "Сізде немесе бұл командада ашық өтініш бар. "
              "Модератор шешім қабылдағанда, осы жерге хабарлама келеді.",
    },
    "request_sent": {
        "en": "Sent to the moderators: {team} ({city}). You'll get a message here when they decide.",
        "ru": "Отправлено модераторам: {team} ({city}). Когда они решат, вам придёт сообщение здесь.",
        "kk": "Модераторларға жіберілді: {team} ({city}). Олар шешім қабылдағанда, осы жерге хабарлама келеді.",
    },
    "request_saved_no_mods": {
        "en": "Your request is saved, but no moderator could be reached yet. "
              "Ask in the FIRST Kazakhstan channel to have it reviewed.",
        "ru": "Заявка сохранена, но пока ни до одного модератора не удалось достучаться. "
              "Попросите рассмотреть её в канале FIRST Kazakhstan.",
        "kk": "Өтінішіңіз сақталды, бірақ әзірге бірде-бір модераторға жеткізілмеді. "
              "Оны қарауды FIRST Kazakhstan арнасында сұраңыз.",
    },

    # --- moderation (in the moderator's own language) -------------------------
    "mod_request": {
        "en": "<b>Team request #{id}</b>\n{team} ({city})\nFrom: {who} (id {tg_id})\n\n"
              "Not on the USTEM Connect list. Check it: {url}",
        "ru": "<b>Заявка команды #{id}</b>\n{team} ({city})\nОт: {who} (id {tg_id})\n\n"
              "Нет в списке USTEM Connect. Проверьте: {url}",
        "kk": "<b>Команда өтініші #{id}</b>\n{team} ({city})\nКімнен: {who} (id {tg_id})\n\n"
              "USTEM Connect тізімінде жоқ. Тексеріңіз: {url}",
    },
    "btn_approve": {
        "en": "✅ Approve",
        "ru": "✅ Одобрить",
        "kk": "✅ Мақұлдау",
    },
    "btn_reject": {
        "en": "✖️ Reject",
        "ru": "✖️ Отклонить",
        "kk": "✖️ Қабылдамау",
    },
    "mods_only": {
        "en": "Only moderators can do this.",
        "ru": "Это могут делать только модераторы.",
        "kk": "Мұны тек модераторлар жасай алады.",
    },
    "unknown_action": {
        "en": "Unknown action.",
        "ru": "Неизвестное действие.",
        "kk": "Белгісіз әрекет.",
    },
    "already_approved": {
        "en": "Already approved.",
        "ru": "Уже одобрено.",
        "kk": "Әлдеқашан мақұлданған.",
    },
    "already_rejected": {
        "en": "Already rejected.",
        "ru": "Уже отклонено.",
        "kk": "Әлдеқашан қабылданбаған.",
    },
    "already_status": {
        "en": "Already {status}.",
        "ru": "Уже решено: {status}.",
        "kk": "Шешім қабылданған: {status}.",
    },
    "request_not_found": {
        "en": "Request not found.",
        "ru": "Заявка не найдена.",
        "kk": "Өтініш табылмады.",
    },
    "team_approved_user": {
        "en": "✅ Your team {team} was approved. You can post listings now.",
        "ru": "✅ Ваша команда {team} одобрена. Теперь можно размещать объявления.",
        "kk": "✅ {team} командаңыз мақұлданды. Енді хабарландыру жариялай аласыз.",
    },
    "team_rejected_user": {
        "en": "A moderator didn't approve {team}. Check your team number on {url} "
              "and send /start to try again.",
        "ru": "Модератор не одобрил {team}. Проверьте номер команды на {url} "
              "и отправьте /start, чтобы попробовать снова.",
        "kk": "Модератор {team} командасын мақұлдамады. Команда нөмірін {url} сайтынан тексеріп, "
              "қайта көру үшін /start жіберіңіз.",
    },
    "verdict_approved": {
        "en": "✅ Approved by {moderator}",
        "ru": "✅ Одобрил(а) {moderator}",
        "kk": "✅ Мақұлдаған: {moderator}",
    },
    "verdict_rejected": {
        "en": "✖️ Rejected by {moderator}",
        "ru": "✖️ Отклонил(а) {moderator}",
        "kk": "✖️ Қабылдамаған: {moderator}",
    },
    "new_member": {
        "en": "<b>New member, team not verified</b>\n{who} joined {team} ({city}).\n\n"
              "If you know they're on this team, verify it.",
        "ru": "<b>Новый участник, команда не подтверждена</b>\n{who} вступил(а) в {team} ({city}).\n\n"
              "Если вы знаете, что этот человек в команде, подтвердите её.",
        "kk": "<b>Жаңа мүше, команда расталмаған</b>\n{who} {team} ({city}) командасына қосылды.\n\n"
              "Бұл адамның осы командада екенін білсеңіз, команданы растаңыз.",
    },
    "btn_verify_team": {
        "en": "✓ Verify team",
        "ru": "✓ Подтвердить команду",
        "kk": "✓ Команданы растау",
    },
    "admins_only": {
        "en": "Only admins can do this.",
        "ru": "Это могут делать только админы.",
        "kk": "Мұны тек әкімшілер жасай алады.",
    },
    "team_not_found": {
        "en": "Team not found.",
        "ru": "Команда не найдена.",
        "kk": "Команда табылмады.",
    },
    "verified_line": {
        "en": "✓ Verified: {team}",
        "ru": "✓ Подтверждена: {team}",
        "kk": "✓ Расталды: {team}",
    },
    "verified_alert": {
        "en": "Verified",
        "ru": "Подтверждено",
        "kk": "Расталды",
    },
    "verify_usage": {
        "en": "Usage: /{command} FTC 24881",
        "ru": "Формат: /{command} FTC 24881",
        "kk": "Қолданылуы: /{command} FTC 24881",
    },
    "no_such_team": {
        "en": "No such team in the database.",
        "ru": "Такой команды нет в базе.",
        "kk": "Мұндай команда базада жоқ.",
    },
    "verification_removed": {
        "en": "Verification removed: {team}",
        "ru": "Подтверждение снято: {team}",
        "kk": "Растау алынып тасталды: {team}",
    },

    # --- listing labels and rendering (texts.py) ------------------------------
    "type_trade": {"en": "🔄 Trade", "ru": "🔄 Обмен", "kk": "🔄 Айырбастау"},
    "type_sell": {"en": "💰 For sale", "ru": "💰 Продажа", "kk": "💰 Сату"},
    "type_wanted": {"en": "🔎 Wanted", "ru": "🔎 Ищу", "kk": "🔎 Іздеймін"},
    "type_give": {"en": "🎁 Give away", "ru": "🎁 Отдам даром", "kk": "🎁 Тегін беремін"},
    "cond_new": {"en": "New", "ru": "Новое", "kk": "Жаңа"},
    "cond_used": {"en": "Used — working", "ru": "Б/у — рабочее", "kk": "Қолданылған — жұмыс істейді"},
    "cond_broken": {"en": "Broken — for parts", "ru": "Сломано — на запчасти", "kk": "Бұзылған — бөлшекке"},
    "price_negotiable": {"en": "Negotiable", "ru": "Договорная", "kk": "Келісім бойынша"},
    "lst_looking_for": {"en": "Looking for: <b>{value}</b>", "ru": "Ищу: <b>{value}</b>",
                        "kk": "Іздеймін: <b>{value}</b>"},
    "lst_have": {"en": "Have: <b>{value}</b>", "ru": "Есть: <b>{value}</b>", "kk": "Бар: <b>{value}</b>"},
    "lst_price": {"en": "Price: {value}", "ru": "Цена: {value}", "kk": "Бағасы: {value}"},
    "lst_want": {"en": "Want: {value}", "ru": "Взамен: {value}", "kk": "Орнына: {value}"},
    "lst_any_offer": {"en": "any offer", "ru": "любые предложения", "kk": "кез келген ұсыныс"},
    "lst_condition": {"en": "Condition: {value}", "ru": "Состояние: {value}", "kk": "Күйі: {value}"},
    "lst_note": {"en": "Note: {value}", "ru": "Примечание: {value}", "kk": "Ескертпе: {value}"},
    "lst_team": {"en": "Team: {value}", "ru": "Команда: {value}", "kk": "Команда: {value}"},
    "lst_city": {"en": "City: {value}", "ru": "Город: {value}", "kk": "Қала: {value}"},
    "lst_contact": {"en": "Contact: @{value}", "ru": "Контакт: @{value}", "kk": "Байланыс: @{value}"},
    "lst_photos": {"en": "Photos: {count}", "ru": "Фото: {count}", "kk": "Фото: {count}"},

    # --- listing keyboards ----------------------------------------------------
    "btn_negotiable": {"en": "Negotiable", "ru": "Договорная", "kk": "Келісім бойынша"},
    "btn_done": {"en": "Done", "ru": "Готово", "kk": "Дайын"},
    "btn_skip_photos": {"en": "Skip photos", "ru": "Без фото", "kk": "Фотосыз"},
    "btn_catalog_photo": {"en": "🖼 Use the catalog photo", "ru": "🖼 Взять фото из каталога",
                          "kk": "🖼 Каталогтағы фотоны алу"},
    "btn_skip": {"en": "Skip", "ru": "Пропустить", "kk": "Өткізіп жіберу"},
    "btn_publish": {"en": "✅ Publish", "ru": "✅ Опубликовать", "kk": "✅ Жариялау"},
    "btn_cancel": {"en": "✖️ Cancel", "ru": "✖️ Отмена", "kk": "✖️ Бас тарту"},
    "btn_edit": {"en": "✏️ Edit", "ru": "✏️ Изменить", "kk": "✏️ Өзгерту"},
    "btn_close": {"en": "✅ Close", "ru": "✅ Закрыть", "kk": "✅ Жабу"},
    "btn_on_website": {"en": "🌐 On the website", "ru": "🌐 На сайте", "kk": "🌐 Сайтта"},
    "btn_view_on_website": {"en": "🌐 View on the website", "ru": "🌐 Смотреть на сайте",
                            "kk": "🌐 Сайтта көру"},
    "btn_field_wanted_part": {"en": "Wanted part", "ru": "Нужная деталь", "kk": "Керек бөлшек"},
    "btn_field_part": {"en": "Part", "ru": "Деталь", "kk": "Бөлшек"},
    "btn_field_price": {"en": "Price", "ru": "Цена", "kk": "Баға"},
    "btn_field_condition": {"en": "Condition", "ru": "Состояние", "kk": "Күйі"},
    "btn_field_note": {"en": "Note", "ru": "Примечание", "kk": "Ескертпе"},
    "btn_field_photos": {"en": "Photos", "ru": "Фото", "kk": "Фотолар"},
    "btn_back": {"en": "⬅️ Back", "ru": "⬅️ Назад", "kk": "⬅️ Артқа"},

    # --- new listing ----------------------------------------------------------
    "register_first": {
        "en": "Register your team first — send /start.",
        "ru": "Сначала зарегистрируйте команду — отправьте /start.",
        "kk": "Алдымен командаңызды тіркеңіз — /start жіберіңіз.",
    },
    "ask_listing_type": {
        "en": "What kind of listing is this?",
        "ru": "Какое это объявление?",
        "kk": "Хабарландыру түрі қандай?",
    },
    "ask_part_wanted": {
        "en": "What part do you need?",
        "ru": "Какая деталь вам нужна?",
        "kk": "Сізге қандай бөлшек керек?",
    },
    "ask_part_have": {
        "en": "What part do you have?",
        "ru": "Какая деталь у вас есть?",
        "kk": "Сізде қандай бөлшек бар?",
    },
    "ask_part_return": {
        "en": "What do you want in return?",
        "ru": "Что хотите взамен?",
        "kk": "Орнына не алғыңыз келеді?",
    },
    "ask_price": {
        "en": "Price in tenge (digits only), or tap Negotiable.",
        "ru": "Цена в тенге (только цифры) или нажмите «Договорная».",
        "kk": "Бағасын теңгемен жазыңыз (тек цифрлар) немесе «Келісім бойынша» батырмасын басыңыз.",
    },
    "ask_condition": {
        "en": "What condition is the part in?",
        "ru": "В каком состоянии деталь?",
        "kk": "Бөлшектің күйі қандай?",
    },
    "ask_photos": {
        "en": "Send up to {max} photos of the part, then tap Done.",
        "ru": "Отправьте до {max} фото детали, затем нажмите «Готово».",
        "kk": "Бөлшектің {max} фотосына дейін жіберіп, «Дайын» батырмасын басыңыз.",
    },
    "ask_photos_catalog": {
        "en": "No photo at hand? Use the official catalog photo instead.",
        "ru": "Нет фото под рукой? Возьмите официальное фото из каталога.",
        "kk": "Фото жоқ па? Оның орнына каталогтағы ресми фотоны алыңыз.",
    },
    "bad_price": {
        "en": "Send the price as digits, for example 15000.",
        "ru": "Отправьте цену цифрами, например 15000.",
        "kk": "Бағаны цифрмен жіберіңіз, мысалы 15000.",
    },
    "price_set_negotiable": {
        "en": "Price: negotiable",
        "ru": "Цена: договорная",
        "kk": "Бағасы: келісім бойынша",
    },
    "photo_limit": {
        "en": "{max} photos is the limit. Tap Done.",
        "ru": "Больше {max} фото нельзя. Нажмите «Готово».",
        "kk": "Ең көбі {max} фото. «Дайын» батырмасын басыңыз.",
    },
    "photo_added": {
        "en": "Photo {count}/{max} added.",
        "ru": "Фото {count}/{max} добавлено.",
        "kk": "Фото {count}/{max} қосылды.",
    },
    "not_available": {
        "en": "Not available for this listing.",
        "ru": "Для этого объявления недоступно.",
        "kk": "Бұл хабарландыру үшін қолжетімсіз.",
    },
    "catalog_photo_added": {
        "en": "Catalog photo added.",
        "ru": "Фото из каталога добавлено.",
        "kk": "Каталогтағы фото қосылды.",
    },
    "ask_note": {
        "en": "Add a note if anything matters — quantity, what is broken, pickup details. Or skip it.",
        "ru": "Добавьте примечание, если что-то важно: количество, что сломано, где забрать. Или пропустите.",
        "kk": "Маңызды жайт болса, ескертпе қосыңыз: саны, неңі бұзылған, қайдан алуға болады. "
              "Немесе өткізіп жіберіңіз.",
    },
    "note_too_long": {
        "en": "Keep the note under {max} characters.",
        "ru": "Примечание должно быть короче {max} символов.",
        "kk": "Ескертпе {max} таңбадан аспауы керек.",
    },
    "check_listing": {
        "en": "Check the listing:",
        "ru": "Проверьте объявление:",
        "kk": "Хабарландыруды тексеріңіз:",
    },
    "uploading_photos": {
        "en": "Uploading photos…",
        "ru": "Загружаю фото…",
        "kk": "Фотолар жүктеліп жатыр…",
    },
    "photos_failed_publish": {
        "en": "Photos could not be uploaded, publishing without them.",
        "ru": "Не удалось загрузить фото, публикую без них.",
        "kk": "Фотолар жүктелмеді, хабарландыру оларсыз жарияланады.",
    },
    "published": {
        "en": "Published.",
        "ru": "Опубликовано.",
        "kk": "Жарияланды.",
    },
    "live_on_website": {
        "en": "It's live on the website now:",
        "ru": "Объявление уже на сайте:",
        "kk": "Хабарландыру енді сайтта:",
    },

    # --- my listings ----------------------------------------------------------
    "no_listings": {
        "en": "You have no active listings.",
        "ru": "У вас нет активных объявлений.",
        "kk": "Сізде белсенді хабарландыру жоқ.",
    },
    "listing_gone": {
        "en": "That listing is gone.",
        "ru": "Этого объявления больше нет.",
        "kk": "Бұл хабарландыру енді жоқ.",
    },
    "not_yours": {
        "en": "That listing is not yours.",
        "ru": "Это не ваше объявление.",
        "kk": "Бұл сіздің хабарландыруыңыз емес.",
    },
    "listing_closed": {
        "en": "Listing #{id} closed. It is off the website now.",
        "ru": "Объявление #{id} закрыто и снято с сайта.",
        "kk": "#{id} хабарландыру жабылды, ол енді сайтта жоқ.",
    },
    "edit_part_wanted": {
        "en": "Which part do you need?",
        "ru": "Какая деталь вам нужна?",
        "kk": "Сізге қай бөлшек керек?",
    },
    "edit_part_have": {
        "en": "Which part do you have?",
        "ru": "Какая деталь у вас есть?",
        "kk": "Сізде қай бөлшек бар?",
    },
    "edit_price": {
        "en": "New price in tenge, or tap Negotiable.",
        "ru": "Новая цена в тенге или нажмите «Договорная».",
        "kk": "Жаңа бағаны теңгемен жазыңыз немесе «Келісім бойынша» батырмасын басыңыз.",
    },
    "edit_condition": {
        "en": "New condition:",
        "ru": "Новое состояние:",
        "kk": "Жаңа күйі:",
    },
    "edit_note": {
        "en": "Send the new note.",
        "ru": "Отправьте новое примечание.",
        "kk": "Жаңа ескертпені жіберіңіз.",
    },
    "edit_photos": {
        "en": "Send up to {max} new photos — they replace the current ones.",
        "ru": "Отправьте до {max} новых фото — они заменят текущие.",
        "kk": "{max} жаңа фотоға дейін жіберіңіз — олар қазіргі фотолардың орнына қойылады.",
    },
    "photos_failed_nothing": {
        "en": "Photos could not be uploaded, nothing changed.",
        "ru": "Не удалось загрузить фото, ничего не изменилось.",
        "kk": "Фотолар жүктелмеді, ештеңе өзгерген жоқ.",
    },

    # --- parts picker ---------------------------------------------------------
    "pick_hint": {
        "en": "Type a part name to search the catalog, browse the categories, "
              "or tap Other to write your own.",
        "ru": "Введите название детали для поиска по каталогу, откройте категории "
              "или нажмите «Другое», чтобы написать своё.",
        "kk": "Каталогтан іздеу үшін бөлшек атауын жазыңыз, санаттарды қараңыз "
              "немесе өзіңіз жазу үшін «Басқа» батырмасын басыңыз.",
    },
    "btn_other": {"en": "✏️ Other: write my own", "ru": "✏️ Другое: написать своё",
                  "kk": "✏️ Басқа: өзім жазамын"},
    "btn_categories": {"en": "📂 Categories", "ru": "📂 Категории", "kk": "📂 Санаттар"},
    "btn_back_categories": {"en": "⬅️ Categories", "ru": "⬅️ Категории", "kk": "⬅️ Санаттар"},
    # A button label, not HTML; {query} is what the user typed.
    "btn_use_as_typed": {"en": '✍️ Use "{query}" as typed', "ru": "✍️ Оставить «{query}» как есть",
                         "kk": "✍️ «{query}» жазылғандай қалсын"},
    "too_short": {
        "en": "Type at least 2 characters.",
        "ru": "Введите хотя бы 2 символа.",
        "kk": "Кемінде 2 таңба жазыңыз.",
    },
    "too_long": {
        "en": "Too long, keep it under {max} characters.",
        "ru": "Слишком длинно, уложитесь в {max} символов.",
        "kk": "Тым ұзын, {max} таңбадан аспасын.",
    },
    "selected": {
        "en": "Selected: <b>{part}</b>",
        "ru": "Выбрано: <b>{part}</b>",
        "kk": "Таңдалды: <b>{part}</b>",
    },
    "catalog_matches": {
        "en": "Catalog matches:",
        "ru": "Нашлось в каталоге:",
        "kk": "Каталогтан табылғаны:",
    },
    "catalog_no_match": {
        "en": "Nothing in the catalog matches that.",
        "ru": "В каталоге ничего не нашлось.",
        "kk": "Каталогтан сәйкес ештеңе табылмады.",
    },
    "pick_category": {
        "en": "Pick a category, or tap Other if your part isn't listed:",
        "ru": "Выберите категорию или нажмите «Другое», если вашей детали нет в списке:",
        "kk": "Санатты таңдаңыз, ал бөлшегіңіз тізімде болмаса, «Басқа» батырмасын басыңыз:",
    },
    "category_gone": {
        "en": "Category is gone, search by name instead.",
        "ru": "Этой категории больше нет, ищите по названию.",
        "kk": "Бұл санат енді жоқ, атауы бойынша іздеңіз.",
    },
    "part_gone": {
        "en": "That part is no longer in the catalog.",
        "ru": "Этой детали больше нет в каталоге.",
        "kk": "Бұл бөлшек каталогта енді жоқ.",
    },
    "type_part_first": {
        "en": "Type the part name first.",
        "ru": "Сначала введите название детали.",
        "kk": "Алдымен бөлшек атауын жазыңыз.",
    },
    "write_own_part": {
        "en": "Write the part as you want it to appear, up to {max} characters. "
              "For example: LEGO Technic beam 15, grey, 20 pcs.",
        "ru": "Напишите деталь так, как она должна выглядеть в объявлении, до {max} символов. "
              "Например: LEGO Technic балка 15, серая, 20 шт.",
        "kk": "Бөлшекті хабарландыруда қалай көрінсін десеңіз, солай жазыңыз, {max} таңбаға дейін. "
              "Мысалы: LEGO Technic арқалығы 15, сұр, 20 дана.",
    },
}

STRINGS: dict[str, dict[str, str]] = {
    lang: {key: versions[lang] for key, versions in _TEXTS.items() if lang in versions}
    for lang in LANGS
}

# Catalog categories are stored in English (callbacks use their index, so the
# names are only for display). Unknown categories are shown as they are.
CATEGORY_NAMES: dict[str, dict[str, str]] = {
    "Axles & Gears": {"ru": "Оси и шестерни", "kk": "Біліктер мен тісті доңғалақтар"},
    "Beams & Frames": {"ru": "Балки и рамы", "kk": "Арқалықтар мен рамалар"},
    "Cables": {"ru": "Кабели", "kk": "Кабельдер"},
    "Control & Electronics": {"ru": "Управление и электроника", "kk": "Басқару және электроника"},
    "Field & Missions": {"ru": "Поле и миссии", "kk": "Алаң және миссиялар"},
    "Hardware": {"ru": "Крепёж и инструмент", "kk": "Бекіткіштер мен құралдар"},
    "Hubs": {"ru": "Хабы", "kk": "Хабтар"},
    "Linear Motion": {"ru": "Линейное движение", "kk": "Сызықтық қозғалыс"},
    "Motion": {"ru": "Передачи и подшипники", "kk": "Берілістер мен мойынтіректер"},
    "Motors": {"ru": "Моторы", "kk": "Қозғалтқыштар"},
    "Other": {"ru": "Другое", "kk": "Басқа"},
    "Pins & Connectors": {"ru": "Штифты и соединители", "kk": "Штифтер мен қосқыштар"},
    "Power": {"ru": "Питание", "kk": "Қуат"},
    "Sensors": {"ru": "Датчики", "kk": "Датчиктер"},
    "Servos": {"ru": "Сервоприводы", "kk": "Сервожетектер"},
    "Sets": {"ru": "Наборы", "kk": "Жиынтықтар"},
    "Structure": {"ru": "Конструкция", "kk": "Құрылымдық бөлшектер"},
    "Wheels": {"ru": "Колёса", "kk": "Дөңгелектер"},
}


def normalize_lang(lang: str | None) -> str:
    return lang if lang in LANGS else DEFAULT_LANG


def detect_lang(language_code: str | None) -> str:
    """Telegram's language_code (e.g. 'ru', 'kk', 'en-US') to one of ours:
    kk → kk, ru → ru, anything else → en."""
    base = (language_code or "").strip().lower().replace("_", "-").split("-")[0]
    return base if base in ("kk", "ru") else DEFAULT_LANG


def t(key: str, lang: str | None, **kwargs) -> str:
    """The text for `key` in `lang` (English if that language lacks it),
    filled in with str.format(**kwargs)."""
    table = STRINGS.get(normalize_lang(lang), STRINGS[DEFAULT_LANG])
    text = table.get(key)
    if text is None:
        text = STRINGS[DEFAULT_LANG][key]
    return text.format(**kwargs)


def all_translations(key: str) -> frozenset[str]:
    """Every language's version of a key, for matching reply-keyboard buttons:
    F.text.in_(all_translations("btn_new_listing"))."""
    return frozenset(STRINGS[lang][key] for lang in LANGS if key in STRINGS[lang])


def category_name(name: str, lang: str | None) -> str:
    """A catalog category for display. The database keeps the English name."""
    return CATEGORY_NAMES.get(name, {}).get(normalize_lang(lang), name)


def short_description(lang: str) -> str:
    return f"{SLOGAN} {t('bot_short_description', lang)}"


def description(lang: str) -> str:
    return f"{BRAND}: {SLOGAN}\n\n{t('bot_description', lang)}"
