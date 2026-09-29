"""Testler için bellekte kod parçası kurar; disk ya da gerçek proje gerekmez (F.I.R.S.T · Repeatable)."""
import ast
import textwrap
from collections.abc import Iterable

from measure.class_definition import ClassDefinition
from measure.findings import Finding, Note
from measure.function import Function
from measure.scope import Scope
from measure.source_file import SourceFile
from measure.syntax import FUNCTION_NODES

SNIPPET_PATH = "parca.py"


class Snippet(SourceFile):
    """Bellekteki kaynak parçası; ilk fonksiyonu ya da ilk sınıfı ölçülecek olandır."""

    def __init__(self, code: str, path: str = SNIPPET_PATH) -> None:
        super().__init__(path, textwrap.dedent(code))

    def function(self) -> Function:
        return self.top_level_functions()[0]

    def cls(self) -> ClassDefinition:
        return self.classes()[0]


def function_in(code: str) -> Function:
    """Parçanın ilk fonksiyonu, test için yeni kurulmuş bir `Function` olarak (Bl.9 · BUILD-OPERATE-CHECK)."""
    [node] = [node for node in ast.parse(textwrap.dedent(code)).body if isinstance(node, FUNCTION_NODES)]
    return Function(node, Scope(SNIPPET_PATH))


def function_with_body_lines(count: int) -> Function:
    body = "\n".join(f"    x{index} = {index}" for index in range(count))
    return Snippet(f"def f():\n{body}\n").function()


def levels(findings: Iterable[Finding]) -> list[str]:
    return [finding.level for finding in findings]


def names(notes: Iterable[Note]) -> list[str]:
    return [note.location.name for note in notes]
