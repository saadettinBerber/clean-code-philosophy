"""Test fonksiyonu ölçümleri (Bl.9, Bl.10 · Encapsulation, T4). Yalnız testlere uygulanır; testler ayrıca
üretim koduyla aynı fonksiyon ölçümlerinden geçer (Bl.9 · Keeping Tests Clean).
"""
import ast

from measure.findings import Finding, alarm, look
from measure.function_checks import FunctionCheck
from measure.syntax import is_name, last_name

SINGLE_ASSERT = 1
UNREPEATABLE_CALLS = frozenset({"time", "now", "today", "utcnow", "sleep", "random", "randint", "choice", "shuffle",
                                "uniform"})
UNREPEATABLE_PATHS = ("/home/", "Desktop", "~/")
SKIP_DECORATORS = frozenset({"skip", "skipIf", "skipUnless"})


def is_assert_call(node: ast.AST) -> bool:
    """`self.assert…` çağrısı; adı yalnız "assert" ile başlayan başka bir fonksiyon sayılmaz."""
    func = node.func if isinstance(node, ast.Call) else None
    return isinstance(func, ast.Attribute) and is_name(func.value, "self") and func.attr.startswith("assert")


class TestCheck(FunctionCheck):
    """Test ölçümlerinin ortak sorusu: testin denetimleri."""

    def _asserts(self) -> list[ast.AST]:
        return [node for node in self._function.own_nodes() if is_assert_call(node)]


class MissingAssert(TestCheck):
    def findings(self) -> list[Finding]:
        return [] if self._asserts() else [alarm("assert yok; test kendi sonucunu söylemiyor (Bl.9 · F.I.R.S.T · Self-Validating)")]


class Printing(TestCheck):
    def findings(self) -> list[Finding]:
        return [alarm("testte print; sonuca bakmak gerekmemeli (Bl.9 · F.I.R.S.T · Self-Validating)")
                for node in self._function.own_nodes() if isinstance(node, ast.Call) and is_name(node.func, "print")]


class AssertCount(TestCheck):
    def findings(self) -> list[Finding]:
        count = len(self._asserts())
        return [look(f"{count} assert; tek kavram mı? (Bl.9 · One Assert per Test)")] if count > SINGLE_ASSERT else []


class OperateAfterCheck(TestCheck):
    """İlk denetimden sonra denetim olmayan deyim: yeni işlem, yani ikinci kavram (BUILD-OPERATE-CHECK)."""

    def findings(self) -> list[Finding]:
        statements = self._function.statements()
        first = next((index for index, statement in enumerate(statements) if self._checks(statement)), len(statements))
        later = [statement for statement in statements[first:] if not self._checks(statement)]
        return [alarm("denetimden sonra yeni işlem (Bl.9 · Clean Tests: BUILD-OPERATE-CHECK)")] if later else []

    @staticmethod
    def _checks(statement: ast.stmt) -> bool:
        return isinstance(statement, ast.Assert) or any(is_assert_call(node) for node in ast.walk(statement))


class PrivateAccess(TestCheck):
    def findings(self) -> list[Finding]:
        names = sorted({node.attr for node in self._function.own_nodes() if self._is_foreign_private(node)})
        return [alarm(f"özel üyelere dokunuyor {names} (Bl.10 · Encapsulation)")] if names else []

    @staticmethod
    def _is_foreign_private(node: ast.AST) -> bool:
        is_private = isinstance(node, ast.Attribute) and node.attr.startswith("_") and not node.attr.startswith("__")
        return is_private and not is_name(node.value, "self")


class Unrepeatable(TestCheck):
    def findings(self) -> list[Finding]:
        nodes = self._function.own_nodes()
        calls = {last_name(node.func) for node in nodes if isinstance(node, ast.Call)} & UNREPEATABLE_CALLS
        paths = {node.value for node in nodes if self._is_machine_path(node)}
        found = sorted(calls) + sorted(paths)
        return [alarm(f"tekrarlanamaz: {found} (Bl.9 · F.I.R.S.T · Repeatable)")] if found else []

    @staticmethod
    def _is_machine_path(node: ast.AST) -> bool:
        is_text = isinstance(node, ast.Constant) and isinstance(node.value, str)
        return is_text and any(part in node.value for part in UNREPEATABLE_PATHS)


class UnexplainedSkip(TestCheck):
    def findings(self) -> list[Finding]:
        skips = [d for d in self._function.decorators() if self._decorator_name(d) in SKIP_DECORATORS]
        unexplained = [d for d in skips if not (isinstance(d, ast.Call) and d.args)]
        return [alarm("gerekçesiz skip; gerekçe bir soru olarak yazılır (T4)")] if unexplained else []

    @staticmethod
    def _decorator_name(decorator: ast.expr) -> str:
        return last_name(decorator.func if isinstance(decorator, ast.Call) else decorator)


TEST_CHECKS = (MissingAssert, Printing, AssertCount, OperateAfterCheck, PrivateAccess, Unrepeatable, UnexplainedSkip)
