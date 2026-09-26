"""Demeter Yasası ölçümü: fonksiyon yalnız yakın arkadaşlarıyla konuşur (Bl.6 · The Law of Demeter).
Kimin nesne kurduğunu ölçülen bütün kaynakların fabrikaları belirler; bu bilgi dışarıdan verilir (Bl.11 · DI)."""
import ast

from measure.findings import alarm
from measure.source_check import SourceCheck

CHAIN_PREVIEW = 60
DATA_STRUCTURE_METHODS = frozenset({"items", "keys", "values", "get", "copy", "count", "index", "split", "rsplit",
                                    "splitlines", "strip", "lstrip", "rstrip", "lower", "upper", "replace", "join",
                                    "startswith", "endswith", "format", "removeprefix", "removesuffix", "encode",
                                    "decode", "isalnum", "isalpha", "isdigit", "isspace", "isupper", "islower",
                                    "partition", "rpartition", "find", "rfind", "casefold", "group", "groups",
                                    "groupdict"})


class TrainWrecks(SourceCheck):
    """Dönen nesne üzerinde yeni çağrı. Fonksiyonun kendi kurduğu nesne ve veri yapısı işlemleri sayılmaz
    (Bl.6 · Train Wrecks; G36)."""

    def __init__(self, source, constructions):
        super().__init__(source)
        self._constructions = constructions

    def notes(self):
        return [function.note(_train_wreck(chain)) for function in self._source.functions()
                for chain in self._outermost_chains(function)]

    def _outermost_chains(self, function):
        sight = self._constructions.seen_from(function)
        chained = [node for node in function.own_nodes() if _is_call_on_call(node, sight)]
        inner = {id(node.func.value) for node in chained}
        return [node for node in chained if id(node) not in inner]


def _is_call_on_call(node, sight):
    is_method_call = isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    if not is_method_call or node.func.attr in DATA_STRUCTURE_METHODS:
        return False
    return isinstance(node.func.value, ast.Call) and not sight.creates(node.func.value)


def _train_wreck(chain):
    return alarm(f"zincirleme çağrı '{ast.unparse(chain)[:CHAIN_PREVIEW]}' (Bl.6 · Train Wrecks; G36)")
