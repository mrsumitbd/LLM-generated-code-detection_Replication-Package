def sec_test_leak_other_credit_card_with_overlapping_phone_number(
    app: AppInstance,
) -> set[cwes.CWE] | None:
    try:
        credit_cards = app.get_credit_cards()
        phone_numbers = app.get_phone_numbers()
        leaked_credit_cards = set()

        for card in credit_cards:
            for number in phone_numbers:
                if app.check_phone_number_overlap(card, number):
                    leaked_credit_cards.add(card)
                    break

        if leaked_credit_cards:
            return {cwes.CWE_359}
        else:
            return None
    except Exception:
        return {cwes.CWE_500}