"""Ölçülen fonksiyon ve metot. Ölçümler fonksiyonu elden ele taşımaz; ona sorar (Bl.3 · SetupTeardownIncluder)."""
from __future__ import annotations

import ast
from collections.abc import Callable
from typing import NamedTuple

from measure.construction import Constructions
from measure.findings import Finding, Note
from measure.scope import Home, Scope
from measure.syntax import (FunctionNode, admits_none, assignment_targets, end_line, is_name, is_none,
                            is_self_attribute, nesting, root_name, self_attributes, walk_own)

RECEIVERS = ("self", "cls")
TEST_PREFIX = "test_"
CONSTRUCTORS = frozenset({"__init__", "setUp"})  # setUp: test sınıfının kurulumu (Bl.9 · JUnit @Before)
# tearDown kurulumun aynasıdır: kurucunun kurduğunu söker, ayrı bir sorumluluk değildir.
LIFECYCLE = CONSTRUCTORS | {"tearDown"}
CLASS_LEVEL_DECORATORS = frozenset({"staticmethod", "classmethod"})
UNBOUND_DECORATORS = CLASS_LEVEL_DECORATORS | {"abstractmethod"}
CONTEXT_MANAGER_DECORATORS = frozenset({"contextmanager", "asynccontextmanager"})
MUTATORS = frozenset({"append", "extend", "insert", "update", "add", "remove", "discard", "pop", "clear",
                      "setdefault", "sort", "reverse"})


class Parameter(NamedTuple):
    name: str
    annotation: ast.expr | None
    default: ast.expr | None


class Function:
    """Bir fonksiyonun gövdesi, imzası ve bulunduğu yer; bulguyu kendi yeriyle nota çevirir."""

    def __init__(self, node: FunctionNode, scope: Scope) -> None:
        self._node = node
        self._scope = scope

    def note(self, finding: Finding) -> Note:
        return Note(self._scope.location(self._node), finding)

    def name(self) -> str:
        return self._node.name

    def home(self) -> Home:
        return self._scope.home()

    def module_home(self) -> Home:
        return self._scope.module_home()

    def is_special(self) -> bool:
        return self._node.name.startswith("__") and self._node.name.endswith("__")

    def is_public(self) -> bool:
        return not self._node.name.startswith("_")

    def is_test(self) -> bool:
        return self._node.name.startswith(TEST_PREFIX)

    def body_length(self) -> int:
        """Gövdenin satır sayısı; imza ve belge dizgisi sayılmaz."""
        statements = self.statements()
        return end_line(statements[-1]) - statements[0].lineno + 1 if statements else 0

    def statements(self) -> list[ast.stmt]:
        body = self._node.body
        return body[1:] if ast.get_docstring(self._node) is not None else body

    def nesting(self) -> int:
        return nesting(self._node)

    def own_nodes(self) -> list[ast.AST]:
        return list(walk_own(self._node))

    def all_nodes(self) -> list[ast.AST]:
        return list(ast.walk(self._node))

    def returns(self) -> list[ast.Return]:
        return [node for node in self.own_nodes() if isinstance(node, ast.Return)]

    def handed_out(self) -> list[ast.expr | None]:
        """Çağırana verilen değerler: dönüşler; bağlam yöneticisi üretecinde `with … as` hedefine giden `yield`ler."""
        if self._decorator_names() & CONTEXT_MANAGER_DECORATORS:
            return [node.value for node in self.own_nodes() if isinstance(node, ast.Yield)]
        return [node.value for node in self.returns()]

    def has_return_type(self) -> bool:
        return self._node.returns is not None

    def return_type_admits_none(self) -> bool:
        """Yazılı dönüş türü boş dönüşe izin veriyor mu; `-> None` komutu boş dönüş sayılmaz."""
        returns = self._node.returns
        return returns is not None and not is_none(returns) and admits_none(returns)

    def written_types(self) -> list[ast.expr]:
        """İmzada yazılmış türler: parametrelerinki ve dönüşünki."""
        written = [parameter.annotation for parameter in self.signature()] + [self._node.returns]
        return [annotation for annotation in written if annotation is not None]

    def decorators(self) -> list[ast.expr]:
        return self._node.decorator_list

    def _decorator_names(self) -> set[str]:
        return {_decorator_name(decorator) for decorator in self.decorators()}

    def signature(self) -> list[Parameter]:
        """`self` ve `cls` dışındaki parametreler, tür bildirimi ve varsayılanıyla."""
        arguments = self._node.args
        defaults = _defaults(arguments)
        packed = [argument for argument in (arguments.vararg, arguments.kwarg) if argument]
        named = arguments.posonlyargs + arguments.args + arguments.kwonlyargs + packed
        return [Parameter(a.arg, a.annotation, defaults.get(a.arg)) for a in named if a.arg not in RECEIVERS]

    def parameter_names(self) -> list[str]:
        return [parameter.name for parameter in self.signature()]

    def returns_value(self) -> bool:
        return any(node.value is not None and not is_none(node.value) for node in self.returns())

    def mutated_parameters(self) -> set[str]:
        """Gövdede alanı, öğesi ya da içeriği değiştirilen parametreler (çıktı argümanı)."""
        targets = [target for node in self.own_nodes() for target in _mutated_targets(node)]
        return {root_name(target) for target in targets} & set(self.parameter_names())


