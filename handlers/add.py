"""Handler for /add command."""
import logging

from telegram import Update
from telegram.ext import ContextTypes

import database

logger = logging.getLogger(__name__)


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add items to the grocery list.
    
    Usage: /add <item1> <item2> <item3>
    Items are separated by newlines.
    Example: /add milk eggs bread
    """
    chat_id = update.effective_chat.id
    
    # Check if this is a private chat
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "❌ This bot only works in group chats. "
            "Please add me to a group and use the commands there!"
        )
        return
    
    # Get the text after the command from the full message text
    message_text = update.effective_message.text
    parts = message_text.split(None, 1)
    cmd_text = parts[1] if len(parts) > 1 else ""
    
    if not cmd_text:
        await update.message.reply_text(
            "Usage: /add <item1> <item2> <item3>\n"
            "Example: /add milk eggs bread\n"
            "(items are separated by spaces/newlines)"
        )
        return
    
    # Parse items - split by newlines
    items = [item.strip() for item in cmd_text.split("\n") if item.strip()]
    
    if not items:
        await update.message.reply_text(
            "Please provide items to add.\n"
            "Usage: /add <item>"
        )
        return
    
    # Add items to database
    added, existing = database.add_items(chat_id, items)
    
    # Build response message
    if added == 0 and existing == 1:
        response = f"⚠️ '{items[0]}' is already in the list!"
    elif added == 1 and existing == 0:
        response = f"✅ Added '{items[0]}' to the grocery list!"
    elif added > 0 and existing == 0:
        response = f"✅ Added {added} items to the grocery list!"
    elif added > 0 and existing > 0:
        response = f"✅ Added {added} item(s). {existing} item(s) were already in the list."
    else:
        response = f"⚠️ All items are already in the list!"
    
    await update.message.reply_text(response)
    logger.info("Items added", extra={"chat_id": chat_id, "added": added, "existing": existing})
