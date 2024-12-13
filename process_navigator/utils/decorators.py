from functools import wraps

from flask import redirect, session, url_for


def session_keys(required_keys=None):
    def decorator_session_keys(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if required_keys is None:
                return func(*args, **kwargs)
            for key, redirect_location in required_keys.items():
                if (
                    "security_keys" not in session
                    or key not in session["security_keys"]
                ):
                    return redirect(url_for(redirect_location))
                return func(*args, **kwargs)

        return decorated_function

    return decorator_session_keys
