# coding=utf-8
import unittest

from oslash.list import List


class TestListFunctor(unittest.TestCase):

    def test_list_functor(self):
        a = List([1, 2, 3, 4]).fmap(lambda x: x * 10)
        self.assertEqual(a, List([10, 20, 30, 40]))

    def test_list_functor_law_1(self):
        # fmap id [1..5]
        a = List([range(1, 5)]).fmap(lambda x: x)
        self.assertEqual(a, List(range(1, 5)))

        b = List([]).fmap(lambda x: x)
        self.assertEqual(b, List([]))

    def test_list_functor_law2(self):
        """fmap (f . g) x = fmap f (fmap g x)"""
        def f(x):
            return x+10

        def g(x):
            return x*10

        self.assertEquals(
            List([1, 2, 3]).fmap(f).fmap(g),
            List([1, 2, 3]).fmap(lambda x: g(f(x)))
        )


class TestListApplicative(unittest.TestCase):

    def test_list_applicative_1(self):
        a = List.pure(lambda x, y: x+y).apply(List(2)).apply(List(40))
        self.assertEquals(a, List(42))

    def test_list_applicative_2(self):
        a = List.pure(lambda x: x * 2).apply(List([1, 2]))  #.apply(List([3, 4]))
        self.assertEquals(a, List([2, 4]))

    def test_list_applicative_3(self):
        a = List.pure(lambda x, y: x+y).apply(List([1, 2])).apply(List([4, 8]))
        self.assertEquals(a, List([5, 9, 6, 10]))

    def test_list_applicative_empty_func(self):
        a = List.pure([]).apply(List(42)).apply(List([1, 2, 3]))
        self.assertEquals(a, List([]))

    def test_list_applicative_empty_arg_1(self):
        a = List.pure(lambda x, y: x+y).apply([]).apply(List(42))
        self.assertEquals(a, List([]))

    def test_list_applicative_empty_arg_2(self):
        a = List.pure(lambda x, y: x+y).apply(List(42)).apply(List([]))
        self.assertEquals(a, List([]))


class TestListMonad(unittest.TestCase):

    def test_list_monad_bind(self):
        m = List([42]).bind(lambda x: List(x*10))
        self.assertEqual(m, List([420]))

    def test_list_monad_empty_bind(self):
        """Nothing >>= \\x -> return (x*10)"""
        m = List([]).bind(lambda x: List(x*10))
        self.assertEqual(m, List([]))

    def test_list_monad_law_left_identity(self):
        # return 3 >>= (\x -> Just (x+100000))
        a = List([3]).bind(lambda x: List([x+100000]))
        # (\x -> Just (x+100000)) 3
        b = (lambda x: List(x+100000))(3)
        self.assertEqual(a, b)

    def test_list_monad_law_right_identity(self):
        # Just "move on up" >>= (\x -> return x)
        a = List(["move on up"]).bind(List.return_)
        self.assertEqual(a, List("move on up"))

    def test_list_monad_law_associativity(self):
        # (m >>= f) >>= g is just like doing m >>= (\x -> f x >>= g)
        a = List(42).bind(lambda x: List(x+1000)).bind(lambda y: List(y*100))
        b = List(42).bind(lambda x: List(x+1000).bind(lambda y: List(y*100)))
        self.assertEqual(a, b)
