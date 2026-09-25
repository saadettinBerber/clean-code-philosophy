import unittest

from measure.class_checks import (MAX_CLASS_LINES, ClassSize, Cohesion, FieldsOutsideConstructor, Hybrid,
                                  Responsibilities, UnusedSelf)
from measure.findings import ALARM, LOOK
from tests.snippets import Snippet, levels

SUPER_DASHBOARD = """
class SuperDashboard:
    def __init__(self):
        self._last_focused = None
        self._major = 1
        self._minor = 0

    def last_focused_component(self):
        return self._last_focused

    def focus(self, component):
        self._last_focused = component

    def version(self):
        return f"{self._major}.{self._minor}"
"""

COHESIVE_STACK = """
class Stack:
    def __init__(self):
        self._items = []
        self._top = 0

    def push(self, item):
        self._items.append(item)
        self._top += 1

    def pop(self):
        self._top -= 1
        return self._items.pop()
"""

MUTUAL_CALLS = """
class Report:
    def __init__(self):
        self._rows = []
        self._title = ""

    def render(self):
        return self._heading() + str(self._rows)

    def _heading(self):
        return self._title
"""

FIELD_BORN_IN_METHOD = """
class Parser:
    def __init__(self):
        self._text = ""

    def parse(self):
        self._tokens = self._text.split()
"""

PUBLIC_FIELD_WITH_BEHAVIOR = """
class Chapter:
    def __init__(self, pages):
        self.pages = pages

    def render(self):
        return "".join(page.render() for page in self.pages)
"""

PUBLIC_ACCESSOR_WITH_BEHAVIOR = """
class Chapter:
    def __init__(self, pages):
        self._pages = pages

    def pages(self):
        return self._pages

    def render(self):
        return "".join(page.render() for page in self._pages)
"""

FIELD_BUILT_IN_SET_UP = """
class ChapterTest:
    def setUp(self):
        self._chapter = Chapter()

    def test_title(self):
        return self._chapter.title()
"""

PUBLIC_FIXTURE_TEST_CASE = """
class ChapterTest:
    def setUp(self):
        self.chapter = Chapter()

    def test_title(self):
        self.assertEqual(self.chapter.title(), "Başlık")
"""

POINT = "class Point:\n    x: int\n    y: int\n"

METHOD_IGNORING_SELF = """
class Tax:
    def rate(self, amount):
        return amount / 100
"""

STATIC_METHOD = """
class Tax:
    @staticmethod
    def rate(amount):
        return amount / 100
"""


def class_with_lines(count):
    body = "\n".join(f"    X{index} = {index}" for index in range(count - 1))
    return Snippet(f"class Big:\n{body}\n").cls()


class ClassSizeTest(unittest.TestCase):
    def test_class_at_the_alarm_line_gives_no_note(self):
        self.assertEqual(ClassSize(class_with_lines(MAX_CLASS_LINES)).findings(), [])

    def test_one_line_over_raises_the_alarm(self):
        self.assertEqual(levels(ClassSize(class_with_lines(MAX_CLASS_LINES + 1)).findings()), [ALARM])


class ResponsibilitiesTest(unittest.TestCase):
    def test_small_class_with_two_jobs_is_caught(self):
        self.assertEqual(levels(Responsibilities(Snippet(SUPER_DASHBOARD).cls()).findings()), [ALARM])

    def test_methods_sharing_fields_form_one_responsibility(self):
        self.assertEqual(Responsibilities(Snippet(COHESIVE_STACK).cls()).findings(), [])

    def test_methods_calling_each_other_form_one_responsibility(self):
        self.assertEqual(Responsibilities(Snippet(MUTUAL_CALLS).cls()).findings(), [])


class CohesionTest(unittest.TestCase):
    def test_field_used_by_one_method_is_worth_a_look(self):
        self.assertEqual(levels(Cohesion(Snippet(SUPER_DASHBOARD).cls()).findings()), [LOOK, LOOK])

    def test_fields_shared_by_methods_are_cohesive(self):
        self.assertEqual(Cohesion(Snippet(COHESIVE_STACK).cls()).findings(), [])

    def test_data_structure_without_methods_is_not_measured(self):
        self.assertEqual(Cohesion(Snippet(POINT).cls()).findings(), [])


class FieldsOutsideConstructorTest(unittest.TestCase):
    def test_field_born_in_a_method_raises_an_alarm(self):
        self.assertEqual(levels(FieldsOutsideConstructor(Snippet(FIELD_BORN_IN_METHOD).cls()).findings()), [ALARM])

    def test_fields_declared_in_the_constructor_are_fine(self):
        self.assertEqual(FieldsOutsideConstructor(Snippet(COHESIVE_STACK).cls()).findings(), [])

    def test_fields_built_in_set_up_are_fine(self):
        self.assertEqual(FieldsOutsideConstructor(Snippet(FIELD_BUILT_IN_SET_UP).cls()).findings(), [])


class HybridTest(unittest.TestCase):
    def test_public_field_beside_behavior_is_a_hybrid(self):
        self.assertEqual(levels(Hybrid(Snippet(PUBLIC_FIELD_WITH_BEHAVIOR).cls()).findings()), [ALARM])

    def test_public_accessor_beside_behavior_is_a_hybrid(self):
        self.assertEqual(levels(Hybrid(Snippet(PUBLIC_ACCESSOR_WITH_BEHAVIOR).cls()).findings()), [ALARM])

    def test_object_hiding_its_data_is_not_a_hybrid(self):
        self.assertEqual(Hybrid(Snippet(COHESIVE_STACK).cls()).findings(), [])

    def test_data_structure_is_not_a_hybrid(self):
        self.assertEqual(Hybrid(Snippet(POINT).cls()).findings(), [])

    def test_test_case_is_not_a_hybrid(self):
        self.assertEqual(Hybrid(Snippet(PUBLIC_FIXTURE_TEST_CASE).cls()).findings(), [])


class UnusedSelfTest(unittest.TestCase):
    def test_method_ignoring_self_is_worth_a_look(self):
        self.assertEqual(levels(UnusedSelf(Snippet(METHOD_IGNORING_SELF).cls()).findings()), [LOOK])

    def test_static_method_is_not_measured(self):
        self.assertEqual(UnusedSelf(Snippet(STATIC_METHOD).cls()).findings(), [])


if __name__ == "__main__":
    unittest.main()
