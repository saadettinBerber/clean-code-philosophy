"""Bir çağrı nesneyi fonksiyonun kendisine mi kuruyor? Demeter'in izni: fonksiyon, kendi kurduğu nesnenin
metotlarını çağırabilir (Bl.6 · The Law of Demeter)."""
import ast

from measure.syntax import is_class_name


class Constructions:
    """Kurucu sayılan çağrılar: `Sınıf(...)`, `Sınıf.fabrika(...)` ve `super()`."""

    def creates(self, node):
        return isinstance(node, ast.Call) and self._is_constructor(node.func)

    @staticmethod
    def _is_constructor(callee):
        if isinstance(callee, ast.Attribute):
            return isinstance(callee.value, ast.Name) and is_class_name(callee.value.id)
        return isinstance(callee, ast.Name) and (callee.id == "super" or is_class_name(callee.id))
