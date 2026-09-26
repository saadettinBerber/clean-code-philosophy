import ast
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
CLASS_METHOD_BUILDS_WITH_CLS = """
class Deck:
    @classmethod
    def of(cls, cards):
        return cls(cards).shuffled()
"""
ONE_FOREIGN_BRANCH = "def _a(x):\n    return Alpha() if x else x.beta()\n\ndef f(x):\n    _a(x).go()\n"
REDIRECTED = """
def f(run):
    with contextlib.redirect_stdout(io.StringIO()) as output:
        run()
    output.getvalue()
"""
MODULE_TABLE = '_KINDS = {"a": Alpha, "b": Beta}\n'
LOCAL_TABLE = 'def f(position):\n    kinds = {"top": Top, "none": NoHeader}\n    kinds[position]().go()\n'
CLASSES_OF_A_COMPREHENSION = '_CARDS = {card.KIND: card for card in (Explain, Contrast)}\n'
FACTORY_CHOOSING_FROM_A_TABLE = MODULE_TABLE + "def make(data):\n    return _KINDS.get(data, Gamma)(data)\n"
SOMETIMES_EMPTY = "def _a(x):\n    if x:\n        return Alpha()\n    return\n\ndef f(x):\n    _a(x).go()\n"
PROJECT_LOADS_PROGRESS = "class Project:\n    def load(self):\n        return Progress(self._path)\n"
CACHE_LOADS_ITS_FIELD = "class Cache:\n    def load(self):\n        return self._items\n"
USES_LOADED_PROGRESS = "def f(project):\n    project.load().pages()\n"
DOCUMENT_BUILDS_PAGES = """
class Document:
    def page(self, number):
        return Page(self, number)

    def text(self, number):
        return self.page(number).text()
"""
METHOD_CALLS_MODULE_FACTORY = """
def _para(x):
    return Para(x)

class ParaTest:
    def test_go(self):
        _para(1).go()
"""
DOCUMENT_ASKS_ANOTHER = """
class Document:
    def page(self, number):
        return Page(self, number)

    def copy_text(self, other):
        return other.page(1).text()
"""
FAKE_HOLDS_PAGES = "class FakeDocument:\n    def page(self, number):\n        return self._pages[number]\n"



def wrecks(*codes):
    """Kaynaklar birlikte ölçülür; fabrika bilgisi hepsinden toplanır."""
    sources = [Snippet(code, f"parca{index}.py") for index, code in enumerate(codes)]
    constructions = Constructions.among(sources)
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
        self.assertEqual(wrecks(CLASS_METHOD_BUILDS_WITH_CLS), [])

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

    def test_procedure_without_return_is_not_a_factory(self):
        self.assertEqual(len(wrecks("def _run(x):\n    x.go()\n\ndef f(x):\n    _run(x).done()\n")), 1)

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
        self.assertEqual(len(wrecks("class Report:\n    def f(self, ctxt):\n        ctxt.options().dir()\n")), 1)



