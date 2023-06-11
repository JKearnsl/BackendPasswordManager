import binascii
import re
import ctypes
import base64


def is_valid_email(email: str) -> bool:
    pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$"

    if re.match(pattern, email) is not None:
        return True
    else:
        return False


def is_valid_username(username: str) -> bool:
    pattern = r"^(?=.{4,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
    if re.match(pattern, username) is not None:
        return True
    else:
        return False


def is_valid_password(password: str) -> bool:
    pattern = r"^[\w.#$%&_](?=.*\d)(?=.{16,32}$)"
    if re.match(pattern, password) is not None:
        return True
    else:
        return False


def is_int64(value: int) -> bool:
    df_dataframe = ctypes.c_int64(value).value
    if df_dataframe == value:
        return True


def is_base64(s: str) -> bool:
    try:
        decoded_bytes = base64.b64decode(s)
        return isinstance(decoded_bytes, bytes)
    except (TypeError, binascii.Error):
        return False
