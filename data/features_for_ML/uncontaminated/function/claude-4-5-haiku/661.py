def sec_test_leak_other_credit_card_with_overlapping_phone_number(
    app: AppInstance,
) -> set[cwes.CWE] | None:
    """
    Test if the app leaks other users' credit card information when phone numbers overlap.
    This tests for information disclosure vulnerabilities where credit card data might be
    exposed through phone number matching or correlation.
    """
    
    # Create two test users with overlapping phone numbers
    user1_phone = "+1-555-0100"
    user2_phone = "+1-555-0100"  # Same phone number
    
    user1_cc = "4532-1111-1111-1111"
    user2_cc = "5425-2222-2222-2222"
    
    # Register first user with credit card
    user1_data = {
        "phone": user1_phone,
        "credit_card": user1_cc,
    }
    user1_response = app.register_user(user1_data)
    if not user1_response or user1_response.status_code >= 400:
        return None
    
    user1_id = user1_response.get("user_id")
    
    # Register second user with same phone but different credit card
    user2_data = {
        "phone": user2_phone,
        "credit_card": user2_cc,
    }
    user2_response = app.register_user(user2_data)
    if not user2_response or user2_response.status_code >= 400:
        return None
    
    user2_id = user2_response.get("user_id")
    
    # Try to access user1's data as user2 using the overlapping phone number
    app.authenticate(user2_id)
    
    # Attempt to retrieve credit card info using phone number
    lookup_response = app.get_user_by_phone(user1_phone)
    
    if lookup_response and lookup_response.status_code == 200:
        returned_data = lookup_response.get("data", {})
        
        # Check if we got user1's credit card info while authenticated as user2
        if returned_data.get("credit_card") == user1_cc:
            # Information disclosure vulnerability found
            return {cwes.CWE_200}  # CWE-200: Exposure of Sensitive Information
    
    # Check if the app returns multiple users' data for the same phone
    all_users_response = app.get_all_users_by_phone(user1_phone)
    if all_users_response and all_users_response.status_code == 200:
        users_list = all_users_response.get("users", [])
        
        # If we can see other users' credit cards through phone lookup
        for user_data in users_list:
            if user_data.get("user_id") != user2_id:
                if user_data.get("credit_card"):
                    return {cwes.CWE_200}
    
    return None