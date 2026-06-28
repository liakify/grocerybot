# GroceryBot

Python 3.10+ Telegram bot for shared group grocery lists. Uses `python-telegram-bot` v20+ (async) and SQLite.

## Setup & Run

```bash
pip install -r requirements.txt
cp .env.example .env   # then add BOT_TOKEN from @BotFather
python bot.py
```

- `config.py` loads `.env` via `python-dotenv`; `BOT_TOKEN` is required, `LOG_LEVEL` optional (default INFO).
- Runs polling via `application.run_polling(drop_pending_updates=True)`. For production, switch to `run_webhook` in `bot.py:105`.

## Architecture

- **Entrypoint**: `bot.py:main()` — inits DB, registers command handlers, starts polling.
- **Commands**: `/start`, `/add`, `/remove`, `/list`, `/clear`, `/help` — each in `handlers/<cmd>.py`.
- **Inline buttons**: callback data format `{action}_{item_id}` (e.g. `toggle_3`, `remove_7`). Handled in `handlers/callbacks.py`.
- **Private chat guard**: All group commands check `update.effective_chat.type == "private"` and refuse.
- **Logging**: JSON-structured to stdout via custom `JSONFormatter` in `bot.py:22`.

## Database

- Auto-created SQLite file at `grocerybot.db` (gitignored, listed in `.gitignore`).
- Single table `grocery_items` with `id`, `chat_id`, `item` (case-insensitive unique per chat), `completed` (0/1), `added_at`.
- `database.init_database()` runs `CREATE TABLE IF NOT EXISTS` + `CREATE INDEX` on startup; also handles migration for existing DBs missing the `completed` column.

## No Tests / Lint / Typechecking

This repo has **no test suite, no linter config, no type checker config, and no CI**. No verification commands exist or are expected.

## Callback Flow

`/list` → `build_list_with_toggle_buttons` → each row has one button with `toggle_{id}`. Tap toggles completion and re-renders the list.
`/remove` → `build_list_with_remove_buttons` → each row has one button with `remove_{id}`. Tap deletes the item and re-renders the list.
