"""Bir çağrı nesneyi fonksiyonun kendisine mi kuruyor? Demeter'in izni: fonksiyon, kendi kurduğu nesnenin
metotlarını çağırabilir (Bl.6 · The Law of Demeter)."""
import ast
import builtins

from measure.syntax import is_class_name

# `open` tür değildir ama dosya nesnesini kurar; `next`, `max`, `getattr` başkasının tuttuğu nesneyi verir.
BUILT_IN_CONSTRUCTORS = frozenset(name for name, value in vars(builtins).items() if isinstance(value, type)) | {"open"}
# `cls(...)` sınıf metodunda sınıfın kendisini kurar.
CONSTRUCTOR_NAMES = BUILT_IN_CONSTRUCTORS | {"cls"}


class Constructions:
    """Kurucu sayılan çağrılar: `Sınıf(...)`, `modül.Sınıf(...)`, `Sınıf.fabrika(...)`, Python'un yerleşik
    türleri (`list(...)`, `super()`), `open(...)` ve sınıf metodunda `cls(...)`."""

    def creates(self, node):
        return isinstance(node, ast.Call) and self._is_constructor(node.func)

    @staticmethod
    def _is_constructor(callee):
        if isinstance(callee, ast.Attribute):
            return is_class_name(callee.attr) or isinstance(callee.value, ast.Name) and is_class_name(callee.value.id)
        return isinstance(callee, ast.Name) and (callee.id in CONSTRUCTOR_NAMES or is_class_name(callee.id))
