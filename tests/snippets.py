"""Testler için bellekte kod parçası kurar; disk ya da gerçek proje gerekmez (F.I.R.S.T · Repeatable)."""
import textwrap

from measure.source_file import SourceFile

SNIPPET_PATH = "parca.py"


class Snippet(SourceFile):
    """Bellekteki kaynak parçası; ilk fonksiyonu ya da ilk sınıfı ölçülecek olandır."""

    def __init__(self, code, path=SNIPPET_PATH):
        super().__init__(path, textwrap.dedent(code))

    def function(self):
        return self.top_level_functions()[0]

    def cls(self):
        return self.classes()[0]


def function_with_body_lines(count):
    body = "\n".join(f"    x{index} = {index}" for index in range(count))
    return Snippet(f"def f():\n{body}\n").function()


def levels(findings):
    return [finding.level for finding in findings]


def names(notes):
    return [note.location.name for note in notes]
