import stripe
from typing import Any, Dict, List, Optional

def stripe_get_customers(api_key: str, **kwargs: Any) -> List[Dict[str, Any]]:
    """
    Retrieve a list of Stripe customers.

    Parameters
    ----------
    api_key : str
        Your Stripe secret key.
    **kwargs : Any
        Optional parameters to pass to `stripe.Customer.list`. Common
        options include:
            - limit (int): Number of customers to return.
            - starting_after (str): ID of the last customer seen in the previous page.
            - ending_before (str): ID of the first customer seen in the previous page.
            - email (str): Filter customers by email.
            - status (str): Filter customers by status.

    Returns
    -------
    List[Dict[str, Any]]
        A list of customer objects represented as dictionaries.

    Raises
    ------
    stripe.error.StripeError
        If the Stripe API call fails.
    """
    stripe.api_key = api_key

    try:
        # stripe.Customer.list returns a stripe.ListObject which behaves like a list
        customers_obj = stripe.Customer.list(**kwargs)
        # Convert each customer to a plain dict
        return [c.to_dict() for c in customers_obj]
    except stripe.error.StripeError as exc:
        # Re‑raise the exception so callers can handle it
        raise exc