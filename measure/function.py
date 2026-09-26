"""Ölçülen fonksiyon ve metot. Ölçümler fonksiyonu elden ele taşımaz; ona sorar (Bl.3 · SetupTeardownIncluder)."""
import ast
from typing import NamedTuple

from measure.construction import Constructions
from measure.findings import Note
from measure.syntax import assignment_targets, is_name, is_none, is_self_attribute, nesting, root_name, self_attributes, walk_own

RECEIVERS = ("self", "cls")
TEST_PREFIX = "test_"
CONSTRUCTORS = frozenset({"__init__", "setUp"})  # setUp: test sınıfının kurulumu (Bl.9 · JUnit @Before)
# tearDown kurulumun aynasıdır: kurucunun kurduğunu söker, ayrı bir sorumluluk değildir.
LIFECYCLE = CONSTRUCTORS | {"tearDown"}
CLASS_LEVEL_DECORATORS = frozenset({"staticmethod", "classmethod"})
UNBOUND_DECORATORS = CLASS_LEVEL_DECORATORS | {"abstractmethod"}
MUTATORS = frozenset({"append", "extend", "insert", "update", "add", "remove", "discard", "pop", "clear",
                      "setdefault", "sort", "reverse"})


class Parameter(NamedTuple):
    name: str
    annotation: ast.expr
    default: ast.expr


class Function:
    """Bir fonksiyonun gövdesi, imzası ve bulunduğu yer; bulguyu kendi yeriyle nota çevirir."""

    def __init__(self, node, scope):
        self._node = node
        self._scope = scope

    def note(self, finding):
        return Note(self._scope.location(self._node), finding)

    def name(self):
        return self._node.name

    def home(self):
        return self._scope.home()

    def module_home(self):
        return self._scope.module_home()

    def is_special(self):
        return self._node.name.startswith("__") and self._node.name.endswith("__")

    def is_public(self):
        return not self._node.name.startswith("_")

    def is_test(self):
        return self._node.name.startswith(TEST_PREFIX)

    def body_length(self):
        """Gövdenin satır sayısı; imza ve belge dizgisi sayılmaz."""
        statements = self.statements()
        return statements[-1].end_lineno - statements[0].lineno + 1 if statements else 0

    def statements(self):
        body = self._node.body
        return body[1:] if ast.get_docstring(self._node) is not None else body

    def nesting(self):
        return nesting(self._node)

    def own_nodes(self):
        return list(walk_own(self._node))

    def all_nodes(self):
        return list(ast.walk(self._node))

    def returns(self):
        return [node for node in self.own_nodes() if isinstance(node, ast.Return)]

    def return_annotation(self):
        return self._node.returns

    def decorators(self):
        return self._node.decorator_list

    def signature(self):
        """`self` ve `cls` dışındaki parametreler, tür bildirimi ve varsayılanıyla."""
        arguments = self._node.args
        defaults = _defaults(arguments)
        packed = [argument for argument in (arguments.vararg, arguments.kwarg) if argument]
        named = arguments.posonlyargs + arguments.args + arguments.kwonlyargs + packed
        return [Parameter(a.arg, a.annotation, defaults.get(a.arg)) for a in named if a.arg not in RECEIVERS]

    def parameter_names(self):
        return [parameter.name for parameter in self.signature()]

    def returns_value(self):
        return any(node.value is not None and not is_none(node.value) for node in self.returns())

    def mutated_parameters(self):
        """Gövdede alanı, öğesi ya da içeriği değiştirilen parametreler (çıktı argümanı)."""
        targets = [target for node in self.own_nodes() for target in _mutated_targets(node)]
        return {root_name(target) for target in targets} & set(self.parameter_names())


def _mutated_targets(node):
    targets = [target for target in assignment_targets(node) if not isinstance(target, ast.Name)]
    is_mutator = isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in MUTATORS
    return targets + ([node.func.value] if is_mutator else [])


def _defaults(arguments):
    """Varsayılanlar son konumsal argümanlara hizalanır; yalnız anahtar sözcüklü argümanlarınki ayrı durur."""
    positional = arguments.posonlyargs + arguments.args
    pairs = list(zip(positional[len(positional) - len(arguments.defaults):], arguments.defaults))
    return {argument.arg: default for argument, default in pairs + list(zip(arguments.kwonlyargs, arguments.kw_defaults))
            if default is not None}


class Method(Function):
    """Sınıfın metodu: alanlarla ilişkisi de sorulabilir."""

    def is_constructor(self):
        return self._node.name in CONSTRUCTORS

    def is_lifecycle(self):
        return self._node.name in LIFECYCLE

    def touched_attributes(self):
        return self_attributes(self._node)

    def assigned_fields(self):
        return {target.attr for node in self.own_nodes() for target in assignment_targets(node) if is_self_attribute(target)}

    def hands_out_self(self):
        """`block.accept(self)` gibi kendini başkasına veren metot; karşı taraf public metotları geri çağırabilir."""
        return any(isinstance(node, ast.Call) and any(is_name(value, "self") for value in _call_values(node))
                   for node in self.own_nodes())

    def is_accessor(self):
        """Gövdesi yalnız `return self.x` ya da yalnız `self.x = değer` olan, kurucu olmayan metot."""
        return self._is_single(_returns_field) or self.is_setter()

    def is_setter(self):
        return self._is_single(_sets_field)

    def returned_fields(self):
        """`return self.x` ile dışarı verilen alanlar."""
        return {node.value.attr for node in self.own_nodes() if _returns_field(node)}

    def collaborators(self):
        """Metodu çağrılan alanlar: `self.x.m()`. Yerinde değiştirilen veri (`append`…) işbirlikçi değildir."""
        return {node.func.value.attr for node in self.own_nodes()
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and is_self_attribute(node.func.value) and node.func.attr not in MUTATORS}

    def _is_single(self, statement_kind):
        body = self._node.body
        return len(body) == 1 and not self.is_constructor() and statement_kind(body[0])

    def is_named_constructor(self):
        """Nesneyi kuran sınıf ya da statik metot: davranış değil, adlı kurucudur (Bl.2 · Method Names)."""
        return bool(self._decorator_names() & CLASS_LEVEL_DECORATORS) and Constructions().is_factory(self)

    def does_work(self):
        return len(self._node.body) > 1 or any(isinstance(node, ast.Call) for node in self.own_nodes())

    def ignores_self(self):
        """`self`'i hiç kullanmayan örnek metodu (G14, G18)."""
        bound = not (self._decorator_names() & UNBOUND_DECORATORS)
        uses_self = any(isinstance(node, ast.Name) and node.id == "self" for node in self.own_nodes())
        return bound and not self.is_special() and not uses_self

    def _decorator_names(self):
        return {_decorator_name(decorator) for decorator in self.decorators()}


def _call_values(call):
    return call.args + [keyword.value for keyword in call.keywords]


def _returns_field(statement):
    return isinstance(statement, ast.Return) and is_self_attribute(statement.value)


def _sets_field(statement):
    return isinstance(statement, ast.Assign) and all(is_self_attribute(target) for target in statement.targets)


def _decorator_name(decorator):
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    return target.attr if isinstance(target, ast.Attribute) else getattr(target, "id", "")
