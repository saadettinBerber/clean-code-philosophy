import unittest

from measure.switch_check import OneSwitch, Switches
from tests.snippets import Snippet, names

RENDER_BY_TYPE = """
def render(block):
    if block["type"] == "para":
        return para(block)
    elif block["type"] == "code":
        return code(block)
"""

COUNT_BY_TYPE = """
def count(block):
    if block["type"] == "para":
        return len(block["sentences"])
    elif block["type"] == "code":
        return 1
"""

SINGLE_COMPARISON = """
def f(b):
    if b.kind == 'listing':
        go()
"""

MATCH_ON_FIELD = """
def f(block):
    match block.kind:
        case "para":
            go()
"""

ISINSTANCE_BRANCHES = """
def f(shape):
    if isinstance(shape, Square):
        return 1
    elif isinstance(shape, Circle):
        return 2
"""


class FieldSwitchesTest(unittest.TestCase):
    def test_two_comparisons_on_one_key_are_a_switch(self):
        self.assertEqual(Switches(Snippet(RENDER_BY_TYPE).function()).fields(), ["type"])

    def test_single_comparison_is_not_a_switch(self):
        self.assertEqual(Switches(Snippet(SINGLE_COMPARISON).function()).fields(), [])

    def test_match_on_a_field_is_a_switch(self):
        self.assertEqual(Switches(Snippet(MATCH_ON_FIELD).function()).fields(), ["kind"])


class TypeSwitchTest(unittest.TestCase):
    def test_isinstance_branches_are_a_switch(self):
        self.assertEqual(Switches(Snippet(ISINSTANCE_BRANCHES).function()).types(), {"Square", "Circle"})

    def test_single_isinstance_predicate_is_not_a_switch(self):
        self.assertEqual(Switches(Snippet("def f(x):\n    return isinstance(x, (A, B))\n").function()).types(), frozenset())


class OneSwitchTest(unittest.TestCase):
    def test_same_switch_in_two_functions_raises_alarms(self):
        self.assertEqual(names(OneSwitch(Snippet(RENDER_BY_TYPE + COUNT_BY_TYPE).functions()).notes()), ["render", "count"])

    def test_switch_in_one_function_is_the_one_switch(self):
        self.assertEqual(OneSwitch(Snippet(RENDER_BY_TYPE).functions()).notes(), [])


if __name__ == "__main__":
    unittest.main()
