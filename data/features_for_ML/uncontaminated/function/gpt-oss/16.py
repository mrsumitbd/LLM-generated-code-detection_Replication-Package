def search_emails_handler(args, context):
    """
    Search emails based on provided arguments.

    Expected `args` keys:
        - search_term (str): term to search for in subject or snippet.
        - max_results (int, optional): maximum number of results to return.
        - offset (int, optional): number of results to skip (for pagination).

    Returns:
        dict: {
            "results": [list of email dicts],
            "total": int (total matches found),
            "offset": int,
            "limit": int
        }
    """
    # Basic validation
    if not isinstance(args, dict):
        raise ValueError("args must be a dictionary")

    search_term = args.get("search_term", "").lower()
    max_results = args.get("max_results", 10)
    offset = args.get("offset", 0)

    if not isinstance(search_term, str):
        raise ValueError("search_term must be a string")
    if not isinstance(max_results, int) or max_results < 0:
        raise ValueError("max_results must be a non‑negative integer")
    if not isinstance(offset, int) or offset < 0:
        raise ValueError("offset must be a non‑negative integer")

    # Dummy email dataset (in a real implementation this would come from a DB or service)
    EMAILS = [
        {"id": 1, "subject": "Meeting Reminder", "sender": "alice@example.com",
         "snippet": "Don't forget our meeting tomorrow at 10am."},
        {"id": 2, "subject": "Project Update", "sender": "bob@example.com",
         "snippet": "The project is on track for the deadline."},
        {"id": 3, "subject": "Lunch Invitation", "sender": "carol@example.com",
         "snippet": "Would you like to grab lunch today?"},
        {"id": 4, "subject": "Re: Meeting Reminder", "sender": "dave@example.com",
         "snippet": "Thanks for the reminder! See you then."},
        {"id": 5, "subject": "Weekly Report", "sender": "eve@example.com",
         "snippet": "Attached is the weekly report for your review."},
        {"id": 6, "subject": "Birthday Party", "sender": "frank@example.com",
         "snippet": "You're invited to my birthday party next Saturday."},
        {"id": 7, "subject": "Invoice", "sender": "grace@example.com",
         "snippet": "Please find the invoice attached."},
        {"id": 8, "subject": "Re: Project Update", "sender": "heidi@example.com",
         "snippet": "Great news! The project is ahead of schedule."},
        {"id": 9, "subject": "Security Alert", "sender": "ivan@example.com",
         "snippet": "Please reset your password immediately."},
        {"id": 10, "subject": "Re: Security Alert", "sender": "judy@example.com",
         "snippet": "Password reset completed successfully."},
    ]

    # Filter emails by search term in subject or snippet
    matches = []
    for email in EMAILS:
        if search_term in email["subject"].lower() or search_term in email["snippet"].lower():
            matches.append(email)

    total_matches = len(matches)

    # Apply pagination
    paginated = matches[offset:offset + max_results]

    # Prepare response
    response = {
        "results": paginated,
        "total": total_matches,
        "offset": offset,
        "limit": max_results
    }

    # Log if logger available
    logger = None
    if context and isinstance(context, dict):
        logger = context.get("logger")
    if logger:
        try:
            logger.info(f"search_emails_handler: found {total_matches} matches, returning {len(paginated)}")
        except Exception:
            pass

    return response