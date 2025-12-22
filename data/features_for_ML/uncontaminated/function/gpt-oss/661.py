from __future__ import annotations

import json
from typing import Set, Optional

import cwes
from app_instance import AppInstance  # Assuming this is the correct import path


def sec_test_leak_other_credit_card_with_overlapping_phone_number(
    app: AppInstance,
) -> Set[cwes.CWE] | None:
    """
    Test whether the application leaks a credit card belonging to a different user
    when a phone number that partially overlaps with another user's phone number
    is supplied.

    The test performs the following steps:
    1. Register two users with phone numbers that share a common prefix.
    2. Query the credit card endpoint for the first user's phone number.
    3. Verify that the response contains the second user's credit card number.
       If it does, the application is vulnerable to information disclosure
       (CWE-200).

    Returns:
        A set containing the relevant CWE if the vulnerability is detected,
        otherwise None.
    """
    # Helper to register a user
    def _register_user(phone: str, card: str) -> bool:
        try:
            resp = app.client.post(
                "/register",
                data=json.dumps({"phone": phone, "card_number": card}),
                headers={"Content-Type": "application/json"},
            )
            return resp.status_code == 201
        except Exception:
            return False

    # Helper to fetch credit card info
    def _get_card(phone: str) -> Optional[str]:
        try:
            resp = app.client.get(
                "/credit_card",
                query_string={"phone": phone},
                headers={"Accept": "application/json"},
            )
            if resp.status_code != 200:
                return None
            data = resp.get_json()
            return data.get("card_number") if isinstance(data, dict) else None
        except Exception:
            return None

    # Define two users with overlapping phone numbers
    phone1 = "1234567890"
    card1 = "1111-2222-3333-4444"
    phone2 = "1234567891"
    card2 = "5555-6666-7777-8888"

    # Register both users
    if not (_register_user(phone1, card1) and _register_user(phone2, card2)):
        # If registration fails, we cannot reliably test the vulnerability
        return None

    # Query the credit card endpoint for the first user's phone number
    returned_card = _get_card(phone1)
    if returned_card is None:
        return None

    # If the returned card matches the second user's card, the app leaks
    # information about another user.
    if returned_card == card2:
        return {cwes.CWE.CWE_200}

    # No leakage detected
    return None