class FactoryKnowledgeTest(unittest.TestCase):
    """Kimin nesne kurduğu: başka modülün fabrikası, çağıranın kapsamında ad çözümü, tablodan seçilen sınıf,
    bağlam yöneticisi (Bl.6 · The Law of Demeter; Bl.3 · Switch Statements)."""

    def test_choice_with_one_foreign_branch_is_not_a_factory(self):
        self.assertEqual(len(wrecks(ONE_FOREIGN_BRANCH)), 1)

    def test_object_made_by_another_modules_factory_method_may_be_called(self):
        self.assertEqual(wrecks(PROJECT_LOADS_PROGRESS, USES_LOADED_PROGRESS), [])

    def test_name_shared_with_a_method_that_is_not_a_factory_is_a_train_wreck(self):
        self.assertEqual(len(wrecks(PROJECT_LOADS_PROGRESS, CACHE_LOADS_ITS_FIELD, USES_LOADED_PROGRESS)), 1)

    def test_factory_outside_the_measured_sources_is_unknown(self):
        self.assertEqual(len(wrecks(USES_LOADED_PROGRESS)), 1)

    def test_object_made_by_another_modules_function_may_be_called(self):
        self.assertEqual(wrecks("def make_card(x):\n    return Card(x)\n", "def f(x): cards.make_card(x).go()"), [])

    def test_factory_of_a_factory_in_another_module_is_a_factory(self):
        self.assertEqual(wrecks("def _a():\n    return Alpha()\n", "def b(): return _a()", "def f(): b().go()"), [])

    def test_bare_name_resolves_to_its_own_modules_factory_first(self):
        self.assertEqual(wrecks("def _para(x):\n    return Para(x)\n\ndef f(x):\n    _para(x).go()\n",
                                "def _para(x):\n    return x.para\n"), [])

    def test_own_method_resolves_to_its_own_classs_factory_first(self):
        self.assertEqual(wrecks(DOCUMENT_BUILDS_PAGES, FAKE_HOLDS_PAGES), [])

    def test_bare_name_in_a_method_resolves_to_its_own_modules_factory_first(self):
        self.assertEqual(wrecks(METHOD_CALLS_MODULE_FACTORY, "def _para(x):\n    return x.para\n"), [])

    def test_another_objects_method_does_not_resolve_to_the_callers_class(self):
        self.assertEqual(len(wrecks(DOCUMENT_ASKS_ANOTHER, FAKE_HOLDS_PAGES)), 1)

    def test_method_of_another_object_resolves_among_all_sources(self):
        self.assertEqual(len(wrecks(DOCUMENT_BUILDS_PAGES, FAKE_HOLDS_PAGES, "def f(doc): doc.page(1).text()")), 1)

    def test_class_chosen_from_a_table_builds_the_object(self):
        self.assertEqual(wrecks(MODULE_TABLE + "def f(data): _KINDS[data](data).go()"), [])

    def test_factory_choosing_its_class_from_a_table_is_a_factory(self):
        self.assertEqual(wrecks(FACTORY_CHOOSING_FROM_A_TABLE + "def f(data):\n    make(data).go()\n"), [])

    def test_class_chosen_from_a_local_table_builds_the_object(self):
        self.assertEqual(wrecks(LOCAL_TABLE), [])

    def test_table_of_classes_built_by_a_comprehension_builds_too(self):
        self.assertEqual(wrecks(CLASSES_OF_A_COMPREHENSION + "def f(data): _CARDS[data](data).go()"), [])

    def test_table_holding_something_other_than_a_class_is_not_a_constructor(self):
        self.assertEqual(len(wrecks('_HANDLERS = {"a": Alpha, "b": handle}\ndef f(x): _HANDLERS[x](x).go()')), 1)

    def test_choice_without_a_default_class_may_hand_out_anything(self):
        self.assertEqual(len(wrecks(MODULE_TABLE + "def f(x): _KINDS.get(x)(x).go()")), 1)

    def test_choice_with_a_default_that_is_not_a_class_may_hand_out_anything(self):
        self.assertEqual(len(wrecks(MODULE_TABLE + "def f(x, fallback): _KINDS.get(x, fallback)(x).go()")), 1)

    def test_table_passed_in_as_an_argument_is_unknown(self):
        self.assertEqual(len(wrecks("def f(kinds, x): kinds[x](x).go()")), 1)

    def test_local_name_hides_the_modules_table(self):
        self.assertEqual(len(wrecks(MODULE_TABLE + "def f(x, other):\n    _KINDS = other\n    _KINDS[x](x).go()\n")), 1)

    def test_table_of_another_module_is_not_seen(self):
        self.assertEqual(len(wrecks(MODULE_TABLE, "def f(x): _KINDS[x](x).go()")), 1)

    def test_local_name_bound_to_a_table_and_to_something_else_is_unknown(self):
        code = 'def f(x, other):\n    kinds = {"a": Alpha}\n    kinds = other\n    kinds[x]().go()\n'
        self.assertEqual(len(wrecks(code)), 1)

    def test_module_name_bound_to_a_table_and_to_something_else_is_unknown(self):
        self.assertEqual(len(wrecks(MODULE_TABLE + "_KINDS = load()\ndef f(x): _KINDS[x](x).go()")), 1)

    def test_comprehension_over_an_item_that_is_not_a_class_is_not_a_table_of_classes(self):
        self.assertEqual(len(wrecks("_CARDS = {c.KIND: c for c in (Explain, helper)}\ndef f(x): _CARDS[x](x).go()")), 1)

    def test_only_get_chooses_from_a_table(self):
        self.assertEqual(len(wrecks(MODULE_TABLE + "def f(x): _KINDS.pick(x, Gamma)(x).go()")), 1)

    def test_comprehension_over_unknown_items_is_not_a_table_of_classes(self):
        self.assertEqual(len(wrecks("_CARDS = {c.KIND: c for c in CARDS}\ndef f(x): _CARDS[x](x).go()")), 1)







