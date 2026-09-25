"""Demeter Yasası ölçümü: fonksiyon yalnız yakın arkadaşlarıyla konuşur (Bl.6 · The Law of Demeter).
Kaynağı bilir, çünkü kimin nesne kurduğu kaynağın kendi fabrikalarına da bağlıdır."""
import ast

from measure.construction import Constructions
from measure.findings import alarm
from measure.source_check import SourceCheck

CHAIN_PREVIEW = 60
DATA_STRUCTURE_METHODS = frozenset({"items", "keys", "values", "get", "copy", "count", "index", "split", "rsplit",
                                    "splitlines", "strip", "lstrip", "rstrip", "lower", "upper", "replace", "join",
                                    "startswith", "endswith", "format", "removeprefix", "removesuffix", "encode",
                                    "decode"})


class TrainWrecks(SourceCheck):
    """Dönen nesne üzerinde yeni çağrı. Fonksiyonun kendi kurduğu nesne ve veri yapısı işlemleri sayılmaz
    (Bl.6 · Train Wrecks; G36)."""

    def __init__(self, source):
        super().__init__(source)
        self._constructions = Constructions()

    def notes(self):
        return [function.note(_train_wreck(chain)) for function in self._source.functions()
                for chain in self._outermost_chains(function)]

    def _outermost_chains(self, function):
        chained = [node for node in function.own_nodes() if self._is_call_on_call(node)]
        inner = {id(node.func.value) for node in chained}
        return [node for node in chained if id(node) not in inner]

    def _is_call_on_call(self, node):
        is_method_call = isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        if not is_method_call or node.func.attr in DATA_STRUCTURE_METHODS:
            return False
        return isinstance(node.func.value, ast.Call) and not self._constructions.creates(node.func.value)


def _train_wreck(chain):
    return alarm(f"zincirleme çağrı '{ast.unparse(chain)[:CHAIN_PREVIEW]}' (Bl.6 · Train Wrecks; G36)")
