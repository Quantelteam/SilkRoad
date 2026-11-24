from aiogram import F

# Free-text input inside a step: never swallow commands like /cancel.
PLAIN_TEXT = F.text & ~F.text.startswith("/")
