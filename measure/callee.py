"""Çağrılan ifade ve onun hakkında sözdiziminden okunabilenler: bir sınıfı mı adlandırıyor, standart kütüphanenin
nesne kuran bir çağrısı mı, bir tablodan mı seçiliyor, adı önce nerede aranır."""
from __future__ import annotations

import ast
import builtins
from typing import TYPE_CHECKING

from measure.scope import Home
from measure.syntax import is_class_name, is_self_attribute, last_name

if TYPE_CHECKING:
    from measure.function import Function

# `open` tür değildir ama dosya nesnesini kurar; `next`, `max`, `getattr` başkasının tuttuğu nesneyi verir.
BUILT_IN_CONSTRUCTORS = frozenset(name for name, value in vars(builtins).items() if isinstance(value, type)) | {"open"}
# `cls(...)` sınıf metodunda sınıfın kendisini kurar.
CONSTRUCTOR_NAMES = BUILT_IN_CONSTRUCTORS | {"cls"}
# Standart kütüphane kurucuları: her çağrı yeni bir nesne kurar, var olanın içinde gezinmez. Kitabın kendi çözümü
# `ctxt.createScratchFileStream(name)` da nesneye yeni bir nesne kurdurur (Bl.6 · Hiding Structure). `parse_args`
# davranışsız bir veri yapısı (`Namespace`) kurar; veri yapısına Demeter uygulanmaz (Bl.6 · Train Wrecks).
# `redirect_stdout` ve `redirect_stderr` küçük harfle yazılmış sınıflardır; `with … as` hedefi verilen akıştır.
# `urlopen` her çağrıda çağırana ait yeni bir cevap nesnesi kurar; `open`'ın ağdaki karşılığıdır.
# Başka nesnelerde de sık görülen belirsiz adlar (`compile`, `sub`, `match`) yalnız modülüyle nitelenmiş hâliyle girer.
STANDARD_LIBRARY_CONSTRUCTORS = frozenset({"re.compile", "add_subparsers", "add_parser", "add_argument_group",
                                           "add_mutually_exclusive_group", "parse_args", "redirect_stdout",
                                           "redirect_stderr", "urlopen"})


class Callee:
    """Çağrılan ifade: `Sınıf`, `modül.fonksiyon`, `nesne.metot`, `self.metot`, `TABLO[tür]` ya da
    `TABLO.get(tür, Varsayılan)`."""

    def __init__(self, node: ast.expr) -> None:
        self._node = node

    def name(self) -> str:
        return last_name(self._node)

    def names_a_class(self) -> bool:
        node = self._node
        if isinstance(node, ast.Attribute):
            return is_class_name(node.attr) or isinstance(node.value, ast.Name) and is_class_name(node.value.id)
        return isinstance(node, ast.Name) and (node.id in CONSTRUCTOR_NAMES or is_class_name(node.id))

    def is_standard_constructor(self) -> bool:
        return ast.unparse(self._node) in STANDARD_LIBRARY_CONSTRUCTORS or self.name() in STANDARD_LIBRARY_CONSTRUCTORS

    def home_seen_from(self, caller: Function) -> Home:
        """Adın önce arandığı yer: çıplak ad çağıranın modülünde, `self.ad` çağıranın sınıfında; başkası yok."""
        if isinstance(self._node, ast.Name):
            return caller.module_home()
        return caller.home() if is_self_attribute(self._node) else ()

    def table_choice(self) -> tuple[str, list[ast.expr]]:
        """Tablodan seçim mi: (tablonun adı, varsayılanlar); değilse ("", [])."""
        node = self._node
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name):
            return node.value.id, []
        is_get = isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get"
        if is_get and isinstance(node.func.value, ast.Name) and len(node.args) == 2:
            return node.func.value.id, node.args[1:]
        return "", []
