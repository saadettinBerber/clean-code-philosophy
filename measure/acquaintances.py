"""Fonksiyonun tanışları: yerel adların kökeni satır sırasıyla izlenir. "Talk to friends, not to strangers"
(Bl.6 · The Law of Demeter). Ad argümanla gelir ya da fonksiyon onu kurar: dosttur. Başka birinin döndürdüğü nesneye
bağlanırsa yabancıdır; zinciri ara değişkene bölmek onu dost yapmaz (Bl.6 · Train Wrecks).
Bilerek izlenmeyenler: `for` hedefi ve demet açma koleksiyon öğesine erişimdir, veri yapısına Demeter uygulanmaz;
`self.x` alanı dörtlü izinden biridir; iç içe fonksiyonun ve kavramanın (comprehension) adları dışarı sızmaz."""
import ast
from typing import NamedTuple

COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)
STATEMENT_LISTS = ("body", "orelse", "finalbody")


class Binding(NamedTuple):
    """`name`, `value`'nun sonucuna `after` konumunda bağlanır; bağın bloğu `anchor`'ın deyiminden okunur."""
    name: str
    value: ast.AST
    after: tuple
    anchor: ast.AST


class Acquaintances:
    """Bir fonksiyonun yerel adları ve her noktada kime bağlı oldukları."""

    def __init__(self, function, sight):
        self._sight = sight
        self._blocks = Blocks(function.statements())
        self._bindings = sorted(_bindings(function.own_nodes()), key=lambda binding: binding.after)

    def strangers_behind(self, name):
        """Bu kullanıma ulaşabilen yabancı bağlar, en yakından başlayarak. Kullanımı kesin önceleyen bağ aramayı
        keser; başka bir kolda kalan dost bağ kesmez: ad yabancı "olabilir"."""
        if self._blocks.is_bound_by_comprehension(name):
            return []
        return [binding for binding in self._reaching(name) if self._hands_out(binding)]

    def _reaching(self, name):
        """Kullanımdan önce kurulan bağlar, sondan başa; kullanımı kesin önceleyen ilk bağda durulur."""
        position = (name.lineno, name.col_offset)
        earlier = [bound for bound in reversed(self._bindings) if bound.name == name.id and bound.after <= position]
        around = self._blocks.around(name)
        cuts = [index for index, binding in enumerate(earlier) if self._blocks.block_of(binding.anchor) in around]
        return earlier[:cuts[0] + 1] if cuts else earlier

    def _hands_out(self, binding):
        """Bağlanan değer yabancı mı: kuruluş olmayan çağrının sonucu ya da yabancıya bağlı bir ad."""
        if isinstance(binding.value, ast.Name):
            return bool(self.strangers_behind(binding.value))
        return self._sight.hands_out(binding.value)


class Blocks:
    """Fonksiyonun deyim listeleri: her düğümün hangi listede durduğu ve hangi listelerin içinde kaldığı."""

    def __init__(self, statements):
        self._parents = {}
        self._link(ast.Module(body=statements, type_ignores=[]))

    def block_of(self, node):
        statement = self._statement_of(node)
        owner = self._parents[statement]
        return id(owner), next(field for field in STATEMENT_LISTS if statement in getattr(owner, field, []))

    def around(self, node):
        """Kullanımı saran deyim listeleri; bunlardan birindeki bağ, kullanımdan önce kesin çalışmıştır."""
        return [self.block_of(ancestor) for ancestor in self._ancestors(node) if isinstance(ancestor, ast.stmt)]

    def is_bound_by_comprehension(self, name):
        return any(name.id in _comprehension_names(node) for node in self._ancestors(name)
                   if isinstance(node, COMPREHENSIONS))

    def _statement_of(self, node):
        return next(ancestor for ancestor in self._ancestors(node) if isinstance(ancestor, ast.stmt))

    def _ancestors(self, node):
        """Düğümün kendisi ve sarmalayanları, içten dışa."""
        yield node
        while node in self._parents:
            node = self._parents[node]
            yield node

    def _link(self, parent):
        for child in ast.iter_child_nodes(parent):
            self._parents[child] = parent
            self._link(child)


def _bindings(nodes):
    return [Binding(*site) for node in nodes for site in _sites(node)]


def _sites(node):
    """Düğümün kurduğu bağlar: (ad, değer, geçerli olduğu yer, bloğunu veren düğüm)."""
    if isinstance(node, ast.Assign):
        return [_site(pair, node) for target in node.targets for pair in _pairs(target, node.value)]
    if isinstance(node, (ast.AnnAssign, ast.NamedExpr)) and node.value is not None:
        return [_site(pair, node) for pair in _pairs(node.target, node.value)]
    if isinstance(node, (ast.For, ast.AsyncFor)):
        return [_site(pair, node.target) for pair in _pairs(node.target, _element_of(node.iter))]
    if isinstance(node, ast.withitem) and node.optional_vars is not None:
        return [_site(pair, node.optional_vars) for pair in _pairs(node.optional_vars, node.context_expr)]
    return _caught(node) if isinstance(node, ast.ExceptHandler) and node.name else []


def _site(pair, end):
    """(ad düğümü, değer) çifti, bağın `end` düğümünün bitiminde geçerli olduğu bir bağ yerine döner."""
    name, value = pair
    return name.id, value, (end.end_lineno, end.end_col_offset), name


def _pairs(target, value):
    """Hedefteki her ad, kendisine düşen değerle. Açık demet öğe öğe dağılır; başka her değer bir koleksiyondur
    ve açılan öğe `değer[i]` gibi okunur."""
    if isinstance(target, ast.Name):
        return [(target, value)]
    if not isinstance(target, (ast.Tuple, ast.List)):
        return []
    literal = isinstance(value, (ast.Tuple, ast.List)) and len(value.elts) == len(target.elts)
    values = value.elts if literal else [_element_of(value)] * len(target.elts)
    return [pair for inner, part in zip(target.elts, values) for pair in _pairs(inner, part)]


def _element_of(collection):
    return ast.Subscript(value=collection, slice=ast.Constant(0), ctx=ast.Load())


def _caught(handler):
    """Yakalanan istisna, yakalayana verilmiş bir nesnedir: argüman gibi dosttur. Bağ gövdenin başında geçerlidir."""
    first = handler.body[0]
    return [(handler.name, handler, (first.lineno, first.col_offset), first)]


def _comprehension_names(comprehension):
    return {name.id for generator in comprehension.generators for name in ast.walk(generator.target)
            if isinstance(name, ast.Name)}
