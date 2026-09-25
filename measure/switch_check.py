"""Tek switch kuralı (Bl.3 · Switch Statements; G23): aynı ayırıcıya dallanan birden fazla fonksiyon.

Ayırıcı iki biçimde tanınır:
- alan: bir fonksiyonda aynı alan ya da anahtar en az iki kez dizge sabitiyle karşılaştırılıyor
  (`b.kind == "a"` … `elif b.kind == "b"`), ya da `match` o alanın üstünde kuruluyor;
- tür: bir fonksiyonun `if`/`elif` dallarında en az iki kez `isinstance` soruluyor.
Alan ayırıcısı iki fonksiyonda, tür ayırıcısı iki türü paylaşan iki fonksiyonda geçerse alarm verilir.
"""
import ast
from collections import Counter
from itertools import combinations

from measure.findings import alarm
from measure.syntax import is_string_literal

MIN_BRANCHES = 2
MIN_SHARED_TYPES = 2
ISINSTANCE_ARGUMENTS = 2


class Switches:
    """Tek fonksiyonun tür dallanmaları."""

    def __init__(self, function):
        self._nodes = function.all_nodes()

    def fields(self):
        keys = Counter(key for key in (self._compared_field(node.test) for node in self._ifs()) if key)
        matched = {self._field_key(node.subject) for node in self._nodes if isinstance(node, ast.Match)} - {""}
        return sorted({key for key, count in keys.items() if count >= MIN_BRANCHES} | matched)

    def types(self):
        calls = [call for node in self._ifs() for call in ast.walk(node.test) if self._is_isinstance(call)]
        return frozenset(ast.unparse(name) for call in calls for name in self._named_types(call)) \
            if len(calls) >= MIN_BRANCHES else frozenset()

    def _ifs(self):
        return [node for node in self._nodes if isinstance(node, ast.If)]

    def _compared_field(self, test):
        is_string_comparison = isinstance(test, ast.Compare) and all(is_string_literal(c) for c in test.comparators)
        return self._field_key(test.left) if is_string_comparison else ""

    @staticmethod
    def _field_key(node):
        if isinstance(node, ast.Attribute):
            return node.attr
        return node.slice.value if isinstance(node, ast.Subscript) and is_string_literal(node.slice) else ""

    @staticmethod
    def _is_isinstance(node):
        is_call = isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        return is_call and node.func.id == "isinstance" and len(node.args) == ISINSTANCE_ARGUMENTS

    @staticmethod
    def _named_types(call):
        types = call.args[1]
        return types.elts if isinstance(types, ast.Tuple) else [types]


class OneSwitch:
    """Bütün kaynakların fonksiyonları üzerinde; ayırıcısı paylaşılan her fonksiyona not düşer."""

    def __init__(self, functions):
        self._functions = functions

    def notes(self):
        return self._shared_fields() + self._shared_types()

    def _shared_fields(self):
        fields = [(function, key) for function in self._functions for key in Switches(function).fields()]
        places = Counter(key for _, key in fields)
        return [self._note(function, f"'{key}' alanına dallanma {places[key]} fonksiyonda")
                for function, key in fields if places[key] > 1]

    def _shared_types(self):
        types = [(function, Switches(function).types()) for function in self._functions]
        types = [(function, found) for function, found in types if found]
        shared = {id(function) for (first, a), (second, b) in combinations(types, 2)
                  if len(a & b) >= MIN_SHARED_TYPES for function in (first, second)}
        return [self._note(function, f"{sorted(found)} türlerine dallanma başka fonksiyonda da var")
                for function, found in types if id(function) in shared]

    @staticmethod
    def _note(function, message):
        return function.note(alarm(f"{message}; tek switch fabrikada durur (Bl.3 · Switch Statements; G23)"))
