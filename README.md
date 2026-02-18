# GroceryBot 🤖🛒

A Telegram bot that manages shared grocery lists in group chats. Each group gets its own independent grocery list!

## Features

- **Add Items** - Add one or multiple items to the grocery list
- **Mark Complete** - Mark items as done using inline buttons from `/list`
- **Remove Items** - Remove items using inline buttons from `/remove`
- **View List** - See all items with completion status via `/list`
- **Clear List** - Clear all items at once
- **Per-Group Lists** - Each group has its own separate list

## Requirements

- Python 3.10 or higher
- Telegram account
- Telegram Bot Token (from @BotFather)

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the bot**
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Telegram bot token:
   ```
   BOT_TOKEN=your_bot_token_here
   ```

5. **Get a bot token**
   
   - Open Telegram and search for @BotFather
   - Send `/newbot` to create a new bot
   - Follow the instructions and copy your bot token
   - Paste the token in your `.env` file

## Usage

Run the bot:
```bash
python bot.py
```

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/add` | Add item(s) to the list | `/add milk, eggs` |
| `/list` | Show list with toggle buttons | `/list` |
| `/remove` | Show list with remove buttons | `/remove` |
| `/clear` | Clear all items from the list | `/clear` |
| `/help` | Show help message | `/help` |

## Adding the Bot to a Group

1. Create a new group in Telegram (or use an existing one)
2. Search for your bot by username and add it to the group
3. Make sure the bot has permission to send messages
4. Start using the commands!

## Project Structure

```
grocerybot/
├── bot.py              # Main bot application
├── config.py           # Configuration management
├── database.py         # Database operations
├── handlers/           # Command handlers
│   ├── __init__.py
│   ├── add.py
│   ├── remove.py
│   ├── list.py
│   ├── clear.py
│   └── help.py
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

## How It Works

- Each group chat has its own grocery list stored in a SQLite database
- The bot uses the group's chat ID to keep lists separate
- All data is persisted in `grocerybot.db`
- The bot only works in group chats (not private chats)

## License

MIT License - Feel free to use and modify!

## Contributing

Pull requests are welcome! If you find any issues, please open an issue.
