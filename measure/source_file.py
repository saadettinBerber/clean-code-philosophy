"""Ölçülen kaynak dosya: fonksiyonları, sınıfları ve yorumları. Disk sınırı `read`dir."""
import ast
from pathlib import Path

from measure.class_definition import ClassDefinition
from measure.comments import Comments
from measure.function import Function
from measure.scope import Scope
from measure.syntax import FUNCTION_NODES


class SourceFile:
    """Bir Python kaynağı; ölçümler dosyayı değil bu nesneyi sorgular."""

    def __init__(self, path, text):
        self._scope = Scope(path)
        self._text = text
        self._tree = ast.parse(text, filename=str(path))

    @classmethod
    def read(cls, path):
        return cls(path, Path(path).read_text(encoding="utf-8"))

    def location(self, line, name):
        return self._scope.location_at(line, name)

    def top_level_functions(self):
        return [Function(node, self._scope) for node in self._top(FUNCTION_NODES)]

    def classes(self):
        return [ClassDefinition(node, self._scope) for node in self._top(ast.ClassDef)]

    def functions(self):
        """Modül düzeyi fonksiyonlar ve sınıf metotları."""
        return self.top_level_functions() + [method for cls in self.classes() for method in cls.methods()]

    def top_level_nodes(self):
        return list(self._tree.body)

    def docstring(self):
        return ast.get_docstring(self._tree) or ""

    def comments(self):
        return Comments(self._scope, self._text)

    def _top(self, kinds):
        return [node for node in self._tree.body if isinstance(node, kinds)]
