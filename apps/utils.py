from random import randint

from django.core.cache import cache
from redis import Redis
from root import settings


def random_code():
    return randint(100_000, 999_999)  #


def _get_login_key(phone):
    return f"login:{phone}"


def send_sms_code(phone: str, code: int, expire_time=60):
    redis = Redis.from_url(settings.CACHES['default']['LOCATION'])
    _key = _get_login_key(phone)
    _ttl = redis.ttl(f':1:{_key}')
    if _ttl > 0:
        return False, _ttl
    print(f"[TEST] Phone: {phone} == Sms code: {code}")
    cache.set(_key, code, expire_time)
    return True, 0


# if data['type'] == 'email':
#     print('email sending')
#     send_email(data['value'],code)
# else:
#     print(f'{data['type']}: {data['value']} == Code: {code}')
#
# _data = {
#     'code':code,
#     'type':data['type'],
#     'first_name':data['first_name'],
#     'last_name':data['last_name'],
#     'password':data['password']
# }
# cache.set(_contact, _data, expired_time)
# return True, 0


def check_sms_code(phone, code):
    _key = _get_login_key(phone)
    _code = cache.get(_key)
    print(_code, code)
    return _code == code
