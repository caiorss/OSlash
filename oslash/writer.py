from .functor import Functor
from .monad import Monad
from .monoid import Monoid


class Writer(Monad, Functor):

    """The writer monad."""

    def __init__(self, value: "Any", log: Monoid):
        """Initialize a new writer.

        :param value Any: Value to
        """
        super().__init__()

        self._get_value = lambda: (value, log)

    def fmap(self, func: "Callable[[Any], Any]") -> "Writer":
        """Map a function func over the Writer value.

        Haskell:
        fmap f m = Writer $ let (a, w) = runWriter m in (f a, w)

        Keyword arguments:
        :param Callable[[Any], Any] func:
        """
        value, log = self.run_writer()
        return Writer(func(value), log)

    def bind(self, func: "Callable[[Any], Writer]") -> "Writer":
        """Flat is better than nested.

        Haskell:
        (Writer (x, v)) >>= f = let
            (Writer (y, v')) = f x in Writer (y, v `mappend` v')

        Keyword Arguments:
        :param func Callable[[Any], Writer[Any, Monoid]]
        :return: New Writer
        :rtype: Writer
        """
        a, w = self.run_writer()
        b, w_ = func(a).run_writer()
        return Writer(b, w + w_)

    def __eq__(self, other: "Writer") -> bool:
        return self.run_writer() == other.run_writer()

    def __str__(self) -> str:
        return "%s :: %s" % self.run_writer()

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def return_(cls, value: "Any", monoid: Monoid=str) -> "Writer":
        # Get default value for empty log monoid
        log = monoid.mempty() if hasattr(monoid, "mempty") else monoid()
        return cls(value, log)

    def run_writer(self) -> tuple:
        """Convert Writer to s simple tuple."""
        return self._get_value()

    @staticmethod
    def apply_log(a: tuple, func: "Callabe[[Any], Tuple[Any, Monoid]]") -> tuple:
        """Apply a function to a value with a log.

        Helper function to apply a function to a value with a log tuple.
        """
        value, log = a
        new, entry = func(value)
        return new, log + entry
