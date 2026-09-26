"""Bir çağrı nesneyi fonksiyonun kendisine mi kuruyor? Demeter'in izni: fonksiyon, kendi kurduğu nesnenin
metotlarını çağırabilir (Bl.6 · The Law of Demeter)."""
import ast
import builtins
from collections import defaultdict

from measure.syntax import is_class_name, is_self_attribute, last_name

# `open` tür değildir ama dosya nesnesini kurar; `next`, `max`, `getattr` başkasının tuttuğu nesneyi verir.
BUILT_IN_CONSTRUCTORS = frozenset(name for name, value in vars(builtins).items() if isinstance(value, type)) | {"open"}
# `cls(...)` sınıf metodunda sınıfın kendisini kurar.
CONSTRUCTOR_NAMES = BUILT_IN_CONSTRUCTORS | {"cls"}
# Standart kütüphane kurucuları: her çağrı yeni bir nesne kurar, var olanın içinde gezinmez. Kitabın kendi çözümü
# `ctxt.createScratchFileStream(name)` da nesneye yeni bir nesne kurdurur (Bl.6 · Hiding Structure). `parse_args`
# davranışsız bir veri yapısı (`Namespace`) kurar; veri yapısına Demeter uygulanmaz (Bl.6 · Train Wrecks).
# `redirect_stdout` ve `redirect_stderr` küçük harfle yazılmış sınıflardır; `with … as` hedefi verilen akışın kendisidir.
# Başka nesnelerde de sık görülen belirsiz adlar (`compile`, `sub`, `match`) yalnız modülüyle nitelenmiş hâliyle girer.
STANDARD_LIBRARY_CONSTRUCTORS = frozenset({"re.compile", "add_subparsers", "add_parser", "add_argument_group",
                                           "add_mutually_exclusive_group", "parse_args", "redirect_stdout",
                                           "redirect_stderr"})


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

    def factories(self):
        return frozenset(function for named in self._by_name.values() for function in named if self.is_factory(function))

    def is_factory(self, function):
        return self.seen_from(function).is_factory()

    def seen_from(self, caller):
        return Sight(self, caller)

    def named(self, name):
        return self._by_name.get(name, [])

    def are_factories(self, functions):
        return bool(functions) and all(function in self._factories for function in functions)


class Sight:
    """Bir fonksiyonun gözünden kuruluşlar. Ad, Python'un çözdüğü gibi önce çağıranın yanında aranır: çıplak ad
    kendi modülünde, `self.ad` kendi sınıfında. Orada tanımlı değilse bütün kaynaklardaki aynı adlılara bakılır."""

    def __init__(self, constructions, caller):
        self._constructions = constructions
        self._caller = caller

    def creates(self, node):
        return isinstance(node, ast.Call) and (_names_a_class(node.func) or _is_standard_constructor(node.func)
                                               or self._constructions.are_factories(self._reachable(node.func)))

    def hands_out(self, node):
        """Kuruluş olmayan çağrının sonucu başka birinin verdiği nesnedir: yabancıdır (Bl.6 · The Law of Demeter)."""
        return isinstance(node, ast.Call) and not self.creates(node)

    def is_factory(self):
        """Her dönüşü bu fonksiyonda kurulan bir nesne olan fonksiyon."""
        built = self._built_names()
        values = [node.value for node in self._caller.returns()]
        return bool(values) and all(self._is_built(value, built) for value in values)

    def _reachable(self, callee):
        named = self._constructions.named(last_name(callee))
        home = self._home_of(callee)
        return [function for function in named if function.home() == home] or named

    def _home_of(self, callee):
        if isinstance(callee, ast.Name):
            return self._caller.module_home()
        return self._caller.home() if is_self_attribute(callee) else ()

    def _is_built(self, value, built):
        """Kurulan nesne; koşullu ifadede iki kol da kurulmuş olmalı."""
        if isinstance(value, ast.IfExp):
            return self._is_built(value.body, built) and self._is_built(value.orelse, built)
        return self.creates(value) or _is_one_of(value, built)

    def _built_names(self):
        return {target.id for node in self._caller.own_nodes() if isinstance(node, ast.Assign) and self.creates(node.value)
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
