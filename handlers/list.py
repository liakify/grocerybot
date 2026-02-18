"""Handler for /list command."""
import logging

from telegram import Update
from telegram.ext import ContextTypes

import database
from handlers.utils import build_list_with_toggle_buttons

logger = logging.getLogger(__name__)


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the current grocery list with toggle buttons."""
    chat_id = update.effective_chat.id
    
    # Check if this is a private chat
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "❌ This bot only works in group chats. "
            "Please add me to a group and use the commands there!"
        )
        return
    
    items = database.get_items(chat_id)
    list_text, reply_markup = build_list_with_toggle_buttons(items)
    
    await update.message.reply_text(
        list_text, 
        reply_markup=reply_markup, 
        parse_mode="Markdown"
    )
    logger.info(f"Chat {chat_id}: Listed {len(items)} items with toggle buttons")
