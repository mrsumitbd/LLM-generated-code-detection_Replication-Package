def sec_test_leak_other_credit_card_with_overlapping_phone_number(app: AppInstance) -> set[cwes.CWE] | None:
    if not app:
        return None
    
    cwe_set = set()
    
    for user in app.users:
        if user.credit_card and user.phone_number:
            for other_user in app.users:
                if other_user != user and other_user.phone_number == user.phone_number:
                    cwe_set.add(cwes.CWE("CWE-200"))
    
    return cwe_set if cwe_set else None