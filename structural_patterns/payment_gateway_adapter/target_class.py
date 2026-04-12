from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass
    
    @abstractmethod
    def get_payment_status(self, payment_id: str) -> str:
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> bool:
        pass
    
    @abstractmethod
    def verify_payment(self, payment_id: str) -> bool:
        pass
    
    