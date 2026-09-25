import unittest

from measure.findings import ALARM, LOOK
from measure.function_checks import (IDEAL_BODY_LINES, MAX_BODY_LINES, ArgumentCount, CommandQuery, FlagArguments,
                                     FunctionSize, MagicNumbers, NestingDepth, OutputArguments, ReturnsNone,
                                     SwallowedExceptions, TrainWrecks)
from tests.snippets import Snippet, function_with_body_lines, levels

DOCUMENTED_IDEAL = 'def f():\n    """Belge."""\n' + "\n".join(f"    x{i} = {i}" for i in range(IDEAL_BODY_LINES))

TWO_LEVELS = """
def f(items):
    for item in items:
        if item:
            go(item)
"""

THREE_LEVELS = """
def f(items):
    for item in items:
        if item:
            while item:
                go(item)
"""

DEEP_ONLY_INSIDE_NESTED_FUNCTION = """
def f(items):
    for item in items:
        def inner():
            if item:
                while item:
                    go(item)
"""

COMMAND_THAT_ANSWERS = """
def set_name(self, name):
    self.name = name
    return True
"""

SWALLOWING = """
def f():
    try:
        go()
    except ValueError:
        pass
"""

TRANSLATING = """
def f():
    try:
        go()
    except ValueError as error:
        raise Failure() from error
"""


class FunctionSizeTest(unittest.TestCase):
    def test_ideal_body_gives_no_note(self):
        self.assertEqual(FunctionSize(function_with_body_lines(IDEAL_BODY_LINES)).findings(), [])

    def test_one_line_over_the_ideal_is_worth_a_look(self):
        self.assertEqual(levels(FunctionSize(function_with_body_lines(IDEAL_BODY_LINES + 1)).findings()), [LOOK])

    def test_body_at_the_ceiling_is_still_only_a_look(self):
        self.assertEqual(levels(FunctionSize(function_with_body_lines(MAX_BODY_LINES)).findings()), [LOOK])

    def test_one_line_over_the_ceiling_raises_an_alarm(self):
        self.assertEqual(levels(FunctionSize(function_with_body_lines(MAX_BODY_LINES + 1)).findings()), [ALARM])

    def test_docstring_is_not_counted(self):
        self.assertEqual(FunctionSize(Snippet(DOCUMENTED_IDEAL).function()).findings(), [])


class NestingDepthTest(unittest.TestCase):
    def test_two_levels_are_allowed(self):
        self.assertEqual(NestingDepth(Snippet(TWO_LEVELS).function()).findings(), [])

    def test_three_levels_raise_an_alarm(self):
        self.assertEqual(levels(NestingDepth(Snippet(THREE_LEVELS).function()).findings()), [ALARM])

    def test_nested_function_is_measured_on_its_own(self):
        self.assertEqual(NestingDepth(Snippet(DEEP_ONLY_INSIDE_NESTED_FUNCTION).function()).findings(), [])


class ArgumentCountTest(unittest.TestCase):
    def test_two_arguments_are_acceptable(self):
        self.assertEqual(ArgumentCount(Snippet("def f(a, b): pass").function()).findings(), [])

    def test_three_arguments_are_triadic(self):
        self.assertIn("triadic", ArgumentCount(Snippet("def f(a, b, c): pass").function()).findings()[0].message)

    def test_four_arguments_are_polyadic(self):
        self.assertIn("polyadic", ArgumentCount(Snippet("def f(a, b, c, d): pass").function()).findings()[0].message)

    def test_self_is_not_counted(self):
        self.assertEqual(ArgumentCount(Snippet("def f(self, a, b): pass").function()).findings(), [])

    def test_packed_arguments_count_once_each(self):
        self.assertIn("triadic", ArgumentCount(Snippet("def f(a, *rest, **options): pass").function()).findings()[0].message)


class FlagArgumentsTest(unittest.TestCase):
    def test_bool_default_is_a_flag(self):
        self.assertEqual(levels(FlagArguments(Snippet("def f(a, verbose=False): pass").function()).findings()), [ALARM])

    def test_bool_annotation_is_a_flag(self):
        self.assertEqual(levels(FlagArguments(Snippet("def f(suite: bool): pass").function()).findings()), [ALARM])

    def test_keyword_only_bool_default_is_a_flag(self):
        self.assertEqual(levels(FlagArguments(Snippet("def f(*, strict=True): pass").function()).findings()), [ALARM])

    def test_other_defaults_are_not_flags(self):
        self.assertEqual(FlagArguments(Snippet("def f(a, limit=3): pass").function()).findings(), [])


