import unittest

from measure.source_checks import MIN_CARRIERS, CarriedArguments, CommentedOutCode, DispatchTables, TodosWithoutTicket
from tests.snippets import Snippet, names


def functions_taking(name, count):
    return "".join(f"def step{index}({name}, kind):\n    return {name}\n\n" for index in range(count))


DISPATCH_TABLE = """
def _sides(card):
    return card

def _options(card):
    return card

_MIDDLE_PARTS = {"contrast": _sides, "code": _sides, "tradeoff": _options}
"""

LABEL_TABLE = 'SIDE_LABELS = {"code": ("Önce", "Sonra"), "contrast": ("Kaçın", "Tercih et")}\n'

DECLARED_PROCEDURAL = '"""Prosedürel (Bl.6): türler sabit, sorular çoğalıyor."""\n' + functions_taking("node", MIN_CARRIERS)


def lines_of(notes):
    return [note.location.line for note in notes]


class CommentedOutCodeTest(unittest.TestCase):
    def test_commented_statement_is_code(self):
        self.assertEqual(lines_of(CommentedOutCode(Snippet("x = 1\n# total = x + 2\n")).notes()), [2])

    def test_consecutive_commented_lines_form_one_block(self):
        self.assertEqual(lines_of(CommentedOutCode(Snippet("# for item in items:\n#     go(item)\n")).notes()), [1])

    def test_prose_comment_is_not_code(self):
        self.assertEqual(CommentedOutCode(Snippet("# Sayfa sonunda yarım kalan paragraf birleşir.\n")).notes(), [])

    def test_single_word_comment_is_not_code(self):
        self.assertEqual(CommentedOutCode(Snippet("# noqa\n")).notes(), [])

    def test_trailing_comment_is_not_a_block(self):
        self.assertEqual(CommentedOutCode(Snippet("x = 1  # type: int\n")).notes(), [])


class TodosWithoutTicketTest(unittest.TestCase):
    def test_todo_without_ticket_raises_an_alarm(self):
        self.assertEqual(lines_of(TodosWithoutTicket(Snippet("# TODO kartları sırala\n")).notes()), [1])

    def test_todo_with_ticket_is_fine(self):
        self.assertEqual(TodosWithoutTicket(Snippet("# TODO KC-12 kartları sırala\n")).notes(), [])

    def test_todo_inside_a_string_is_not_a_comment(self):
        self.assertEqual(TodosWithoutTicket(Snippet('PATTERN = "# TODO"\n')).notes(), [])


class CarriedArgumentsTest(unittest.TestCase):
    def test_argument_carried_through_enough_functions_raises_an_alarm(self):
        notes = CarriedArguments(Snippet(functions_taking("card", MIN_CARRIERS))).notes()
        self.assertEqual([note.finding.message.split("'")[1] for note in notes], ["card", "kind"])

    def test_argument_in_fewer_functions_is_fine(self):
        self.assertEqual(CarriedArguments(Snippet(functions_taking("card", MIN_CARRIERS - 1))).notes(), [])

    def test_methods_are_not_counted(self):
        code = "class Card:\n" + "".join(f"    def step{i}(self, card):\n        return card\n" for i in range(MIN_CARRIERS))
        self.assertEqual(CarriedArguments(Snippet(code)).notes(), [])

    def test_declared_procedural_module_is_not_measured(self):
        self.assertEqual(CarriedArguments(Snippet(DECLARED_PROCEDURAL)).notes(), [])


class DispatchTablesTest(unittest.TestCase):
    def test_string_keyed_table_of_functions_is_a_switch(self):
        self.assertEqual(names(DispatchTables(Snippet(DISPATCH_TABLE)).notes()), ["_MIDDLE_PARTS"])

    def test_table_of_plain_values_is_not_a_switch(self):
        self.assertEqual(DispatchTables(Snippet(LABEL_TABLE)).notes(), [])


if __name__ == "__main__":
    unittest.main()
