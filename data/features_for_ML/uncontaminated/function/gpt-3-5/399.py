from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Dict, Optional

def get_subscription_options_keyboard(subscription_options: Dict[int, Optional[int]], currency_symbol_val: str, lang: str, i18n_instance) -> InlineKeyboardMarkup:
    keyboard = []
    for key, value in subscription_options.items():
        if value is not None:
            text = f"{value} {currency_symbol_val}"
        else:
            text = "Free"
        callback_data = f"subscribe_{key}"
        keyboard.append([InlineKeyboardButton(text, callback_data=callback_data)])
    return InlineKeyboardMarkup(keyboard)