from slowapi import Limiter
from slowapi.util import get_remote_address

# Shared Limiter instance. Lives in its own module (rather than main.py)
# so route modules can import it without a main.py <-> routes circular import.
limiter = Limiter(key_func=get_remote_address)
