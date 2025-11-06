from random import randint

from django.core.cache import cache


def random_code():
    return randint(100_000, 999_999)  #


def _get_login_key(phone):
    return f"login:{phone}"


def send_sms_code(phone: str, expire_time=60):
    _key = _get_login_key(phone)

    cached = cache.get(_key)
    if cached:
        try:
            remaining = cache.client.get_client().ttl(_key)
        except Exception:
            remaining = expire_time
        return {"success": False, "remaining": remaining}

    code = random_code()
    print(f"[TEST] Phone: {phone} == Sms code: {code}")
    cache.set(_key, code, expire_time)
    return {"success": True, "remaining": expire_time}


def check_sms_code(phone, code):
    _key = _get_login_key(phone)
    _code = cache.get(_key)
    print(_code, code)
    return _code == code
