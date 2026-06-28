"""Handler for /clear command."""
import logging

from telegram import Update
from telegram.ext import ContextTypes

import database

logger = logging.getLogger(__name__)


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Clear all items from the grocery list.
    
    Usage: /clear
    """
    chat_id = update.effective_chat.id
    
    # Check if this is a private chat
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "❌ This bot only works in group chats. "
            "Please add me to a group and use the commands there!"
        )
        return
    
    # Check if list is already empty
    count = database.get_item_count(chat_id)
    if count == 0:
        await update.message.reply_text(
            "📝 The grocery list is already empty!"
        )
        return
    
    # Clear the list
    removed = database.clear_list(chat_id)
    
    await update.message.reply_text(
        f"🗑️ Cleared {removed} item(s) from the grocery list!"
    )
    logger.info("List cleared", extra={"chat_id": chat_id, "removed": removed})
