import functools

def validate_types(*expected_arg_types):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            for i,arg in enumerate(args):
                if not isinstance(arg,expected_arg_types[i]):
                    raise TypeError(f"Argument{i + 1} must be type {expected_arg_types[i].__name__},"
                    f"not {type(arg).__name__}")
            return func(*args,**kwargs)
        return wrapper
    return decorator

@validate_types(str,str,int)
def create_user_account(username,email,age):
    """Create a new user account."""
    return f"Account created for {username} {email}, age:{age}"

#This will work
print(create_user_account('testuser','test@example.com',30))

#This will raise a TypeError
try:
    print(create_user_account('testuser','test@example.com','30'))
except TypeError as e:
    print(f"Error: {e}")
