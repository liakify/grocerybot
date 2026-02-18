"""Handler for /help command."""
import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


HELP_TEXT = """🛒 **GroceryBot Help**

I help manage a shared grocery list for your group!

**Commands:**

• `/add <item>` - Add item(s) to the list
  Example: `/add milk, eggs`
  Example: `/add bread`

• `/remove` - Show list with remove buttons to delete items

• `/list` - Show list with toggle buttons to mark items done/undone

• `/clear` - Clear all items from the list

• `/help` - Show this help message

**How it works:**
- Use `/list` to mark items as done/undone (tap the item button)
- Use `/remove` to delete items (tap the 🗑️ button)
- Each group has its own separate list
- Items are case-insensitive

**Made with ❤️ for group shopping lists!"""


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show help information.
    
    Usage: /help
    """
    await update.message.reply_text(HELP_TEXT, parse_mode="Markdown")
    logger.info(f"Chat {update.effective_chat.id}: Help requested")
