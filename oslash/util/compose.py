from functools import reduce


def compose(*funcs: "Tuple[Callable,...") -> "Callable":
    """Compose multiple functions right to left.

    Composes zero or more functions into a functional composition. The
    functions are composed right to left. A composition of zero
    functions gives back the identity function.

    compose()(x) == x
    compose(f)(x) == f(x)
    compose(g, f)(x) == g(f(x))
    compose(h, g, f)(x) == h(g(f(x)))
    ...
    """

    def _(*args, **kw):
        ret = reduce(lambda acc, f: lambda g: g(acc(f)), funcs[::-1],
                     lambda f: f(*args, **kw))
        return ret(lambda x: x)
    return _

identity = compose()  # type: Callable
