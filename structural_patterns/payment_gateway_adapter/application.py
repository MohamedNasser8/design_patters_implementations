from adapter import StripeEUAdapter

def application():
    print("Application started")
    stripe_payment_adapter = StripeEUAdapter("1234567890", "Germany")
    
    stripe_payment_adapter.process_payment(100)
    stripe_payment_adapter.get_payment_status("1234567890")
    stripe_payment_adapter.refund_payment("1234567890", 100)
    stripe_payment_adapter.verify_payment("1234567890")
    
    print(stripe_payment_adapter.get_payment_status("1234567890"))
    print(stripe_payment_adapter.refund_payment("1234567890", 100))
    print(stripe_payment_adapter.verify_payment("1234567890"))
    
    