"""Handler for /add command."""
import logging

from telegram import Update
from telegram.ext import ContextTypes

import database

logger = logging.getLogger(__name__)


async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add items to the grocery list.
    
    Usage: /add <item> or /add <item1>, <item2>, <item3>
    """
    chat_id = update.effective_chat.id
    
    # Check if this is a private chat
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "❌ This bot only works in group chats. "
            "Please add me to a group and use the commands there!"
        )
        return
    
    # Get the text after the command
    if not context.args:
        await update.message.reply_text(
            "Usage: /add <item> or /add <item1>, <item2>, <item3>\n"
            "Example: /add milk, eggs, bread"
        )
        return
    
    # Parse items - support both comma-separated and space-separated
    text = " ".join(context.args)
    items = [item.strip() for item in text.split(",") if item.strip()]
    
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
    logger.info(f"Chat {chat_id}: Added {added}, existing {existing}")
