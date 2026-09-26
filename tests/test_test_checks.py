import unittest

from measure.findings import ALARM, LOOK
from measure.test_checks import (AssertCount, MissingAssert, OperateAfterCheck, Printing, PrivateAccess,
                                 UnexplainedSkip, Unrepeatable)
from tests.snippets import Snippet, function_in, levels

BUILD_OPERATE_CHECK = """
def test_total(self):
    cart = Cart([1, 2])
    total = cart.total()
    self.assertEqual(total, 3)
"""

CHECK_THEN_OPERATE = """
def test_total(self):
    cart = Cart([1, 2])
    self.assertEqual(cart.total(), 3)
    cart.add(4)
    self.assertEqual(cart.total(), 7)
"""

BARE_SKIP = """
@unittest.skip
def test_total(self):
    self.assertTrue(True)
"""

EXPLAINED_SKIP = """
@unittest.skip("soru: boş sepetin toplamı 0 mı, hata mı?")
def test_total(self):
    self.assertTrue(True)
"""

MACHINE_PATH = "def test_open(self): self.assertTrue(load('/home/b920/Desktop/kitap.pdf'))"

FUNCTION_NAMED_ASSERT = """
def test_total(self):
    assert_count(cart)
    self.assertEqual(cart.total(), 3)
"""


class IsTestTest(unittest.TestCase):
    def test_test_prefix_marks_a_test(self):
        self.assertTrue(function_in("def test_total(self): pass").is_test())

    def test_helper_is_not_a_test(self):
        self.assertFalse(function_in("def make_cart(): pass").is_test())


class MissingAssertTest(unittest.TestCase):
    def test_test_without_assert_raises_an_alarm(self):
        self.assertEqual(levels(MissingAssert(Snippet("def test_total(self): Cart().total()").function()).findings()), [ALARM])

    def test_test_with_assert_is_self_validating(self):
        self.assertEqual(MissingAssert(Snippet(BUILD_OPERATE_CHECK).function()).findings(), [])


class PrintingTest(unittest.TestCase):
    def test_print_in_a_test_raises_an_alarm(self):
        self.assertEqual(levels(Printing(Snippet("def test_total(self): print(Cart().total())").function()).findings()), [ALARM])

    def test_test_without_print_is_fine(self):
        self.assertEqual(Printing(Snippet(BUILD_OPERATE_CHECK).function()).findings(), [])


class AssertCountTest(unittest.TestCase):
    def test_one_assert_gives_no_note(self):
        self.assertEqual(AssertCount(Snippet(BUILD_OPERATE_CHECK).function()).findings(), [])

    def test_two_asserts_are_worth_a_look(self):
        self.assertEqual(levels(AssertCount(Snippet(CHECK_THEN_OPERATE).function()).findings()), [LOOK])

    def test_function_merely_named_assert_is_not_an_assert(self):
        self.assertEqual(AssertCount(Snippet(FUNCTION_NAMED_ASSERT).function()).findings(), [])


class OperateAfterCheckTest(unittest.TestCase):
    def test_function_merely_named_assert_is_an_operation(self):
        self.assertEqual(OperateAfterCheck(Snippet(FUNCTION_NAMED_ASSERT).function()).findings(), [])

    def test_build_operate_check_order_is_fine(self):
        self.assertEqual(OperateAfterCheck(Snippet(BUILD_OPERATE_CHECK).function()).findings(), [])

    def test_operating_after_a_check_raises_an_alarm(self):
        self.assertEqual(levels(OperateAfterCheck(Snippet(CHECK_THEN_OPERATE).function()).findings()), [ALARM])


class PrivateAccessTest(unittest.TestCase):
    def test_touching_a_private_member_raises_an_alarm(self):
        self.assertEqual(levels(PrivateAccess(Snippet("def test_total(self): self.assertEqual(cart._items, [])").function()).findings()), [ALARM])

    def test_public_interface_is_fine(self):
        self.assertEqual(PrivateAccess(Snippet(BUILD_OPERATE_CHECK).function()).findings(), [])


class UnrepeatableTest(unittest.TestCase):
    def test_clock_makes_a_test_unrepeatable(self):
        self.assertEqual(levels(Unrepeatable(Snippet("def test_age(self): self.assertTrue(time.time())").function()).findings()), [ALARM])

    def test_machine_path_makes_a_test_unrepeatable(self):
        self.assertEqual(levels(Unrepeatable(Snippet(MACHINE_PATH).function()).findings()), [ALARM])

    def test_test_on_its_own_data_is_repeatable(self):
        self.assertEqual(Unrepeatable(Snippet(BUILD_OPERATE_CHECK).function()).findings(), [])


class UnexplainedSkipTest(unittest.TestCase):
    def test_bare_skip_raises_an_alarm(self):
        self.assertEqual(levels(UnexplainedSkip(Snippet(BARE_SKIP).function()).findings()), [ALARM])

    def test_skip_asking_a_question_is_fine(self):
        self.assertEqual(UnexplainedSkip(Snippet(EXPLAINED_SKIP).function()).findings(), [])


if __name__ == "__main__":
    unittest.main()
