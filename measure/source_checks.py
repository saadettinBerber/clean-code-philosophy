"""Kaynak dosya ölçümleri: yorumlar (Bl.4) ve sınıf olmak isteyen fonksiyon kümeleri (Bl.2, Bl.10, G23)."""
import ast
import re
from abc import ABC
from collections import defaultdict
from collections.abc import Sequence

from measure.findings import Note, alarm
from measure.function import Function
from measure.source_check import SourceCheck
from measure.source_file import SourceFile
from measure.syntax import FUNCTION_NODES, is_string_literal

TODO = re.compile(r"\b(TODO|FIXME|XXX)\b")
TODO_ALARM = "TODO: yapılabiliyorsa kapat; kalıyorsa nedenini ve kodun ne olacağını söylesin (Bl.4 · TODO Comments)"
TRIVIAL_EXPRESSIONS = (ast.Name, ast.Constant, ast.Attribute)
MIN_CARRIERS = 3
PROCEDURAL_DECLARATION = "Prosedürel (Bl.6):"


class CommentCheck(SourceCheck, ABC):
    """Kaynağın yorumlarının ölçümü."""

    def __init__(self, source: SourceFile) -> None:
        super().__init__(source)
        self._comments = source.comments()


class CommentedOutCode(CommentCheck):
    def notes(self) -> list[Note]:
        return [Note(block.location, alarm("yoruma alınmış kod (Bl.4 · Commented-Out Code; C5)"))
                for block in self._comments.blocks() if self._is_code(block.text)]

    @staticmethod
    def _is_code(block: str) -> bool:
        try:
            return any(not _is_trivial(statement) for statement in ast.parse(block).body)
        except SyntaxError:
            return False


def _is_trivial(statement: ast.stmt) -> bool:
    return isinstance(statement, ast.Expr) and isinstance(statement.value, TRIVIAL_EXPRESSIONS)


class Todos(CommentCheck):
    """Her TODO bir alarmdır: düzenli taranır, yapılabilen kapatılır."""

    def notes(self) -> list[Note]:
        return [Note(comment.location, alarm(TODO_ALARM))
                for comment in self._comments.all() if TODO.search(comment.text)]


class CarriedArguments(SourceCheck):
    """Aynı parametre modülde birçok fonksiyonda: elden ele taşınan değişken, sınıf olmak istiyor.
    Belge dizgisi prosedürel seçimi Bl.6 gerekçesiyle ilan eden modül ölçülmez."""

    def notes(self) -> list[Note]:
        if PROCEDURAL_DECLARATION in self._source.docstring():
            return []
        return [functions[0].note(alarm(self._message(name, functions)))
                for name, functions in sorted(self._carriers().items()) if len(functions) >= MIN_CARRIERS]

    def _carriers(self) -> dict[str, list[Function]]:
        carriers: defaultdict[str, list[Function]] = defaultdict(list)
        for function in self._source.top_level_functions():
            for name in function.parameter_names():
                carriers[name].append(function)
        return carriers

    @staticmethod
    def _message(name: str, functions: Sequence[Function]) -> str:
        return (f"'{name}' {len(functions)} fonksiyonda elden ele taşınıyor; sınıf olmak istiyor "
                "(Bl.10 · Cohesion; Bl.2 · Add Meaningful Context)")


class DispatchTables(SourceCheck):
    """Dizge anahtarlı, değerleri modülün fonksiyonları olan sözlük: sözlükle yazılmış tür dallanması."""

    def notes(self) -> list[Note]:
        return [Note(self._source.location(node.lineno, node.targets[0].id), alarm(
                    "sözlükle tür dağıtımı; davranış tür başına sınıfta, seçim fabrikada durur (Bl.3 · Switch Statements; G23)"))
                for node in self._source.top_level_nodes() if self._is_dispatch_table(node)]

    def _is_dispatch_table(self, node: ast.stmt) -> bool:
        is_table = isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict) and isinstance(node.targets[0], ast.Name)
        return is_table and bool(node.value.keys) and self._maps_types_to_functions(node.value)

    def _maps_types_to_functions(self, table: ast.Dict) -> bool:
        functions = {node.name for node in self._source.top_level_nodes() if isinstance(node, FUNCTION_NODES)}
        keys_are_types = all(key is not None and is_string_literal(key) for key in table.keys)
        return keys_are_types and all(isinstance(value, ast.Name) and value.id in functions for value in table.values)


SOURCE_CHECKS = (CommentedOutCode, Todos, CarriedArguments, DispatchTables)
