import random
from datetime import datetime


# Simulates the Stripe US third-party SDK — cannot be modified
class StripeUS:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def charge(self, amount_usd: float, card_token: str) -> dict:
        print(f"[StripeUS] Charging ${amount_usd:.2f} USD with card token {card_token}")
        return {
            "charge_id": f"ch_us_{random.randint(100000, 999999)}",
            "paid": True,
            "amount_usd": amount_usd,
            "card_token": card_token,
            "timestamp": datetime.now().isoformat(),
        }

    def retrieve_charge(self, charge_id: str) -> dict:
        print(f"[StripeUS] Retrieving charge {charge_id}")
        return {
            "charge_id": charge_id,
            "paid": True,
            "status": "succeeded",
            "timestamp": datetime.now().isoformat(),
        }

    def issue_refund(self, charge_id: str, amount_usd: float) -> dict:
        print(f"[StripeUS] Issuing refund of ${amount_usd:.2f} USD for charge {charge_id}")
        return {
            "refund_id": f"re_us_{random.randint(100000, 999999)}",
            "charge_id": charge_id,
            "refunded": True,
            "amount_usd": amount_usd,
        }


# Simulates the Stripe EU third-party SDK — cannot be modified
class StripeEU:
    def __init__(self, merchant_id: str, secret: str):
        self.merchant_id = merchant_id
        self.secret = secret

    def initiate_transaction(self, amount_eur: float, iban: str, billing_country: str) -> dict:
        print(f"[StripeEU] Initiating transaction of €{amount_eur:.2f} EUR from IBAN {iban} ({billing_country})")
        return {
            "transaction_ref": f"txn_eu_{random.randint(100000, 999999)}",
            "authorised": True,
            "amount_eur": amount_eur,
            "iban": iban,
            "billing_country": billing_country,
            "timestamp": datetime.now().isoformat(),
        }

    def query_transaction(self, transaction_ref: str) -> dict:
        print(f"[StripeEU] Querying transaction {transaction_ref}")
        return {
            "transaction_ref": transaction_ref,
            "authorised": True,
            "state": "settled",
            "timestamp": datetime.now().isoformat(),
        }

    def reverse_transaction(self, transaction_ref: str, amount_eur: float) -> dict:
        print(f"[StripeEU] Reversing €{amount_eur:.2f} EUR for transaction {transaction_ref}")
        return {
            "reversal_ref": f"rev_eu_{random.randint(100000, 999999)}",
            "transaction_ref": transaction_ref,
            "reversed": True,
            "amount_eur": amount_eur,
        }
