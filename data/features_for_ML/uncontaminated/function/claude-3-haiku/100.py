import stripe

def stripe_get_customers(api_key: str, **kwargs):
    """
    Retrieves a list of Stripe customers.

    Args:
        api_key (str): The Stripe API key.
        **kwargs: Additional parameters to be passed to the Stripe API.

    Returns:
        list: A list of Stripe customer objects.
    """
    stripe.api_key = api_key
    customers = stripe.Customer.list(**kwargs)
    return list(customers.auto_paging_iter())