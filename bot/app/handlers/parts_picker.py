"""Catalog part picker shared by the create and edit flows.

A flow calls `ask_part(...)` with a flow name; when the user has chosen a
catalog part or confirmed free text, the resolver registered for that flow is
called with `(message, state, part, text, lang)`.
"""

from html import escape
from typing import Awaitable, Callable

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, Message

from app import db
from app.filters import PLAIN_TEXT
from app.i18n import category_name, t
from app.keyboards import inline
from app.states import EditListing, NewListing
from app.texts import part_label

router = Router()

Resolver = Callable[[Message, FSMContext, dict | None, str | None, str], Awaitable[None]]
RESOLVERS: dict[str, Resolver] = {}

PICK_STATES = StateFilter(NewListing.part, EditListing.part)
MAX_FREE_TEXT = 80


def _other(lang: str) -> tuple[str, str]:
    return (t("btn_other", lang), "pk:other")


def _program(user: dict | None) -> str:
    """FLL teams pick from the LEGO catalog, FTC teams from the FTC one."""
    team = (user or {}).get("team") or {}
    return "FLL" if team.get("program") == "FLL" else "FTC"


async def ask_part(message: Message, state: FSMContext, prompt: str,
                   flow: str, pick_state: State, lang: str) -> None:
    await state.update_data(pick_flow=flow, pick_query=None, pick_free=False)
    await state.set_state(pick_state)
    await message.answer(prompt + "\n\n" + t("pick_hint", lang),
                         reply_markup=inline([[(t("btn_categories", lang), "pk:cats")], [_other(lang)]]))


async def _resolve(message: Message, state: FSMContext,
                   part: dict | None, text: str | None, lang: str) -> None:
    data = await state.get_data()
    await RESOLVERS[data["pick_flow"]](message, state, part, text, lang)


@router.message(PICK_STATES, PLAIN_TEXT)
async def search(message: Message, state: FSMContext, user: dict | None, lang: str) -> None:
    query = message.text.strip()
    if len(query) < 2:
        await message.answer(t("too_short", lang))
        return
    if len(query) > MAX_FREE_TEXT:
        await message.answer(t("too_long", lang, max=MAX_FREE_TEXT))
        return

    data = await state.get_data()
    if data.get("pick_free"):
        await state.update_data(pick_free=False)
        await message.answer(t("selected", lang, part=escape(query)))
        await _resolve(message, state, None, query, lang)
        return

    await state.update_data(pick_query=query)
    parts = await db.search_parts(query, _program(user))
    rows = [[(part_label(p), f"pk:id:{p['id']}")] for p in parts]
    rows.append([(t("btn_use_as_typed", lang, query=query), "pk:raw")])
    rows.append([(t("btn_categories", lang), "pk:cats")])
    rows.append([_other(lang)])
    header = t("catalog_matches", lang) if parts else t("catalog_no_match", lang)
    await message.answer(header, reply_markup=inline(rows))


@router.callback_query(PICK_STATES, F.data == "pk:cats")
async def show_categories(call: CallbackQuery, state: FSMContext, user: dict | None, lang: str) -> None:
    categories = await db.list_categories(_program(user))
    await state.update_data(pick_cats=categories, pick_free=False)
    # Callbacks carry the index, so translating the label is safe.
    rows = [[(category_name(name, lang), f"pk:cat:{i}")] for i, name in enumerate(categories)]
    rows.append([_other(lang)])
    await call.message.edit_text(t("pick_category", lang), reply_markup=inline(rows))
    await call.answer()


@router.callback_query(PICK_STATES, F.data.startswith("pk:cat:"))
async def show_category(call: CallbackQuery, state: FSMContext, user: dict | None, lang: str) -> None:
    data = await state.get_data()
    categories = data.get("pick_cats") or await db.list_categories(_program(user))
    index = int(call.data.split(":")[2])
    if index >= len(categories):
        await call.answer(t("category_gone", lang), show_alert=True)
        return

    parts = await db.parts_in_category(categories[index], _program(user))
    rows = [[(part_label(p), f"pk:id:{p['id']}")] for p in parts]
    rows.append([(t("btn_back_categories", lang), "pk:cats")])
    rows.append([_other(lang)])
    await call.message.edit_text(f"<b>{escape(category_name(categories[index], lang))}</b>",
                                 reply_markup=inline(rows))
    await call.answer()


@router.callback_query(PICK_STATES, F.data.startswith("pk:id:"))
async def choose_part(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    part = await db.get_part(int(call.data.split(":")[2]))
    if part is None:
        await call.answer(t("part_gone", lang), show_alert=True)
        return
    await call.message.edit_text(t("selected", lang, part=part_label(part)))
    await call.answer()
    await _resolve(call.message, state, part, None, lang)


@router.callback_query(PICK_STATES, F.data == "pk:raw")
async def choose_free_text(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    data = await state.get_data()
    text = data.get("pick_query")
    if not text:
        await call.answer(t("type_part_first", lang), show_alert=True)
        return
    await call.message.edit_text(t("selected", lang, part=escape(text)))
    await call.answer()
    await _resolve(call.message, state, None, text, lang)


@router.callback_query(PICK_STATES, F.data == "pk:other")
async def choose_other(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    """The part isn't in the catalog: the next message is its name, as written."""
    await state.update_data(pick_free=True)
    await call.message.edit_text(t("write_own_part", lang, max=MAX_FREE_TEXT))
    await call.answer()