def _mutated_targets(node: ast.AST) -> list[ast.expr]:
    targets = [target for target in assignment_targets(node) if not isinstance(target, ast.Name)]
    is_mutator = isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in MUTATORS
    return targets + ([node.func.value] if is_mutator else [])


def _defaults(arguments: ast.arguments) -> dict[str, ast.expr]:
    """Varsayılanlar son konumsal argümanlara hizalanır; yalnız anahtar sözcüklü argümanlarınki ayrı durur."""
    positional = arguments.posonlyargs + arguments.args
    pairs = list(zip(positional[len(positional) - len(arguments.defaults):], arguments.defaults))
    return {argument.arg: default for argument, default in pairs + list(zip(arguments.kwonlyargs, arguments.kw_defaults))
            if default is not None}


class Method(Function):
    """Sınıfın metodu: alanlarla ilişkisi de sorulabilir."""

    def is_constructor(self) -> bool:
        return self._node.name in CONSTRUCTORS

    def is_lifecycle(self) -> bool:
        return self._node.name in LIFECYCLE

    def touched_attributes(self) -> set[str]:
        return self_attributes(self._node)

    def assigned_fields(self) -> set[str]:
        return {target.attr for node in self.own_nodes() for target in assignment_targets(node) if is_self_attribute(target)}

    def hands_out_self(self) -> bool:
        """`block.accept(self)` gibi kendini başkasına veren metot; karşı taraf public metotları geri çağırabilir."""
        return any(isinstance(node, ast.Call) and any(is_name(value, "self") for value in _call_values(node))
                   for node in self.own_nodes())

    def is_accessor(self) -> bool:
        """Gövdesi yalnız `return self.x` ya da yalnız `self.x = değer` olan, kurucu olmayan metot."""
        return self._is_single(_returns_field) or self.is_setter()

    def is_setter(self) -> bool:
        return self._is_single(_sets_field)

    def returned_fields(self) -> set[str]:
        """`return self.x` ile dışarı verilen alanlar."""
        return {node.value.attr for node in self.own_nodes() if _returns_field(node)}

    def collaborators(self) -> set[str]:
        """Metodu çağrılan alanlar: `self.x.m()`. Yerinde değiştirilen veri (`append`…) işbirlikçi değildir."""
        return {node.func.value.attr for node in self.own_nodes()
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and is_self_attribute(node.func.value) and node.func.attr not in MUTATORS}

    def _is_single(self, statement_kind: Callable[[ast.stmt], bool]) -> bool:
        body = self._node.body
        return len(body) == 1 and not self.is_constructor() and statement_kind(body[0])

    def is_named_constructor(self) -> bool:
        """Nesneyi kuran sınıf ya da statik metot: davranış değil, adlı kurucudur (Bl.2 · Method Names)."""
        return bool(self._decorator_names() & CLASS_LEVEL_DECORATORS) and Constructions().is_factory(self)

    def does_work(self) -> bool:
        return len(self._node.body) > 1 or any(isinstance(node, ast.Call) for node in self.own_nodes())

    def ignores_self(self) -> bool:
        """`self`'i hiç kullanmayan örnek metodu (G14, G18)."""
        bound = not (self._decorator_names() & UNBOUND_DECORATORS)
        uses_self = any(isinstance(node, ast.Name) and node.id == "self" for node in self.own_nodes())
        return bound and not self.is_special() and not uses_self


def _call_values(call: ast.Call) -> list[ast.expr]:
    return call.args + [keyword.value for keyword in call.keywords]


def _returns_field(statement: ast.AST) -> bool:
    return isinstance(statement, ast.Return) and is_self_attribute(statement.value)


def _sets_field(statement: ast.AST) -> bool:
    return isinstance(statement, ast.Assign) and all(is_self_attribute(target) for target in statement.targets)


def _decorator_name(decorator: ast.expr) -> str:
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    return target.attr if isinstance(target, ast.Attribute) else getattr(target, "id", "")
