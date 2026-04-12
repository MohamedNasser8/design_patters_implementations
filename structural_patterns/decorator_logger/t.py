import functools

def handle_exceptions(default_return=None, log_errors=True):
    """
    Catches exceptions and returns default value
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    print(f"❌ Exception in {func.__name__}: {type(e).__name__}: {e}")
                return default_return
        
        return wrapper
    
    return decorator

# Usage
@handle_exceptions(default_return={'error': 'failed'})
def risky_operation():
    raise Exception("Something went wrong!")
    return {"result": "success"}

result = risky_operation()
print(result)  # {'error': 'failed'}