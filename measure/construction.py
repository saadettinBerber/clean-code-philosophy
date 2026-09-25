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
    türleri (`list(...)`, `super()`), `open(...)`, sınıf metodunda `cls(...)` ve kaynağın kendi fabrikaları (`_kart(...)`, `self._yapici()`)."""

    def __init__(self, factories=frozenset()):
        self._factories = factories

    @classmethod
    def of(cls, source):
        """Fabrikayı çağıran fonksiyon da fabrikadır; liste yeni fabrika çıkmayana dek genişler."""
        factories, previous = frozenset(), None
        while factories != previous:
            previous, factories = factories, cls(factories).factories_in(source)
        return cls(factories)

    def creates(self, node):
        return isinstance(node, ast.Call) and (ast.unparse(node.func) in self._factories or _names_a_class(node.func))

    def factories_in(self, source):
        return frozenset(function.reference() for function in source.functions() if self._is_factory(function))

    def _is_factory(self, function):
        """Her dönüşü bu fonksiyonda kurulan bir nesne olan fonksiyon."""
        built = self._built_names(function)
        values = [node.value for node in function.returns()]
        return bool(values) and all(self._is_built(value, built) for value in values)

    def _is_built(self, value, built):
        """Kurulan nesne; koşullu ifadede iki kol da kurulmuş olmalı."""
        if isinstance(value, ast.IfExp):
            return self._is_built(value.body, built) and self._is_built(value.orelse, built)
        return self.creates(value) or _is_one_of(value, built)

    def _built_names(self, function):
        return {target.id for node in function.own_nodes() if isinstance(node, ast.Assign) and self.creates(node.value)
                for target in node.targets if isinstance(target, ast.Name)}


def _names_a_class(callee):
    if isinstance(callee, ast.Attribute):
        return is_class_name(callee.attr) or isinstance(callee.value, ast.Name) and is_class_name(callee.value.id)
    return isinstance(callee, ast.Name) and (callee.id in CONSTRUCTOR_NAMES or is_class_name(callee.id))


def _is_one_of(node, names):
    return isinstance(node, ast.Name) and node.id in names
