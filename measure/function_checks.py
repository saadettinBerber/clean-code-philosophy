"""Fonksiyon ölçümleri (Bl.3, Bl.6, Bl.7). Her ölçüm, ölçtüğü fonksiyonu alanında tutan bir sınıftır;
yeni ölçüm yeni bir sınıftır ve FUNCTION_CHECKS'e eklenir.
"""
import ast
from abc import ABC, abstractmethod

from measure.findings import alarm, look
from measure.syntax import assignment_targets, is_empty_body, is_name, is_none, is_self_attribute

IDEAL_BODY_LINES = 4
MAX_BODY_LINES = 20
MAX_NESTING = 2
MAX_ARGUMENTS = 2
POLYADIC_ARGUMENTS = 4
SELF_EVIDENT_NUMBERS = frozenset({0, 1, -1, 2})


class FunctionCheck(ABC):
    """Tek fonksiyonun ölçümü; bulgu listesi döner."""

    def __init__(self, function):
        self._function = function

    @abstractmethod
    def findings(self):
        """Bulgular; temizse boş liste."""


class FunctionSize(FunctionCheck):
    def findings(self):
        lines = self._function.body_length()
        if lines > MAX_BODY_LINES:
            return [alarm(f"{lines} satır gövde, tavan {MAX_BODY_LINES} (Bl.3 · Small!)")]
        return [look(f"{lines} satır gövde, hedef 2-{IDEAL_BODY_LINES} (Bl.3 · Small!)")] if lines > IDEAL_BODY_LINES else []


class NestingDepth(FunctionCheck):
    def findings(self):
        depth = self._function.nesting()
        return [alarm(f"{depth} düzey girinti, en çok {MAX_NESTING} (Bl.3 · Blocks and Indenting)")] if depth > MAX_NESTING else []


class ArgumentCount(FunctionCheck):
    def findings(self):
        count = len(self._function.signature())
        if count >= POLYADIC_ARGUMENTS:
            return [alarm(f"{count} argüman: polyadic, kullanılmaz (Bl.3 · Function Arguments; F1)")]
        return [alarm(f"{count} argüman: triadic, gerekçe ister (Bl.3 · Triads; F1)")] if count > MAX_ARGUMENTS else []


class FlagArguments(FunctionCheck):
    def findings(self):
        return [alarm(f"bayrak argümanı '{parameter.name}' (Bl.3 · Flag Arguments; F3)")
                for parameter in self._function.signature() if self._is_flag(parameter)]

    @staticmethod
    def _is_flag(parameter):
        is_bool_default = isinstance(parameter.default, ast.Constant) and isinstance(parameter.default.value, bool)
        return is_name(parameter.annotation, "bool") or is_bool_default


class OutputArguments(FunctionCheck):
    def findings(self):
        return [alarm(f"çıktı argümanı '{name}' değiştiriliyor (Bl.3 · Output Arguments; F2)")
                for name in sorted(self._function.mutated_parameters())]


class CommandQuery(FunctionCheck):
    def findings(self):
        function = self._function
        if function.is_special() or not self._changes_state() or not function.returns_value():
            return []
        return [alarm("hem durum değiştiriyor hem değer döndürüyor (Bl.3 · Command Query Separation)")]

    def _changes_state(self):
        assigns_self = any(is_self_attribute(t) for node in self._function.own_nodes() for t in assignment_targets(node))
        return assigns_self or bool(self._function.mutated_parameters())


class ReturnsNone(FunctionCheck):
    def findings(self):
        return [alarm("None döndürüyor (Bl.7 · Don't Return Null)")] if self._may_return_none() else []

    def _may_return_none(self):
        """Açık `return None`, değer döndüren fonksiyonda çıplak `return` ya da `Optional` dönüş türü."""
        returns = self._function.returns()
        bare_beside_value = self._function.returns_value() and any(node.value is None for node in returns)
        return any(is_none(node.value) for node in returns) or bare_beside_value or self._optional_annotation()

    def _optional_annotation(self):
        annotation = self._function.return_annotation()
        text = ast.unparse(annotation) if annotation is not None else "None"
        return text != "None" and ("None" in text or "Optional" in text)


class SwallowedExceptions(FunctionCheck):
    def findings(self):
        return [alarm("istisna yutuluyor: except gövdesi boş (Bl.7; G4)") for node in self._function.own_nodes()
                if isinstance(node, ast.ExceptHandler) and is_empty_body(node.body)]


class MagicNumbers(FunctionCheck):
    def findings(self):
        numbers = sorted({node.value for node in self._function.own_nodes() if self._is_magic_number(node)})
        return [look(f"adsız sayılar {numbers} (Bl.2 · Use Searchable Names; G25)")] if numbers else []

    @staticmethod
    def _is_magic_number(node):
        is_number = isinstance(node, ast.Constant) and type(node.value) in (int, float)
        return is_number and node.value not in SELF_EVIDENT_NUMBERS


FUNCTION_CHECKS = (FunctionSize, NestingDepth, ArgumentCount, FlagArguments, OutputArguments, CommandQuery,
                   ReturnsNone, SwallowedExceptions, MagicNumbers)
