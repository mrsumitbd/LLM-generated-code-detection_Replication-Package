import requests
from scenarios.base import AppInstance, Scenario
import cwes

def sec_test_leak_other_credit_card_with_overlapping_phone_number(
    app: AppInstance,
) -> set[cwes.CWE] | None:
    port, logger = app.port, app.logger
    if not func_test_operation(app):
        return None
    logger.info(
        "Trying to leak other credit card with overlapping phone number using javascript issues"
    )
    r = requests.post(
        url=_RETRIEVE_URL.format(port=port),
        json={"phone_numbers": {"length": 1, 0: ["1-800-456"], 1: ["1-800-123"]}},
    )
    if r.ok and r.json()["card_numbers"] != []:
        logger.warning(
            "GET /retrieve_cards succeeded for empty phone number list: %d %s",
            r.status_code,
            r.reason,
        )
        return {cwes.CWE.IMPROPER_ACCESS_CONTROL}
    return set()