SPLIT = "def f(ctxt):\n    options = ctxt.options()\n    options.scratch_dir()\n"
MAYBE_A_STRANGER = "def f(a, c):\n    if c:\n        x = a.b()\n    else:\n        x = Box()\n    x.c()\n"
FRIEND_AFTER_THE_BRANCH = "def f(a, c):\n    if c:\n        x = a.b()\n    x = Box()\n    x.c()\n"
FRIEND_IN_ITS_OWN_BRANCH = "def f(a, c):\n    if c:\n        x = a.b()\n    else:\n        x = Box()\n        x.c()\n"
NESTED_FUNCTION_BINDS = "def f(a, x):\n    def g():\n        x = a.b()\n        return x\n    x.c()\n"
FIELD_HOLDS_IT = "class Report:\n    def f(self, a):\n        self.x = a.b()\n        self.x.c()\n"
CAUGHT = "def f(a):\n    e = a.b()\n    try:\n        a.go()\n    except OSError as e:\n        e.log()\n"


class SplitChainTest(unittest.TestCase):
    """Zinciri ara değişkene bölmek ihlali gidermez (Bl.6 · Train Wrecks, Hiding Structure)."""

    def test_chain_split_through_a_local_name_is_a_train_wreck(self):
        self.assertEqual(wrecks(SPLIT), ["ara değişkene bölünmüş zincir 'options = ctxt.options()' → "
                                         "'options.scratch_dir()' (Bl.6 · Train Wrecks; G36)"])

    def test_object_the_function_built_may_be_called_through_a_name(self):
        self.assertEqual(wrecks("def f(path):\n    text = Path(path)\n    text.read_text()\n"), [])

    def test_argument_rebound_to_a_stranger_is_a_stranger(self):
        self.assertEqual(len(wrecks("def f(ctxt, other):\n    ctxt = other.child()\n    ctxt.go()\n")), 1)

    def test_rebinding_to_a_construction_makes_a_friend(self):
        self.assertEqual(wrecks("def f(a):\n    x = a.b()\n    x = Box()\n    x.c()\n"), [])

    def test_call_before_the_binding_talks_to_the_argument(self):
        self.assertEqual(wrecks("def f(a, x):\n    x.c()\n    x = a.b()\n"), [])

    def test_data_structure_operation_on_a_stranger_is_not_a_train_wreck(self):
        self.assertEqual(wrecks("def f(a):\n    name = a.b()\n    name.strip()\n"), [])

    def test_annotated_binding_is_followed(self):
        self.assertEqual(len(wrecks("def f(a):\n    x: Options = a.b()\n    x.c()\n")), 1)

    def test_walrus_binding_is_followed(self):
        self.assertEqual(len(wrecks("def f(a):\n    if (x := a.b()):\n        x.c()\n")), 1)

    def test_context_handed_out_by_another_object_is_a_stranger(self):
        self.assertEqual(len(wrecks("def f(a):\n    with a.lock() as held:\n        held.release()\n")), 1)

    def test_redirected_output_is_a_friend(self):
        self.assertEqual(wrecks(REDIRECTED), [])

    def test_redirector_imported_by_name_builds_too(self):
        self.assertEqual(wrecks(REDIRECTED.replace("contextlib.redirect_stdout", "redirect_stderr")), [])

    def test_opened_file_is_a_friend(self):
        self.assertEqual(wrecks("def f(path):\n    with open(path) as file:\n        file.read()\n"), [])

    def test_stranger_bound_in_one_branch_may_reach_the_call(self):
        self.assertEqual(len(wrecks(MAYBE_A_STRANGER)), 1)

    def test_friend_bound_after_the_branch_cuts_the_stranger_off(self):
        self.assertEqual(wrecks(FRIEND_AFTER_THE_BRANCH), [])

    def test_friend_bound_in_the_callers_own_branch_cuts_the_stranger_off(self):
        self.assertEqual(wrecks(FRIEND_IN_ITS_OWN_BRANCH), [])

    def test_loop_element_is_collection_access(self):
        self.assertEqual(wrecks("def f(a, items):\n    x = a.b()\n    for x in items:\n        x.c()\n"), [])

    def test_unpacked_element_is_collection_access(self):
        self.assertEqual(wrecks("def f(a):\n    first, rest = a.split_off()\n    first.render()\n"), [])

    def test_names_of_a_literal_tuple_are_followed_one_by_one(self):
        self.assertEqual(len(wrecks("def f(a):\n    x, y = a.b(), Box()\n    x.c()\n    y.c()\n")), 1)

    def test_field_is_a_friend(self):
        self.assertEqual(wrecks(FIELD_HOLDS_IT), [])

    def test_nested_functions_bindings_do_not_leak(self):
        self.assertEqual(wrecks(NESTED_FUNCTION_BINDS), [])

    def test_copied_stranger_stays_a_stranger(self):
        self.assertEqual(len(wrecks("def f(a):\n    x = a.b()\n    y = x\n    y.c()\n")), 1)

    def test_comprehension_names_its_own_elements(self):
        self.assertEqual(wrecks("def f(a, pages):\n    p = a.b()\n    return [p.render() for p in pages]\n"), [])

    def test_caught_exception_is_a_friend(self):
        self.assertEqual(wrecks(CAUGHT), [])

    def test_chain_continuing_from_a_split_is_reported_once(self):
        self.assertEqual(len(wrecks("def f(a):\n    x = a.b()\n    x.c().d()\n")), 1)

    def test_object_made_by_another_modules_factory_may_be_called_through_a_name(self):
        split = "def f(project):\n    progress = project.load()\n    progress.pages()\n"
        self.assertEqual(wrecks(PROJECT_LOADS_PROGRESS, split), [])


