"""Main bot application for GroceryBot."""
import json
import logging
from datetime import datetime
from telegram.ext import (
    Application,
    CommandHandler,
)

import config
import database
from handlers import (
    add_command,
    remove_command,
    list_command,
    clear_command,
    help_command,
    get_callback_handler,
)


class JSONFormatter(logging.Formatter):
    """JSON log formatter."""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)


# Configure logging
handler = logging.StreamHandler(config.LOG_STREAM)
handler.setFormatter(JSONFormatter())

root_logger = logging.getLogger()
root_logger.setLevel(getattr(logging, config.LOG_LEVEL))
root_logger.addHandler(handler)

logger = logging.getLogger(__name__)


async def error_handler(update, context):
    """Handle errors in the bot."""
    logger.error(f"Error: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred. Please try again."
        )


async def start_command(update, context):
    """Handle /start command."""
    await update.message.reply_text(
        "👋 Welcome to GroceryBot!\n\n"
        "I help manage shared grocery lists in group chats.\n\n"
        "Use /help to see available commands."
    )


def main():
    """Start the bot."""
    # Check if bot token is configured
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN not found! Please set it in .env file.")
        print("ERROR: BOT_TOKEN not found!")
        print("Please create a .env file with BOT_TOKEN=your_token_here")
        return
    
    # Initialize database
    try:
        database.init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return
    
    # Create the application
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("add", add_command))
    application.add_handler(CommandHandler("remove", remove_command))
    application.add_handler(CommandHandler("list", list_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Add callback query handler for inline buttons
    application.add_handler(get_callback_handler())
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Log startup
    logger.info("GroceryBot is starting...")
    print("🤖 GroceryBot is running! Press Ctrl+C to stop.")
    
    # Start polling (for development)
    # Use webhook in production: application.run_webhook(...)
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
