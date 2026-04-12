from target_class import PaymentGateway
from adaptee import StripeUS, StripeEU

# Conversion rate — in a real app this would come from an FX service
USD_TO_EUR = 0.92


class StripeUSAdapter(PaymentGateway):
    """Adapts the StripeUS SDK to the PaymentGateway interface."""

    def __init__(self, card_token: str):
        self.stripe_us = StripeUS()
        self.card_token = card_token

    def process_payment(self, amount: float) -> bool:
        result = self.stripe_us.charge(amount, self.card_token)
        return result["paid"]

    def get_payment_status(self, payment_id: str) -> str:
        result = self.stripe_us.retrieve_charge(payment_id)
        return result["status"]

    def refund_payment(self, transaction_id: str, amount: float) -> bool:
        result = self.stripe_us.issue_refund(transaction_id, amount)
        return result["refunded"]

    def verify_payment(self, transaction_id: str) -> bool:
        result = self.stripe_us.retrieve_charge(transaction_id)
        return result["paid"]


class StripeEUAdapter(PaymentGateway):
    """
    Adapts the StripeEU SDK to the PaymentGateway interface.
    The EU SDK works in EUR and expects an IBAN + billing country,
    so this adapter converts USD → EUR and maps card_token to an IBAN.
    """

    def __init__(self, iban: str, billing_country: str):
        self.stripe_eu = StripeEU()
        self.iban = iban
        self.billing_country = billing_country

    def _to_eur(self, amount_usd: float) -> float:
        return round(amount_usd * USD_TO_EUR, 2)

    def process_payment(self, amount: float) -> bool:
        result = self.stripe_eu.initiate_transaction(
            self._to_eur(amount), self.iban, self.billing_country
        )
        return result["authorised"]

    def get_payment_status(self, payment_id: str) -> str:
        result = self.stripe_eu.query_transaction(payment_id)
        return result["state"]

    def refund_payment(self, transaction_id: str, amount: float) -> bool:
        result = self.stripe_eu.reverse_transaction(transaction_id, self._to_eur(amount))
        return result["reversed"]

    def verify_payment(self, transaction_id: str) -> bool:
        result = self.stripe_eu.query_transaction(transaction_id)
        return result["authorised"]