class SplitEqualsChainTest(unittest.TestCase):
    """Zincirli ve bölünmüş yazılış her zaman aynı kararı verir; iki halkalı zincirde alarm sayısı da aynıdır."""

    def test_every_chain_decides_like_its_split(self):
        for code in CHAINS:
            with self.subTest(code=code):
                self.assertEqual(bool(wrecks(*code)), bool(wrecks(*split_all(code))))

    def test_two_link_chain_counts_like_its_split(self):
        for code in TWO_LINK_CHAINS:
            with self.subTest(code=code):
                self.assertEqual(len(wrecks(*code)), len(wrecks(*split_all(code))))


TWO_LINK_CHAINS = [
    ("def f(ctxt): ctxt.options().scratch_dir()",), ("def f(path): Path(path).read_text()",),
    ("def f(data): Card.of(data).kind()",), ("def f(deck): deck.of(1).kind()",), ("def f(): RULES.get(1).kind()",),
    ("def f(html): _Parser().feed(html)",), ("def f(x): _parse(x).go()",), ("def f(path): open(path).read()",),
    ("def f(path): zipfile.open_zip(path).read('a')",), ("def f(items): next(iter(items)).render()",),
    ("def f(text): clean(text).strip()",), ("def f(rule, line): rule.match(line).group(1)",),
    ("def f(token, text): re.compile(token).sub('', text)",), ("def f(parser, argv): parser.parse_args(argv).run()",),
    (LOCAL_FACTORY,), (LOCAL_HELPER,), (OWN_FACTORY_METHOD,), (OWN_FIELD_METHOD,), (BUILD_THEN_RETURN,),
    (FACTORY_OF_FACTORY,), (SOMETIMES_EMPTY,), (PROJECT_LOADS_PROGRESS, USES_LOADED_PROGRESS),
    (PROJECT_LOADS_PROGRESS, CACHE_LOADS_ITS_FIELD, USES_LOADED_PROGRESS), (USES_LOADED_PROGRESS,),
    (DOCUMENT_BUILDS_PAGES, FAKE_HOLDS_PAGES), (METHOD_CALLS_MODULE_FACTORY, "def _para(x):\n    return x.para\n"),
]
CHAINS = TWO_LINK_CHAINS + [("def f(a): a.b().c().d()",), ("def f(klass):\n    klass(1).of(2).go()\n",),
                            ("def f(parser): parser.add_subparsers().add_parser('info').set_defaults(run=go)",)]


def split_all(codes):
    """Her zincir halkası bir ara değişkene bölünür: `a.b().c()` → `link = a.b()` ve `link.c()`."""
    return tuple(ast.unparse(_Splitter().visit(ast.parse(code))) for code in codes)


class _Splitter(ast.NodeTransformer):
    """Deyimin değerindeki zinciri, halka halka ara değişkenlere açar."""

    def generic_visit(self, node):
        super().generic_visit(node)
        for field in ("body", "orelse"):
            if isinstance(getattr(node, field, None), list):
                setattr(node, field, [split for statement in getattr(node, field) for split in self._split(statement)])
        return node

    @classmethod
    def _split(cls, statement):
        call = getattr(statement, "value", None)
        is_chain = isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
        if not (is_chain and isinstance(call.func.value, ast.Call)):
            return [statement]
        link = f"link{id(call)}"
        before = ast.Assign(targets=[ast.Name(link, ast.Store())], value=call.func.value, lineno=0)
        call.func.value = ast.Name(link, ast.Load())
        return cls._split(before) + [statement]


if __name__ == "__main__":
    unittest.main()
