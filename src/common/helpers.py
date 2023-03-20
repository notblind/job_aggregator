def convert(num, fun, default=None):
    try:
        res = fun(num)
    except ValueError:
        return default
    return res
