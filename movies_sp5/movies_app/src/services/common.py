def make_redis_key(entity: str, *args):
    return f'{entity}__' + '__'.join((str(arg) for arg in args))
