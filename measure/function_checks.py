"""Fonksiyon ölçümleri (Bl.3, Bl.6, Bl.7). Her ölçüm, ölçtüğü fonksiyonu alanında tutan bir sınıftır;
yeni ölçüm yeni bir sınıftır ve FUNCTION_CHECKS'e eklenir.
"""
import ast
from abc import ABC, abstractmethod

from measure.findings import Finding, alarm, look
from measure.function import Function, Parameter
from measure.syntax import assignment_targets, is_empty_body, is_name, is_none, is_self_attribute

IDEAL_BODY_LINES = 4
MAX_BODY_LINES = 20
MAX_NESTING = 2
MAX_ARGUMENTS = 2
POLYADIC_ARGUMENTS = 4
SELF_EVIDENT_NUMBERS = frozenset({0, 1, -1, 2})
BARE_CONTAINERS = frozenset({"list", "dict", "set", "frozenset", "tuple", "type",
                             "Sequence", "Iterable", "Iterator", "Mapping", "Callable"})
TYPE_HINT_SOURCE = "Dil eşlemesi · İmza türü"


class FunctionCheck(ABC):
    """Tek fonksiyonun ölçümü; bulgu listesi döner."""

    def __init__(self, function: Function) -> None:
        self._function = function

    @abstractmethod
    def findings(self) -> list[Finding]:
        """Bulgular; temizse boş liste."""


class FunctionSize(FunctionCheck):
    def findings(self) -> list[Finding]:
        lines = self._function.body_length()
        if lines > MAX_BODY_LINES:
            return [alarm(f"{lines} satır gövde, tavan {MAX_BODY_LINES} (Bl.3 · Small!)")]
        return [look(f"{lines} satır gövde, hedef 2-{IDEAL_BODY_LINES} (Bl.3 · Small!)")] if lines > IDEAL_BODY_LINES else []


class NestingDepth(FunctionCheck):
    def findings(self) -> list[Finding]:
        depth = self._function.nesting()
        return [alarm(f"{depth} düzey girinti, en çok {MAX_NESTING} (Bl.3 · Blocks and Indenting)")] if depth > MAX_NESTING else []


class ArgumentCount(FunctionCheck):
    def findings(self) -> list[Finding]:
        count = len(self._function.signature())
        if count >= POLYADIC_ARGUMENTS:
            return [alarm(f"{count} argüman: polyadic, kullanılmaz (Bl.3 · Function Arguments; F1)")]
        return [alarm(f"{count} argüman: triadic, gerekçe ister (Bl.3 · Triads; F1)")] if count > MAX_ARGUMENTS else []


class FlagArguments(FunctionCheck):
    def findings(self) -> list[Finding]:
        return [alarm(f"bayrak argümanı '{parameter.name}' (Bl.3 · Flag Arguments; F3)")
                for parameter in self._function.signature() if self._is_flag(parameter)]

    @staticmethod
    def _is_flag(parameter: Parameter) -> bool:
        is_bool_default = isinstance(parameter.default, ast.Constant) and isinstance(parameter.default.value, bool)
        return is_name(parameter.annotation, "bool") or is_bool_default


class OutputArguments(FunctionCheck):
    def findings(self) -> list[Finding]:
        return [alarm(f"çıktı argümanı '{name}' değiştiriliyor (Bl.3 · Output Arguments; F2)")
                for name in sorted(self._function.mutated_parameters())]


class CommandQuery(FunctionCheck):
    def findings(self) -> list[Finding]:
        function = self._function
        if function.is_special() or not self._changes_state() or not function.returns_value():
            return []
        return [alarm("hem durum değiştiriyor hem değer döndürüyor (Bl.3 · Command Query Separation)")]

    def _changes_state(self) -> bool:
        assigns_self = any(is_self_attribute(t) for node in self._function.own_nodes() for t in assignment_targets(node))
        return assigns_self or bool(self._function.mutated_parameters())


class ReturnsNone(FunctionCheck):
    """Özel metodun dönüşünü dilin protokolü belirler (`__exit__` None ile istisnayı geçirir)."""

    def findings(self) -> list[Finding]:
        is_measured = not self._function.is_special() and self._may_return_none()
        return [alarm("None döndürüyor (Bl.7 · Don't Return Null)")] if is_measured else []

    def _may_return_none(self) -> bool:
        """Açık `return None`, değer döndüren fonksiyonda çıplak `return` ya da `Optional` dönüş türü."""
        returns = self._function.returns()
        bare_beside_value = self._function.returns_value() and any(node.value is None for node in returns)
        return any(is_none(node.value) for node in returns) or bare_beside_value or self._optional_annotation()

    def _optional_annotation(self) -> bool:
        annotation = self._function.return_annotation()
        text = ast.unparse(annotation) if annotation is not None else "None"
        return text != "None" and ("None" in text or "Optional" in text)


class SwallowedExceptions(FunctionCheck):
    def findings(self) -> list[Finding]:
        return [alarm("istisna yutuluyor: except gövdesi boş (Bl.7; G4)") for node in self._function.own_nodes()
                if isinstance(node, ast.ExceptHandler) and is_empty_body(node.body)]


class MagicNumbers(FunctionCheck):
    def findings(self) -> list[Finding]:
        numbers = sorted({node.value for node in self._function.own_nodes() if self._is_magic_number(node)})
        return [look(f"adsız sayılar {numbers} (Bl.2 · Use Searchable Names; G25)")] if numbers else []

    @staticmethod
    def _is_magic_number(node: ast.AST) -> bool:
        is_number = isinstance(node, ast.Constant) and type(node.value) in (int, float)
        return is_number and node.value not in SELF_EVIDENT_NUMBERS


class TypeHints(FunctionCheck):
    """İmzada her parametrenin ve dönüşün türü yazılı, kaplar içerik türüyle. Kitapta yok: kitabın Java'sında
    tür imzada dilin zorunluluğudur; Python'da yazılmazsa standart gevşer (tamam-tanimi.md · Dil eşlemesi)."""

    def findings(self) -> list[Finding]:
        return self._untyped() + self._bare()

    def _untyped(self) -> list[Finding]:
        untyped = [f"'{parameter.name}'" for parameter in self._function.signature() if parameter.annotation is None]
        untyped += [] if self._function.return_annotation() is not None else ["dönüş"]
        return [alarm(f"türü yazılı değil: {', '.join(untyped)} ({TYPE_HINT_SOURCE})")] if untyped else []

    def _bare(self) -> list[Finding]:
        bare = sorted({name for annotation in self._annotations() for name in _bare_containers(annotation)})
        quoted = ", ".join(f"'{name}'" for name in bare)
        return [alarm(f"içerik türü yazılı değil: {quoted} (G26; {TYPE_HINT_SOURCE})")] if bare else []

    def _annotations(self) -> list[ast.expr]:
        written = [parameter.annotation for parameter in self._function.signature()]
        return [annotation for annotation in written + [self._function.return_annotation()] if annotation is not None]


def _bare_containers(annotation: ast.expr) -> list[str]:
    """İçerik türü verilmemiş kap adları: `list[dict]` içindeki `dict` gibi."""
    subscripted = {id(node.value) for node in ast.walk(annotation) if isinstance(node, ast.Subscript)}
    return [node.id for node in ast.walk(annotation)
            if isinstance(node, ast.Name) and node.id in BARE_CONTAINERS and id(node) not in subscripted]


FUNCTION_CHECKS = (FunctionSize, NestingDepth, ArgumentCount, FlagArguments, OutputArguments, CommandQuery,
                   ReturnsNone, SwallowedExceptions, MagicNumbers, TypeHints)
