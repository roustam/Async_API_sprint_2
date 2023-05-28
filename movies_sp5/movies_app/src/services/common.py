CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


def make_redis_key(entity: str, *args):
    return f'{entity}__' + '__'.join((str(arg) for arg in args))
