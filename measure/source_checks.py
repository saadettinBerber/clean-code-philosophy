"""Kaynak dosya ölçümleri: yorumlar (Bl.4) ve sınıf olmak isteyen fonksiyon kümeleri (Bl.2, Bl.10, G23)."""
import ast
import re
from abc import ABC
from collections import defaultdict

from measure.demeter import TrainWrecks
from measure.findings import Note, alarm
from measure.source_check import SourceCheck
from measure.syntax import FUNCTION_NODES, is_string_literal

TODO = re.compile(r"\b(TODO|FIXME|XXX)\b")
TICKET = re.compile(r"\b[A-Z][A-Z0-9]+-\d+\b|#\d+")
TRIVIAL_EXPRESSIONS = (ast.Name, ast.Constant, ast.Attribute)
MIN_CARRIERS = 3
PROCEDURAL_DECLARATION = "Prosedürel (Bl.6):"


class CommentCheck(SourceCheck, ABC):
    """Kaynağın yorumlarının ölçümü."""

    def __init__(self, source):
        super().__init__(source)
        self._comments = source.comments()


class CommentedOutCode(CommentCheck):
    def notes(self):
        return [Note(block.location, alarm("yoruma alınmış kod (Bl.4 · Commented-Out Code; C5)"))
                for block in self._comments.blocks() if self._is_code(block.text)]

    @staticmethod
    def _is_code(block):
        try:
            return any(not _is_trivial(statement) for statement in ast.parse(block).body)
        except SyntaxError:
            return False


def _is_trivial(statement):
    return isinstance(statement, ast.Expr) and isinstance(statement.value, TRIVIAL_EXPRESSIONS)


class TodosWithoutTicket(CommentCheck):
    def notes(self):
        return [Note(comment.location, alarm("bilet numarasız TODO (Bl.4 · TODO Comments)"))
                for comment in self._comments.all() if self._lacks_ticket(comment.text)]

    @staticmethod
    def _lacks_ticket(text):
        return bool(TODO.search(text)) and not TICKET.search(text)


class CarriedArguments(SourceCheck):
    """Aynı parametre modülde birçok fonksiyonda: elden ele taşınan değişken, sınıf olmak istiyor.
    Belge dizgisi prosedürel seçimi Bl.6 gerekçesiyle ilan eden modül ölçülmez."""

    def notes(self):
        if PROCEDURAL_DECLARATION in self._source.docstring():
            return []
        return [functions[0].note(alarm(self._message(name, functions)))
                for name, functions in sorted(self._carriers().items()) if len(functions) >= MIN_CARRIERS]

    def _carriers(self):
        carriers = defaultdict(list)
        for function in self._source.top_level_functions():
            for name in function.parameter_names():
                carriers[name].append(function)
        return carriers

    @staticmethod
    def _message(name, functions):
        return (f"'{name}' {len(functions)} fonksiyonda elden ele taşınıyor; sınıf olmak istiyor "
                "(Bl.10 · Cohesion; Bl.2 · Add Meaningful Context)")


class DispatchTables(SourceCheck):
    """Dizge anahtarlı, değerleri modülün fonksiyonları olan sözlük: sözlükle yazılmış tür dallanması."""

    def notes(self):
        return [Note(self._source.location(node.lineno, node.targets[0].id), alarm(
                    "sözlükle tür dağıtımı; davranış tür başına sınıfta, seçim fabrikada durur (Bl.3 · Switch Statements; G23)"))
                for node in self._source.top_level_nodes() if self._is_dispatch_table(node)]

    def _is_dispatch_table(self, node):
        is_table = isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict) and isinstance(node.targets[0], ast.Name)
        return is_table and bool(node.value.keys) and self._maps_types_to_functions(node.value)

    def _maps_types_to_functions(self, table):
        functions = {node.name for node in self._source.top_level_nodes() if isinstance(node, FUNCTION_NODES)}
        keys_are_types = all(key is not None and is_string_literal(key) for key in table.keys)
        return keys_are_types and all(isinstance(value, ast.Name) and value.id in functions for value in table.values)


SOURCE_CHECKS = (CommentedOutCode, TodosWithoutTicket, CarriedArguments, DispatchTables, TrainWrecks)
