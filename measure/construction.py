"""Bir çağrı nesneyi fonksiyonun kendisine mi kuruyor? Demeter'in izni: fonksiyon, kendi kurduğu nesnenin
metotlarını çağırabilir (Bl.6 · The Law of Demeter)."""
import ast
import builtins
from collections import defaultdict

from measure.syntax import is_class_name, last_name

# `open` tür değildir ama dosya nesnesini kurar; `next`, `max`, `getattr` başkasının tuttuğu nesneyi verir.
BUILT_IN_CONSTRUCTORS = frozenset(name for name, value in vars(builtins).items() if isinstance(value, type)) | {"open"}
# `cls(...)` sınıf metodunda sınıfın kendisini kurar.
CONSTRUCTOR_NAMES = BUILT_IN_CONSTRUCTORS | {"cls"}
# Standart kütüphane kurucuları: her çağrı yeni bir nesne kurar, var olanın içinde gezinmez. Kitabın kendi çözümü
# `ctxt.createScratchFileStream(name)` da nesneye yeni bir nesne kurdurur (Bl.6 · Hiding Structure). `parse_args`
# davranışsız bir veri yapısı (`Namespace`) kurar; veri yapısına Demeter uygulanmaz (Bl.6 · Train Wrecks).
# Başka nesnelerde de sık görülen belirsiz adlar (`compile`, `sub`, `match`) yalnız modülüyle nitelenmiş hâliyle girer.
STANDARD_LIBRARY_CONSTRUCTORS = frozenset({"re.compile", "add_subparsers", "add_parser", "add_argument_group",
                                           "add_mutually_exclusive_group", "parse_args"})


class Constructions:
    """Kurucu sayılan çağrılar: `Sınıf(...)`, `modül.Sınıf(...)`, `Sınıf.fabrika(...)`, Python'un yerleşik
    türleri (`list(...)`, `super()`), `open(...)`, sınıf metodunda `cls(...)`, standart kütüphane kurucuları ve ölçülen
    kaynakların fabrikaları. Tür bilgisi yoktur, fabrika ada göre çözülür: o adı taşıyan bütün fonksiyonlar fabrikaysa
    çağrı kuruluştur; biri bile değilse ad belirsizdir ve kuruluş sayılmaz, alarm insanın okumasına kalır."""

    def __init__(self, functions=(), factories=frozenset()):
        self._by_name = _by_name(functions)
        self._factories = factories

    @classmethod
    def among(cls, functions):
        """Fabrikayı çağıran fonksiyon da fabrikadır; küme yeni fabrika çıkmayana dek genişler."""
        factories, previous = frozenset(), None
        while factories != previous:
            previous, factories = factories, cls(functions, factories).factories()
        return cls(functions, factories)

    def creates(self, node):
        return isinstance(node, ast.Call) and (_names_a_class(node.func) or _is_standard_constructor(node.func)
                                               or self._calls_a_factory(node.func))

    def factories(self):
        return frozenset(function for named in self._by_name.values() for function in named if self.is_factory(function))

    def _calls_a_factory(self, callee):
        named = self._by_name.get(last_name(callee), [])
        return bool(named) and all(function in self._factories for function in named)

    def is_factory(self, function):
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


def _by_name(functions):
    by_name = defaultdict(list)
    for function in functions:
        by_name[function.name()].append(function)
    return by_name


def _is_standard_constructor(callee):
    return ast.unparse(callee) in STANDARD_LIBRARY_CONSTRUCTORS or last_name(callee) in STANDARD_LIBRARY_CONSTRUCTORS


def _names_a_class(callee):
    if isinstance(callee, ast.Attribute):
        return is_class_name(callee.attr) or isinstance(callee.value, ast.Name) and is_class_name(callee.value.id)
    return isinstance(callee, ast.Name) and (callee.id in CONSTRUCTOR_NAMES or is_class_name(callee.id))


def _is_one_of(node, names):
    return isinstance(node, ast.Name) and node.id in names
