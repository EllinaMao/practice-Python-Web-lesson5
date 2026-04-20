
from functools import wraps
from colorama import Fore



def try_catch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
    return wrapper

