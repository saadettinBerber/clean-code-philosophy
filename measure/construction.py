"""Bir çağrı nesneyi fonksiyonun kendisine mi kuruyor? Demeter'in izni: fonksiyon, kendi kurduğu nesnenin
metotlarını çağırabilir (Bl.6 · The Law of Demeter)."""
import ast
from collections import defaultdict
from typing import NamedTuple

from measure.callee import Callee
from measure.syntax import is_name

class Known(NamedTuple):
    """Ölçülen kaynaklarda bilinenler: fonksiyonlar ve modül düzeyindeki sınıf tabloları (`(modül evi, ad)`)."""
    functions: tuple = ()
    tables: frozenset = frozenset()


class Constructions:
    """Kurucu sayılan çağrılar: `Sınıf(...)`, `modül.Sınıf(...)`, `Sınıf.fabrika(...)`, Python'un yerleşik
    türleri (`list(...)`, `super()`), `open(...)`, sınıf metodunda `cls(...)`, standart kütüphane kurucuları, tablodan
    seçilen sınıfla kurma ve ölçülen kaynakların fabrikaları. Tür bilgisi yoktur, fabrika ada göre çözülür: o adı
    taşıyan bütün fonksiyonlar fabrikaysa çağrı kuruluştur; biri bile değilse ad belirsizdir ve kuruluş sayılmaz,
    alarm insanın okumasına kalır."""

    def __init__(self, known=Known(), factories=frozenset()):
        self._by_name = _by_name(known.functions)
        self._tables = known.tables
        self._factories = factories

    @classmethod
    def among(cls, sources):
        """Fabrikayı çağıran fonksiyon da fabrikadır; küme yeni fabrika çıkmayana dek genişler."""
        known = Known(tuple(function for source in sources for function in source.functions()),
                      frozenset(table for source in sources for table in _class_tables_of(source)))
        factories, previous = frozenset(), None
        while factories != previous:
            previous, factories = factories, cls(known, factories).factories()
        return cls(known, factories)

    def factories(self):
        functions = [function for named in self._by_name.values() for function in named]
        return frozenset(function for function in functions if self.is_factory(function))

    def is_factory(self, function):
        return self.seen_from(function).is_factory()

    def seen_from(self, caller):
        return Sight(self, caller)

    def named(self, name):
        return self._by_name.get(name, [])

    def are_factories(self, functions):
        return bool(functions) and all(function in self._factories for function in functions)

    def has_table(self, place):
        """`(modül evi, ad)` o modülde yalnız sınıflardan oluşan bir tabloyu mu adlandırıyor?"""
        return place in self._tables


class Sight:
    """Bir fonksiyonun gözünden kuruluşlar. Ad, Python'un çözdüğü gibi önce çağıranın yanında aranır: çıplak ad
    kendi modülünde, `self.ad` kendi sınıfında. Orada tanımlı değilse bütün kaynaklardaki aynı adlılara bakılır."""

    def __init__(self, constructions, caller):
        self._constructions = constructions
        self._caller = caller

    def creates(self, node):
        if not isinstance(node, ast.Call):
            return False
        callee = Callee(node.func)
        return (callee.names_a_class() or callee.is_standard_constructor()
                or self._constructions.are_factories(self._reachable(callee)) or self._chooses_a_class(callee))

    def hands_out(self, node):
        """Kuruluş olmayan çağrının sonucu başka birinin verdiği nesnedir: yabancıdır (Bl.6 · The Law of Demeter)."""
        return isinstance(node, ast.Call) and not self.creates(node)

    def is_factory(self):
        """Çağırana verdiği her değer bu fonksiyonda kurulan bir nesne olan fonksiyon (dönüş ya da bağlam `yield`i)."""
        built = self._built_names()
        values = self._caller.handed_out()
        return bool(values) and all(self._is_built(value, built) for value in values)

    def _chooses_a_class(self, callee):
        """Tablodan seçilen sınıfla kurma: `SINIFLAR[tür](veri)` ya da `SINIFLAR.get(tür, Varsayılan)(veri)`.
        Tek switch fabrikanın dibinde durur ve polimorfik nesne kurar (Bl.3 · Switch Statements)."""
        table, defaults = callee.table_choice()
        classes_by_default = all(Callee(default).names_a_class() for default in defaults)
        return bool(table) and classes_by_default and self._is_class_table(table)

    def _is_class_table(self, name):
        """Ad önce fonksiyonun içinde aranır, orada bağlanmamışsa kendi modülünde (Python'un ad çözümü)."""
        local = _assigned_values(self._caller.own_nodes(), name)
        if local:
            return all(is_class_table(value) for value in local)
        return self._constructions.has_table((self._caller.module_home(), name))

    def _reachable(self, callee):
        named = self._constructions.named(callee.name())
        home = callee.home_seen_from(self._caller)
        return [function for function in named if function.home() == home] or named

    def _is_built(self, value, built):
        """Kurulan nesne; koşullu ifadede iki kol da kurulmuş olmalı."""
        if isinstance(value, ast.IfExp):
            return self._is_built(value.body, built) and self._is_built(value.orelse, built)
        return self.creates(value) or _is_one_of(value, built)

    def _built_names(self):
        assignments = [node for node in self._caller.own_nodes() if isinstance(node, ast.Assign)]
        return {target.id for node in assignments if self.creates(node.value)
                for target in node.targets if isinstance(target, ast.Name)}


def is_class_table(value):
    """Değerlerinin hepsi sınıf olan sözlük: sözlük yazımı ya da sınıf listesi üzerinde sözlük kavraması."""
    if isinstance(value, ast.Dict):
        return bool(value.values) and all(Callee(item).names_a_class() for item in value.values)
    return isinstance(value, ast.DictComp) and _comprehends_classes(value)


def _comprehends_classes(comprehension):
    """`{sınıf.KIND: sınıf for sınıf in (A, B)}`: değer, sınıf listesinin öğesidir."""
    [generator] = comprehension.generators or [None]
    listed = isinstance(getattr(generator, "iter", None), (ast.Tuple, ast.List))
    is_element = listed and isinstance(generator.target, ast.Name) and is_name(comprehension.value, generator.target.id)
    return is_element and all(Callee(item).names_a_class() for item in generator.iter.elts)


def _class_tables_of(source):
    nodes = source.top_level_nodes()
    names = {target.id for node in nodes if isinstance(node, ast.Assign) for target in node.targets
             if isinstance(target, ast.Name)}
    return [(source.module_home(), name) for name in names
            if all(is_class_table(value) for value in _assigned_values(nodes, name))]


def _assigned_values(nodes, name):
    assignments = [node for node in nodes if isinstance(node, ast.Assign)]
    return [node.value for node in assignments if any(is_name(target, name) for target in node.targets)]


def _by_name(functions):
    by_name = defaultdict(list)
    for function in functions:
        by_name[function.name()].append(function)
    return by_name


def _is_one_of(node, names):
    return isinstance(node, ast.Name) and node.id in names
