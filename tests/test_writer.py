import unittest

from oslash import Writer


class TestWriterMonad(unittest.TestCase):
    def test_writer_return(self):
        w = Writer.return_(42)
        self.assertEqual(w.run_writer(), (42, ""))

    def test_writer_return_int_log(self):
        w = Writer.return_(42, int)
        self.assertEqual(w.run_writer(), (42, 0))

    def test_writer_monad_bind(self):
        entry = "Multiplied by 10"
        m = Writer.return_(42).bind(lambda x: Writer(x*10, entry))
        self.assertEqual(m, Writer(420, entry))

    def test_writer_monad_law_left_identity(self):
        # return x >>= f == f x
        entry = "Added 100000 to %s"
        a = Writer.return_(42).bind(lambda x: Writer(x+100000, entry % x))
        b = (lambda x: Writer(x+100000, entry % x))(42)
        self.assertEqual(a, b)

    def test_writer_monad_law_right_identity(self):
        # m >>= return is no different than just m.
        a = Writer.return_(42).bind(Writer.return_)
        self.assertEqual(a, Writer.return_(42))

    def test_writer_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        add1000 = "Added 1000 to %s"
        mul100 = "Multiplied %s by 100"
        a = Writer.return_(42).bind(lambda x: Writer(x+1000, add1000 % x)).bind(lambda y: Writer(y*100, mul100 % y))
        b = Writer.return_(42).bind(lambda x: Writer(x+1000, add1000 % x).bind(lambda y: Writer(y*100, mul100 % y)))
        self.assertEqual(a, b)
