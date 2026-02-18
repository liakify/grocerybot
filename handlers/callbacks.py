"""Callback query handler for inline button clicks."""
import logging

from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

import database
from handlers.utils import build_list_with_toggle_buttons, build_list_with_remove_buttons

logger = logging.getLogger(__name__)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle callback queries from inline buttons."""
    query = update.callback_query
    await query.answer()  # Answer the callback to stop loading animation
    
    chat_id = query.message.chat.id
    data = query.data
    
    # Parse callback data: action_itemid (e.g., "toggle_1" or "remove_1")
    try:
        action, item_id_str = data.rsplit("_", 1)
        item_id = int(item_id_str)
    except (ValueError, AttributeError):
        logger.error(f"Invalid callback data: {data}")
        return
    
    if action == "toggle":
        # Toggle item completion status
        new_status = database.toggle_item_completed(chat_id, item_id)
        if new_status is None:
            await query.edit_message_text("❌ Item not found!")
            return
        
        status_text = "completed ✅" if new_status else "uncompleted"
        await query.edit_message_text(f"Item marked as {status_text}")
        
        # Show updated list with toggle buttons
        items = database.get_items(chat_id)
        list_text, reply_markup = build_list_with_toggle_buttons(items)
        await query.message.edit_text(
            list_text, 
            reply_markup=reply_markup, 
            parse_mode="Markdown"
        )
        
    elif action == "remove":
        # Remove item
        removed_item = database.remove_item_by_id(chat_id, item_id)
        if removed_item is None:
            await query.edit_message_text("❌ Item not found!")
            return
        
        await query.edit_message_text(f"✅ Removed '{removed_item}' from the list!")
        
        # Show updated list with remove buttons
        items = database.get_items(chat_id)
        list_text, reply_markup = build_list_with_remove_buttons(items)
        await query.message.edit_text(
            list_text, 
            reply_markup=reply_markup, 
            parse_mode="Markdown"
        )
    
    logger.info(f"Chat {chat_id}: Callback {action} for item {item_id}")


def get_callback_handler():
    """Return the callback query handler."""
    return CallbackQueryHandler(callback_handler)