class OutputArgumentsTest(unittest.TestCase):
    def test_appending_to_an_argument_is_an_output_argument(self):
        self.assertEqual(levels(OutputArguments(Snippet("def f(report): report.append(1)").function()).findings()), [ALARM])

    def test_assigning_into_an_argument_is_an_output_argument(self):
        self.assertEqual(levels(OutputArguments(Snippet("def f(page): page['title'] = 1").function()).findings()), [ALARM])

    def test_rebinding_the_name_is_not_an_output_argument(self):
        self.assertEqual(OutputArguments(Snippet("def f(page): page = 1").function()).findings(), [])

    def test_changing_own_state_is_not_an_output_argument(self):
        self.assertEqual(OutputArguments(Snippet("def f(self, x): self.items.append(x)").function()).findings(), [])


class CommandQueryTest(unittest.TestCase):
    def test_command_that_also_answers_raises_an_alarm(self):
        self.assertEqual(levels(CommandQuery(Snippet(COMMAND_THAT_ANSWERS).function()).findings()), [ALARM])

    def test_pure_command_is_fine(self):
        self.assertEqual(CommandQuery(Snippet("def f(self, x): self.x = x").function()).findings(), [])

    def test_pure_query_is_fine(self):
        self.assertEqual(CommandQuery(Snippet("def f(self): return self.x").function()).findings(), [])

    def test_special_methods_are_not_measured(self):
        self.assertEqual(CommandQuery(Snippet("def __enter__(self):\n    self.open = 1\n    return self").function()).findings(), [])


class ReturnsNoneTest(unittest.TestCase):
    def test_explicit_none_is_an_alarm(self):
        self.assertEqual(levels(ReturnsNone(Snippet("def f(x):\n    if x:\n        return 1\n    return None").function()).findings()), [ALARM])

    def test_bare_return_beside_a_value_is_an_alarm(self):
        self.assertEqual(levels(ReturnsNone(Snippet("def f(x):\n    if x:\n        return\n    return 1").function()).findings()), [ALARM])

    def test_optional_annotation_is_an_alarm(self):
        self.assertEqual(levels(ReturnsNone(Snippet("def f(x) -> Optional[int]: return x").function()).findings()), [ALARM])

    def test_command_returning_nothing_is_fine(self):
        self.assertEqual(ReturnsNone(Snippet("def f(self) -> None:\n    self.x = 1\n    return").function()).findings(), [])


class TrainWrecksTest(unittest.TestCase):
    def test_call_on_a_returned_object_is_a_train_wreck(self):
        self.assertEqual(levels(TrainWrecks(Snippet("def f(ctxt): ctxt.options().scratch_dir()").function()).findings()), [ALARM])

    def test_long_chain_is_reported_once(self):
        self.assertEqual(len(TrainWrecks(Snippet("def f(a): a.b().c().d()").function()).findings()), 1)

    def test_object_created_by_the_function_may_be_called(self):
        self.assertEqual(TrainWrecks(Snippet("def f(path): Path(path).read_text()").function()).findings(), [])

    def test_object_made_by_a_static_factory_may_be_called(self):
        self.assertEqual(TrainWrecks(Snippet("def f(data): Card.of(data).kind()").function()).findings(), [])

    def test_call_on_what_an_instance_returns_is_a_train_wreck(self):
        self.assertEqual(levels(TrainWrecks(Snippet("def f(deck): deck.of(1).kind()").function()).findings()), [ALARM])

    def test_call_on_what_a_constant_returns_is_a_train_wreck(self):
        self.assertEqual(levels(TrainWrecks(Snippet("def f(): RULES.get(1).kind()").function()).findings()), [ALARM])

    def test_super_may_be_called(self):
        self.assertEqual(TrainWrecks(Snippet("def f(self): super().close()").function()).findings(), [])

    def test_data_structure_operations_are_not_train_wrecks(self):
        self.assertEqual(TrainWrecks(Snippet("def f(text): clean(text).strip()").function()).findings(), [])


class SwallowedExceptionsTest(unittest.TestCase):
    def test_empty_except_swallows(self):
        self.assertEqual(levels(SwallowedExceptions(Snippet(SWALLOWING).function()).findings()), [ALARM])

    def test_translated_exception_is_fine(self):
        self.assertEqual(SwallowedExceptions(Snippet(TRANSLATING).function()).findings(), [])


class MagicNumbersTest(unittest.TestCase):
    def test_unnamed_number_is_worth_a_look(self):
        self.assertEqual(levels(MagicNumbers(Snippet("def f(days): return days * 86400").function()).findings()), [LOOK])

    def test_self_evident_numbers_are_fine(self):
        self.assertEqual(MagicNumbers(Snippet("def f(items): return items[-1] * 2 + 0").function()).findings(), [])


if __name__ == "__main__":
    unittest.main()
