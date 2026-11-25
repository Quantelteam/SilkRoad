"""Catalog part picker shared by the create and edit flows.

A flow calls `ask_part(...)` with a flow name; when the user has chosen a
catalog part or confirmed free text, the resolver registered for that flow is
called with `(message, state, part, text)`.
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
from app.keyboards import inline
from app.states import EditListing, NewListing
from app.texts import part_label

router = Router()

Resolver = Callable[[Message, FSMContext, dict | None, str | None], Awaitable[None]]
RESOLVERS: dict[str, Resolver] = {}

PICK_STATES = StateFilter(NewListing.part, EditListing.part)
MAX_FREE_TEXT = 80

HINT = ("\n\nType a part name to search the catalog, browse the categories, "
        "or tap Other to write your own.")
OTHER = ("✏️ Other: write my own", "pk:other")


def _program(user: dict | None) -> str:
    """FLL teams pick from the LEGO catalog, FTC teams from the FTC one."""
    team = (user or {}).get("team") or {}
    return "FLL" if team.get("program") == "FLL" else "FTC"


async def ask_part(message: Message, state: FSMContext, prompt: str,
                   flow: str, pick_state: State) -> None:
    await state.update_data(pick_flow=flow, pick_query=None, pick_free=False)
    await state.set_state(pick_state)
    await message.answer(prompt + HINT,
                         reply_markup=inline([[("📂 Categories", "pk:cats")], [OTHER]]))


async def _resolve(message: Message, state: FSMContext,
                   part: dict | None, text: str | None) -> None:
    data = await state.get_data()
    await RESOLVERS[data["pick_flow"]](message, state, part, text)


@router.message(PICK_STATES, PLAIN_TEXT)
async def search(message: Message, state: FSMContext, user: dict | None) -> None:
    query = message.text.strip()
    if len(query) < 2:
        await message.answer("Type at least 2 characters.")
        return
    if len(query) > MAX_FREE_TEXT:
        await message.answer(f"Too long, keep it under {MAX_FREE_TEXT} characters.")
        return

    data = await state.get_data()
    if data.get("pick_free"):
        await state.update_data(pick_free=False)
        await message.answer(f"Selected: <b>{escape(query)}</b>")
        await _resolve(message, state, None, query)
        return

    await state.update_data(pick_query=query)
    parts = await db.search_parts(query, _program(user))
    rows = [[(part_label(p), f"pk:id:{p['id']}")] for p in parts]
    rows.append([(f'✍️ Use "{query}" as typed', "pk:raw")])
    rows.append([("📂 Categories", "pk:cats")])
    rows.append([OTHER])
    header = "Catalog matches:" if parts else "Nothing in the catalog matches that."
    await message.answer(header, reply_markup=inline(rows))


@router.callback_query(PICK_STATES, F.data == "pk:cats")
async def show_categories(call: CallbackQuery, state: FSMContext, user: dict | None) -> None:
    categories = await db.list_categories(_program(user))
    await state.update_data(pick_cats=categories, pick_free=False)
    rows = [[(name, f"pk:cat:{i}")] for i, name in enumerate(categories)]
    rows.append([OTHER])
    await call.message.edit_text("Pick a category, or tap Other if your part isn't listed:",
                                 reply_markup=inline(rows))
    await call.answer()


@router.callback_query(PICK_STATES, F.data.startswith("pk:cat:"))
async def show_category(call: CallbackQuery, state: FSMContext, user: dict | None) -> None:
    data = await state.get_data()
    categories = data.get("pick_cats") or await db.list_categories(_program(user))
    index = int(call.data.split(":")[2])
    if index >= len(categories):
        await call.answer("Category is gone, search by name instead.", show_alert=True)
        return

    parts = await db.parts_in_category(categories[index], _program(user))
    rows = [[(part_label(p), f"pk:id:{p['id']}")] for p in parts]
    rows.append([("⬅️ Categories", "pk:cats")])
    rows.append([OTHER])
    await call.message.edit_text(f"<b>{categories[index]}</b>", reply_markup=inline(rows))
    await call.answer()


@router.callback_query(PICK_STATES, F.data.startswith("pk:id:"))
async def choose_part(call: CallbackQuery, state: FSMContext) -> None:
    part = await db.get_part(int(call.data.split(":")[2]))
    if part is None:
        await call.answer("That part is no longer in the catalog.", show_alert=True)
        return
    await call.message.edit_text(f"Selected: <b>{part_label(part)}</b>")
    await call.answer()
    await _resolve(call.message, state, part, None)


@router.callback_query(PICK_STATES, F.data == "pk:raw")
async def choose_free_text(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    text = data.get("pick_query")
    if not text:
        await call.answer("Type the part name first.", show_alert=True)
        return
    await call.message.edit_text(f"Selected: <b>{escape(text)}</b>")
    await call.answer()
    await _resolve(call.message, state, None, text)


@router.callback_query(PICK_STATES, F.data == "pk:other")
async def choose_other(call: CallbackQuery, state: FSMContext) -> None:
    """The part isn't in the catalog: the next message is its name, as written."""
    await state.update_data(pick_free=True)
    await call.message.edit_text(
        f"Write the part as you want it to appear, up to {MAX_FREE_TEXT} characters. "
        "For example: LEGO Technic beam 15, grey, 20 pcs."
    )
    await call.answer()
