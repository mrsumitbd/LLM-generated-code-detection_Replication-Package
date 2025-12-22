def get_subscription_options_keyboard(subscription_options: Dict[
    int, Optional[int]], currency_symbol_val: str, lang: str,
                                      i18n_instance) -> InlineKeyboardMarkup:
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = []
    
    for price, discount in subscription_options.items():
        if discount is not None:
            button_text = f"{currency_symbol_val}{price} (-{discount}%)"
            callback_data = f"subscribe_{price}_{discount}"
        else:
            button_text = f"{currency_symbol_val}{price}"
            callback_data = f"subscribe_{price}"
        
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    
    cancel_text = i18n_instance.t("cancel", locale=lang)
    keyboard.append([InlineKeyboardButton(cancel_text, callback_data="cancel_subscription")])
    
    return InlineKeyboardMarkup(keyboard)