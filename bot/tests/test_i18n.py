"""Checks the bot's translations. No network and no env vars needed:

    cd bot && python3 -m unittest discover tests

Only app.i18n is imported; the handlers pull in app.config, which needs
BOT_TOKEN and the Supabase keys.
"""

import re
import string
import unittest

from app import i18n
from app.i18n import (CATEGORY_NAMES, LANG_NAMES, LANGS, STRINGS, all_translations, category_name,
                      description, detect_lang, short_description, t)

# The only markup our strings may contain in HTML parse mode.
ALLOWED_TAG = re.compile(r"</?b>")


def placeholders(text: str) -> set[str]:
    return {name for _, name, _, _ in string.Formatter().parse(text) if name is not None}


class KeysTest(unittest.TestCase):
    def test_three_languages(self):
        self.assertEqual(set(LANGS), {"kk", "ru", "en"})
        self.assertEqual(set(STRINGS), set(LANGS))
        self.assertEqual(set(LANG_NAMES), set(LANGS))

    def test_every_key_in_every_language(self):
        keys = set().union(*(STRINGS[lang] for lang in LANGS))
        for lang in LANGS:
            missing = keys - set(STRINGS[lang])
            self.assertFalse(missing, f"{lang} is missing {sorted(missing)}")

    def test_no_empty_strings(self):
        for lang in LANGS:
            for key, text in STRINGS[lang].items():
                self.assertTrue(text.strip(), f"{lang}.{key} is empty")

    def test_placeholders_match(self):
        for key, text in STRINGS["en"].items():
            expected = placeholders(text)
            for lang in LANGS:
                self.assertEqual(placeholders(STRINGS[lang][key]), expected,
                                 f"{lang}.{key} placeholders differ from English")

    def test_every_string_formats(self):
        for lang in LANGS:
            for key, text in STRINGS[lang].items():
                values = {name: "x" for name in placeholders(text)}
                t(key, lang, **values)  # raises on a stray { or a bad field

    def test_html_safe(self):
        """Parse mode is HTML: no stray < > or & outside the <b> tags we use."""
        for lang in LANGS:
            for key, text in STRINGS[lang].items():
                bare = ALLOWED_TAG.sub("", text)
                for char in "<>&":
                    self.assertNotIn(char, bare, f"{lang}.{key} has a bare {char!r}")
                self.assertEqual(text.count("<b>"), text.count("</b>"), f"{lang}.{key} unbalanced <b>")

    def test_kazakh_and_russian_are_translated(self):
        """Catch copy-paste: most texts must differ from English."""
        en = STRINGS["en"]
        for lang in ("kk", "ru"):
            same = [key for key, text in STRINGS[lang].items() if text == en[key]]
            self.assertLess(len(same), len(en) // 20, f"{lang} identical to English: {same}")


class FunctionsTest(unittest.TestCase):
    def test_detect_lang(self):
        self.assertEqual(detect_lang("kk"), "kk")
        self.assertEqual(detect_lang("ru"), "ru")
        self.assertEqual(detect_lang("en"), "en")
        self.assertEqual(detect_lang("ru-RU"), "ru")
        self.assertEqual(detect_lang("KK"), "kk")
        self.assertEqual(detect_lang("uk"), "en")
        self.assertEqual(detect_lang("de"), "en")
        self.assertEqual(detect_lang(""), "en")
        self.assertEqual(detect_lang(None), "en")

    def test_t_formats_and_falls_back(self):
        self.assertEqual(t("photo_added", "en", count=1, max=3), "Photo 1/3 added.")
        self.assertEqual(t("cancelled", "ru"), "Отменено.")
        self.assertEqual(t("cancelled", "xx"), "Cancelled.")  # unknown language: English
        self.assertEqual(t("cancelled", None), "Cancelled.")
        with self.assertRaises(KeyError):
            t("no_such_key", "en")

    def test_all_translations(self):
        labels = all_translations("btn_new_listing")
        self.assertEqual(labels, {STRINGS[lang]["btn_new_listing"] for lang in LANGS})
        self.assertIn("➕ New listing", labels)

    def test_menu_buttons_do_not_collide(self):
        keys = ("btn_new_listing", "btn_my_listings", "btn_website", "btn_language")
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                self.assertFalse(all_translations(a) & all_translations(b), f"{a} and {b} share a label")

    def test_categories(self):
        self.assertEqual(category_name("Motors", "en"), "Motors")
        self.assertEqual(category_name("Motors", "ru"), "Моторы")
        self.assertEqual(category_name("Unknown thing", "kk"), "Unknown thing")
        for name, names in CATEGORY_NAMES.items():
            self.assertEqual(set(names), {"ru", "kk"}, name)
            for text in names.values():
                self.assertNotIn("&", text)

    def test_bot_profile_limits(self):
        for lang in LANGS:
            self.assertIn(i18n.SLOGAN, short_description(lang))
            self.assertLessEqual(len(short_description(lang)), 120, lang)
            self.assertTrue(description(lang).startswith(f"{i18n.BRAND}: {i18n.SLOGAN}"))
            self.assertLessEqual(len(description(lang)), 512, lang)
            for key in ("cmd_start", "cmd_help", "cmd_cancel", "cmd_lang", "cmd_site"):
                self.assertLessEqual(len(t(key, lang)), 256)


if __name__ == "__main__":
    unittest.main()
