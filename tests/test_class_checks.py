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

INJECTED_COLLABORATOR = """
class Portfolio:
    def __init__(self, exchange):
        self._exchange = exchange

    def set_exchange(self, exchange):
        self._exchange = exchange

    def value_of(self, symbol):
        return self._exchange.current_price(symbol)
"""

EXPOSED_COLLABORATOR = """
class Portfolio:
    def __init__(self, exchange):
        self._exchange = exchange

    def set_exchange(self, exchange):
        self._exchange = exchange

    def exchange(self):
        return self._exchange

    def value_of(self, symbol):
        return self._exchange.current_price(symbol)
"""

SETTER_OF_MUTATED_DATA = """
class Playlist:
    def __init__(self):
        self._songs = []

    def set_songs(self, songs):
        self._songs = songs

    def enqueue(self, song):
        self._songs.append(song)
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


    def test_visitor_handing_itself_out_is_one_responsibility(self):
        self.assertEqual(Responsibilities(Snippet(VISITOR).cls()).findings(), [])

    def test_visitor_handing_itself_out_by_keyword_is_one_responsibility(self):
        self.assertEqual(Responsibilities(Snippet(VISITOR.replace("accept(self)", "accept(visitor=self)")).cls()).findings(), [])

    def test_handing_out_a_field_does_not_join_the_callbacks(self):
        self.assertEqual(levels(Responsibilities(Snippet(FIELD_HANDED_OUT).cls()).findings()), [ALARM])

    def test_tear_down_belongs_to_the_fixture(self):
        self.assertEqual(Responsibilities(Snippet(TEST_WITH_TEAR_DOWN).cls()).findings(), [])

    def test_ordinary_cleanup_method_is_a_responsibility_of_its_own(self):
        self.assertEqual(levels(Responsibilities(Snippet(CLEANUP_BESIDE_WORK).cls()).findings()), [ALARM])

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

SHARED_FIXTURE_BASE = """
class _BookTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = make_dir()

    def tearDown(self):
        self.tmp.cleanup()
"""

FIXTURE_LOOKALIKE = """
class BookTestCase:
    def __init__(self):
        self.tmp = make_dir()

    def cleanup(self):
        self.tmp.cleanup()
"""

FIELDS_ASSIGNED_TOGETHER = """
class Chapter:
    def __init__(self, title, pages):
        self.title, (self.first, *self.rest) = title, pages

    def render(self):
        return self.title.upper() + render(self.first)
"""

TEST_WITH_TEAR_DOWN = """
class PageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = make_dir()
        self.page = Page(self.tmp)

    def tearDown(self):
        self.tmp.cleanup()

    def test_title(self):
        self.assertEqual(self.page.title(), "Başlık")
"""

CLEANUP_BESIDE_WORK = """
class Page:
    def __init__(self, tmp, title):
        self.tmp, self.title = tmp, title

    def cleanup(self):
        self.tmp.cleanup()

    def heading(self):
        return self.title.upper()
"""

VISITOR = """
class Renderer:
    def __init__(self, document, style):
        self._document, self._style = document, style

    def fragments(self):
        return [block.accept(self) for block in self._document.blocks()]

    def visit_para(self, block):
        return self._style.para(block)

    def visit_code(self, block):
        return self._style.code(block)
"""

FIELD_HANDED_OUT = """
class Renderer:
    def __init__(self, document, style):
        self._document, self._style = document, style

    def fragments(self):
        return [block.accept(self._document) for block in self._document.blocks()]

    def visit_para(self, block):
        return self._style.para(block)
"""

DATA_WITH_NAMED_CONSTRUCTOR = """
class Metadata:
    def __init__(self, title, author):
        self.title, self.author = title, author

    @classmethod
    def for_book(cls, book):
        return cls(book["title"].strip(), book["author"])
"""

DATA_WITH_STATIC_FACTORY = """
class Header:
    def __init__(self, prefix):
        self.prefix = prefix

    @staticmethod
    def of(settings):
        return TopHeader(settings) if settings.get("top") else Header(settings.get("prefix"))
"""

DATA_WITH_CLASS_QUERY = """
class Metadata:
    def __init__(self, title):
        self.title = title

    @classmethod
    def label(cls, book):
        return book["title"].strip().upper()
"""


class HybridTest(unittest.TestCase):
    def test_public_field_beside_behavior_is_a_hybrid(self):
        self.assertEqual(levels(Hybrid(Snippet(PUBLIC_FIELD_WITH_BEHAVIOR).cls()).findings()), [ALARM])

    def test_fields_assigned_together_are_public_state(self):
        findings = Hybrid(Snippet(FIELDS_ASSIGNED_TOGETHER).cls()).findings()
        self.assertIn("['first', 'rest', 'title']", findings[0].message)

    def test_public_accessor_beside_behavior_is_a_hybrid(self):
        self.assertEqual(levels(Hybrid(Snippet(PUBLIC_ACCESSOR_WITH_BEHAVIOR).cls()).findings()), [ALARM])

    def test_object_hiding_its_data_is_not_a_hybrid(self):
        self.assertEqual(Hybrid(Snippet(COHESIVE_STACK).cls()).findings(), [])

    def test_data_structure_is_not_a_hybrid(self):
        self.assertEqual(Hybrid(Snippet(POINT).cls()).findings(), [])

    def test_shared_fixture_base_is_a_test_case(self):
        self.assertEqual(Hybrid(Snippet(SHARED_FIXTURE_BASE).cls()).findings(), [])

    def test_class_named_like_a_test_case_but_not_derived_is_measured(self):
        self.assertEqual(levels(Hybrid(Snippet(FIXTURE_LOOKALIKE).cls()).findings()), [ALARM])

    def test_named_constructor_is_not_behavior(self):
        self.assertEqual(Hybrid(Snippet(DATA_WITH_NAMED_CONSTRUCTOR).cls()).findings(), [])

    def test_static_factory_choosing_a_subclass_is_not_behavior(self):
        self.assertEqual(Hybrid(Snippet(DATA_WITH_STATIC_FACTORY).cls()).findings(), [])

    def test_class_method_computing_an_answer_is_behavior(self):
        self.assertEqual(levels(Hybrid(Snippet(DATA_WITH_CLASS_QUERY).cls()).findings()), [ALARM])

    def test_test_case_is_not_a_hybrid(self):
        self.assertEqual(Hybrid(Snippet(PUBLIC_FIXTURE_TEST_CASE).cls()).findings(), [])

    def test_setter_injecting_a_collaborator_is_not_public_state(self):
        self.assertEqual(Hybrid(Snippet(INJECTED_COLLABORATOR).cls()).findings(), [])

    def test_injected_collaborator_handed_out_by_a_getter_is_public_state(self):
        self.assertEqual(levels(Hybrid(Snippet(EXPOSED_COLLABORATOR).cls()).findings()), [ALARM])

    def test_setter_of_data_mutated_in_place_is_public_state(self):
        self.assertEqual(levels(Hybrid(Snippet(SETTER_OF_MUTATED_DATA).cls()).findings()), [ALARM])


class UnusedSelfTest(unittest.TestCase):
    def test_method_ignoring_self_is_worth_a_look(self):
        self.assertEqual(levels(UnusedSelf(Snippet(METHOD_IGNORING_SELF).cls()).findings()), [LOOK])

    def test_static_method_is_not_measured(self):
        self.assertEqual(UnusedSelf(Snippet(STATIC_METHOD).cls()).findings(), [])


if __name__ == "__main__":
    unittest.main()
