"""Demeter Yasası ölçümü: fonksiyon yalnız yakın arkadaşlarıyla konuşur (Bl.6 · The Law of Demeter).
Kimin nesne kurduğunu ölçülen bütün kaynakların fabrikaları belirler; bu bilgi dışarıdan verilir (Bl.11 · DI)."""
import ast

from measure.acquaintances import Acquaintances
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
    """Yabancıyla konuşma: dönen nesne üzerinde yeni çağrı, nesne ister zincirde ister ara değişkende dursun.
    İki biçim de alıcıyı aynı sorudan geçirir (`Sight.hands_out`), bu yüzden hiçbir zaman farklı karar vermez.
    Fonksiyonun kendi kurduğu nesne ve veri yapısı işlemleri sayılmaz (Bl.6 · Train Wrecks, Hiding Structure; G36)."""

    def __init__(self, source, constructions):
        super().__init__(source)
        self._constructions = constructions

    def notes(self):
        return [function.note(finding) for function in self._source.functions() for finding in self._findings(function)]

    def _findings(self, function):
        sight = self._constructions.seen_from(function)
        calls = [node for node in function.own_nodes() if _is_behavior_call(node)]
        chains = _outermost([call for call in calls if sight.hands_out(call.func.value)])
        named = _called_through_names(calls, chains)
        return [_train_wreck(chain) for chain in chains] + _split_wrecks(named, Acquaintances(function, sight))


def _is_behavior_call(node):
    """Nesneye davranış çağrısı; veri yapısı işlemleri (`strip`, `get`…) sayılmaz."""
    is_method_call = isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    return is_method_call and node.func.attr not in DATA_STRUCTURE_METHODS


def _outermost(chained):
    inner = {id(node.func.value) for node in chained}
    return [node for node in chained if id(node) not in inner]


def _called_through_names(calls, chains):
    """Alıcısı yerel bir ad olan çağrılar; zincirin iç halkası olan çağrı zincirle birlikte bir kez söylenir."""
    links = {id(link) for chain in chains for link in ast.walk(chain.func.value)}
    return [call for call in calls if isinstance(call.func.value, ast.Name) and id(call) not in links]


def _split_wrecks(calls, acquaintances):
    return [_split_wreck(call, strangers[0]) for call in calls
            for strangers in [acquaintances.strangers_behind(call.func.value)] if strangers]


def _train_wreck(chain):
    return alarm(f"zincirleme çağrı '{ast.unparse(chain)[:CHAIN_PREVIEW]}' (Bl.6 · Train Wrecks; G36)")


def _split_wreck(call, binding):
    bound = f"{binding.name} = {ast.unparse(binding.value)}"[:CHAIN_PREVIEW]
    called = ast.unparse(call)[:CHAIN_PREVIEW]
    return alarm(f"ara değişkene bölünmüş zincir '{bound}' → '{called}' (Bl.6 · Train Wrecks; G36)")
