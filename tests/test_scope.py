import ast
import unittest

from measure.findings import Location
from measure.scope import Scope

PATH = "kart.py"
CARD = "class Card:\n    def render(self): pass\n"
[CARD_CLASS] = [node for node in ast.parse(CARD).body if isinstance(node, ast.ClassDef)]
[RENDER_METHOD] = [node for node in CARD_CLASS.body if isinstance(node, ast.FunctionDef)]
CLASS_LINE = 1
METHOD_LINE = 2


class ScopeTest(unittest.TestCase):
    def test_top_level_definition_is_named_by_itself(self) -> None:
        self.assertEqual(Scope(PATH).location(CARD_CLASS), Location(PATH, CLASS_LINE, "Card"))

    def test_inner_definition_is_named_after_its_owner(self) -> None:
        inside = Scope(PATH).inner(CARD_CLASS)
        self.assertEqual(inside.location(RENDER_METHOD), Location(PATH, METHOD_LINE, "Card.render"))


if __name__ == "__main__":
    unittest.main()
