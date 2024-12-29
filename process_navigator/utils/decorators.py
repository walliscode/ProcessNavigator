from functools import wraps

from flask import redirect, session, url_for

"""
This decorators that can be used to protect routes from undesired requests.
Mainly, when we need pre requiste information from the previous route such as picking which 
method to edit
"""


def session_keys(required_keys=None):
    def decorator_session_keys(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if required_keys is None:
                return func(*args, **kwargs)
            for key, redirect_location in required_keys.items():
                if key not in session["security_keys"]:
                    return redirect(url_for(redirect_location))

                return func(*args, **kwargs)

        return decorated_function

    return decorator_session_keys


"""
This decorator is a used to check whether the user is logged in or not, if not, it will redirect the user to the login page.
The absence of this decorator will allow the user to access the route without logging in.
"""


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login"))
        return func(*args, **kwargs)

    return decorated_function
