import unittest

from measure.demeter import TrainWrecks
from tests.snippets import Snippet


def wrecks(code):
    return [note.finding.message for note in TrainWrecks(Snippet(code)).notes()]


class TrainWrecksTest(unittest.TestCase):
    def test_call_on_a_returned_object_is_a_train_wreck(self):
        self.assertEqual(len(wrecks("def f(ctxt): ctxt.options().scratch_dir()")), 1)

    def test_long_chain_is_reported_once(self):
        self.assertEqual(len(wrecks("def f(a): a.b().c().d()")), 1)

    def test_object_created_by_the_function_may_be_called(self):
        self.assertEqual(wrecks("def f(path): Path(path).read_text()"), [])

    def test_object_made_by_a_static_factory_may_be_called(self):
        self.assertEqual(wrecks("def f(data): Card.of(data).kind()"), [])

    def test_call_on_what_an_instance_returns_is_a_train_wreck(self):
        self.assertEqual(len(wrecks("def f(deck): deck.of(1).kind()")), 1)

    def test_call_on_what_a_constant_returns_is_a_train_wreck(self):
        self.assertEqual(len(wrecks("def f(): RULES.get(1).kind()")), 1)

    def test_object_made_by_a_module_qualified_class_may_be_called(self):
        self.assertEqual(wrecks("def f(path): zipfile.ZipFile(path).read('a')"), [])

    def test_call_on_what_a_module_function_returns_is_a_train_wreck(self):
        self.assertEqual(len(wrecks("def f(path): zipfile.open_zip(path).read('a')")), 1)

    def test_super_may_be_called(self):
        self.assertEqual(wrecks("def f(self): super().close()"), [])

    def test_opened_file_may_be_read(self):
        self.assertEqual(wrecks("def f(path): open(path).read()"), [])

    def test_object_made_by_a_built_in_type_may_be_called(self):
        self.assertEqual(wrecks("def f(items): list(items).sort()"), [])

    def test_call_on_what_a_built_in_function_hands_out_is_a_train_wreck(self):
        self.assertEqual(len(wrecks("def f(items): next(iter(items)).render()")), 1)

    def test_object_a_class_method_builds_with_cls_may_be_called(self):
        self.assertEqual(wrecks("class Deck:\n    @classmethod\n    def of(cls, cards):\n        return cls(cards).shuffled()\n"), [])

    def test_call_on_what_a_parameter_named_like_cls_hands_out_is_a_train_wreck(self):
        self.assertEqual(len(wrecks("def f(klass):\n    klass(1).of(2).go()\n")), 1)

    def test_data_structure_operations_are_not_train_wrecks(self):
        self.assertEqual(wrecks("def f(text): clean(text).strip()"), [])

    def test_methods_are_measured_too(self):
        self.assertEqual(len(wrecks("class Report:\n    def f(self, ctxt):\n        ctxt.options().scratch_dir()\n")), 1)


if __name__ == "__main__":
    unittest.main()
