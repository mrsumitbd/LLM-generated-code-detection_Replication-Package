from typing import Dict, Optional
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def get_subscription_options_keyboard(
    subscription_options: Dict[int, Optional[int]],
    currency_symbol_val: str,
    lang: str,
    i18n_instance,
) -> InlineKeyboardMarkup:
    """
    Build an inline keyboard with subscription options.

    Parameters
    ----------
    subscription_options : Dict[int, Optional[int]]
        Mapping of subscription option id to price in cents.  If the price is
        ``None`` the option is considered free.
    currency_symbol_val : str
        Currency symbol to prepend to the price (e.g. "$").
    lang : str
        Language code used for translations.
    i18n_instance : Any
        Instance providing a ``t`` method for translations.  The method
        signature is assumed to be ``t(key: str, **kwargs)`` and returns a
        translated string.

    Returns
    -------
    InlineKeyboardMarkup
        Keyboard markup ready to be sent with a bot message.
    """
    # Helper to format a single option
    def _format_option(opt_id: int, price_cents: Optional[int]) -> InlineKeyboardButton:
        if price_cents is None:
            # Free option
            text = i18n_instance.t("free", lang=lang)
        else:
            # Convert cents to dollars (or other currency) and format
            price = price_cents / 100
            price_str = f"{currency_symbol_val}{price:,.2f}"
            # Use a translation key that can accept a price placeholder
            text = i18n_instance.t("subscription_option", lang=lang, price=price_str)
        return InlineKeyboardButton(
            text=text,
            callback_data=f"subscribe_{opt_id}",
        )

    # Build rows of buttons (one button per row)
    rows = [[_format_option(opt_id, price)] for opt_id, price in sorted(subscription_options.items())]

    # Add a cancel button at the bottom
    cancel_text = i18n_instance.t("cancel", lang=lang)
    rows.append([InlineKeyboardButton(text=cancel_text, callback_data="cancel_subscription")])

    return InlineKeyboardMarkup(rows)