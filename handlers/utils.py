"""Shared utility functions for the grocery bot."""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_list_with_toggle_buttons(items: list) -> tuple[str, InlineKeyboardMarkup | None]:
    """Build the grocery list message with only toggle buttons.
    
    Args:
        items: List of grocery items from the database
        
    Returns:
        Tuple of (message_text, reply_markup)
    """
    if not items:
        return (
            "📝 Your grocery list is empty!\n\n"
            "Use /add <item> to add items to the list.",
            None
        )
    
    list_text = "🛒 Your Grocery List:\n\n"
    keyboard = []
    
    for index, item in enumerate(items, start=1):
        item_id = item["id"]
        item_name = item["item"]
        completed = item["completed"]
        
        # Toggle button - shows item name with status
        if completed:
            toggle_text = f"✅ {item_name}"
            toggle_callback = f"toggle_{item_id}"
        else:
            toggle_text = f"{item_name}"
            toggle_callback = f"toggle_{item_id}"
        
        keyboard.append([
            InlineKeyboardButton(toggle_text, callback_data=toggle_callback)
        ])
    
    list_text += f"📊 Total: {len(items)} item(s)\n"
    list_text += "Tap to mark items done/undone"
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    return list_text, reply_markup


def build_list_with_remove_buttons(items: list) -> tuple[str, InlineKeyboardMarkup | None]:
    """Build the grocery list message with only remove buttons.
    
    Args:
        items: List of grocery items from the database
        
    Returns:
        Tuple of (message_text, reply_markup)
    """
    if not items:
        return (
            "📝 Your grocery list is empty!\n\n"
            "Use /add <item> to add items to the list.",
            None
        )
    
    list_text = "🛒 Your Grocery List:\n\n"
    keyboard = []
    
    for index, item in enumerate(items, start=1):
        item_id = item["id"]
        item_name = item["item"]
        completed = item["completed"]
        
        # Format item with check mark if completed
        if completed:
            list_text += f"{index}. ✅ ~~{item_name}~~\n"
        else:
            list_text += f"{index}. {item_name}\n"
        
        # Remove button - shows item name
        remove_text = f"🗑️ {item_name}"
        remove_callback = f"remove_{item_id}"
        
        keyboard.append([
            InlineKeyboardButton(remove_text, callback_data=remove_callback)
        ])
    
    list_text += f"\n📊 Total: {len(items)} item(s)\n"
    list_text += "Tap to remove items"
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    return list_text, reply_markup
