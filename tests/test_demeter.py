import unittest

from measure.construction import Constructions
from measure.demeter import TrainWrecks
from tests.snippets import Snippet

LOCAL_FACTORY = "def _card(x):\n    return Card(x)\n\ndef f(x):\n    _card(x).render()\n"
LOCAL_HELPER = "def _options(ctxt):\n    return ctxt.options()\n\ndef f(ctxt):\n    _options(ctxt).scratch_dir()\n"
OWN_FACTORY_METHOD = """
class Report:
    def _fixer(self):
        return Fixer()

    def f(self):
        self._fixer().plain()
"""
OWN_FIELD_METHOD = """
class Report:
    def _options(self):
        return self.options

    def f(self):
        self._options().scratch_dir()
"""
BUILD_THEN_RETURN = """
def _package():
    package = Package()
    package.add(1)
    return package

def f():
    _package().write()
"""
FACTORY_OF_FACTORY = "def _a():\n    return Alpha()\n\ndef _b():\n    return _a()\n\ndef f():\n    _b().go()\n"
SOMETIMES_EMPTY = "def _a(x):\n    if x:\n        return Alpha()\n    return\n\ndef f(x):\n    _a(x).go()\n"
PROJECT_LOADS_PROGRESS = "class Project:\n    def load(self):\n        return Progress(self._path)\n"
CACHE_LOADS_ITS_FIELD = "class Cache:\n    def load(self):\n        return self._items\n"
USES_LOADED_PROGRESS = "def f(project):\n    project.load().pages()\n"



def wrecks(*codes):
    """Kaynaklar birlikte ölçülür; fabrika bilgisi hepsinden toplanır."""
    sources = [Snippet(code) for code in codes]
    constructions = Constructions.among([function for source in sources for function in source.functions()])
    return [note.finding.message for source in sources for note in TrainWrecks(source, constructions).notes()]


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

    def test_object_made_by_a_private_class_may_be_called(self):
        self.assertEqual(wrecks("def f(html): _Parser().feed(html)"), [])

    def test_call_on_what_a_private_function_returns_is_a_train_wreck(self):
        self.assertEqual(len(wrecks("def f(x): _parse(x).go()")), 1)

    def test_call_on_what_a_private_constant_returns_is_a_train_wreck(self):
        self.assertEqual(len(wrecks("def f(): _RULES.get(1).kind()")), 1)

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

    def test_object_made_by_a_local_factory_may_be_called(self):
        self.assertEqual(wrecks(LOCAL_FACTORY), [])

    def test_call_on_what_a_local_helper_hands_out_is_a_train_wreck(self):
        self.assertEqual(len(wrecks(LOCAL_HELPER)), 1)

    def test_object_made_by_an_own_factory_method_may_be_called(self):
        self.assertEqual(wrecks(OWN_FACTORY_METHOD), [])

    def test_call_on_what_an_own_method_hands_out_is_a_train_wreck(self):
        self.assertEqual(len(wrecks(OWN_FIELD_METHOD)), 1)

    def test_factory_may_build_the_object_before_returning_it(self):
        self.assertEqual(wrecks(BUILD_THEN_RETURN), [])

    def test_factory_of_a_factory_is_a_factory(self):
        self.assertEqual(wrecks(FACTORY_OF_FACTORY), [])

    def test_helper_that_may_return_nothing_is_not_a_factory(self):
        self.assertEqual(len(wrecks(SOMETIMES_EMPTY)), 1)

    def test_factory_may_choose_between_two_constructions(self):
        self.assertEqual(wrecks("def _a(x):\n    return Alpha() if x else Beta()\n\ndef f(x):\n    _a(x).go()\n"), [])

    def test_choice_with_one_foreign_branch_is_not_a_factory(self):
        self.assertEqual(len(wrecks("def _a(x):\n    return Alpha() if x else x.beta()\n\ndef f(x):\n    _a(x).go()\n")), 1)

    def test_procedure_without_return_is_not_a_factory(self):
        self.assertEqual(len(wrecks("def _run(x):\n    x.go()\n\ndef f(x):\n    _run(x).done()\n")), 1)

    def test_object_made_by_another_modules_factory_method_may_be_called(self):
        self.assertEqual(wrecks(PROJECT_LOADS_PROGRESS, USES_LOADED_PROGRESS), [])

    def test_name_shared_with_a_method_that_is_not_a_factory_is_a_train_wreck(self):
        self.assertEqual(len(wrecks(PROJECT_LOADS_PROGRESS, CACHE_LOADS_ITS_FIELD, USES_LOADED_PROGRESS)), 1)

    def test_factory_outside_the_measured_sources_is_unknown(self):
        self.assertEqual(len(wrecks(USES_LOADED_PROGRESS)), 1)

    def test_object_made_by_another_modules_function_may_be_called(self):
        self.assertEqual(wrecks("def make_card(x):\n    return Card(x)\n", "def f(x):\n    cards.make_card(x).render()\n"), [])

    def test_factory_of_a_factory_in_another_module_is_a_factory(self):
        self.assertEqual(wrecks("def _a():\n    return Alpha()\n", "def b():\n    return _a()\n", "def f():\n    b().go()\n"), [])

    def test_data_structure_operations_are_not_train_wrecks(self):
        self.assertEqual(wrecks("def f(text): clean(text).strip()"), [])

    def test_groups_of_a_match_are_data(self):
        self.assertEqual(wrecks("def f(rule, line): rule.match(line).group(1)"), [])

    def test_questions_about_a_string_are_data(self):
        self.assertEqual(wrecks("def f(host): word_before(host).isalnum()"), [])

    def test_pattern_compiled_by_the_standard_library_may_be_called(self):
        self.assertEqual(wrecks("def f(token, text): re.compile(token).sub('', text)"), [])

    def test_call_on_what_another_objects_compile_returns_is_a_train_wreck(self):
        self.assertEqual(len(wrecks("def f(compiler, token): compiler.compile(token).sub('')")), 1)

    def test_parser_built_by_an_argument_parser_may_be_called(self):
        self.assertEqual(wrecks("def f(parser): parser.add_subparsers().add_parser('info').set_defaults(run=go)"), [])

    def test_namespace_built_by_parsing_arguments_is_data(self):
        self.assertEqual(wrecks("def f(parser, argv): parser.parse_args(argv).run()"), [])

    def test_call_on_what_another_parser_method_returns_is_a_train_wreck(self):
        self.assertEqual(len(wrecks("def f(parser): parser.get_default('x').render()")), 1)

    def test_methods_are_measured_too(self):
        self.assertEqual(len(wrecks("class Report:\n    def f(self, ctxt):\n        ctxt.options().scratch_dir()\n")), 1)


if __name__ == "__main__":
    unittest.main()
