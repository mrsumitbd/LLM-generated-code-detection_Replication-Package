import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe
import stripe

def stripe_get_customers(api_key: str, **kwargs):
        import stripe
        stripe.api_key = api_key
        return stripe.Customer.list(**kwargs)