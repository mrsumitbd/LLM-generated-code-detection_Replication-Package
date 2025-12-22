from typing import Dict, Optional
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def get_subscription_options_keyboard(subscription_options: Dict[
    int, Optional[int]], currency_symbol_val: str, lang: str,
                                      i18n_instance) -> InlineKeyboardMarkup:
    keyboard = []
    for plan_id, price in subscription_options.items():
        if price is not None:
            plan_name = i18n_instance.t(f'subscription_plan_{plan_id}', lang=lang)
            plan_price = f"{currency_symbol_val}{price:.2f}"
            keyboard.append([InlineKeyboardButton(
                f"{plan_name} - {plan_price}",
                callback_data=f"subscribe_{plan_id}"
            )])
    return InlineKeyboardMarkup(keyboard)