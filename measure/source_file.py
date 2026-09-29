"""Ölçülen kaynak dosya: fonksiyonları, sınıfları ve yorumları. Disk sınırı `read`dir."""
import ast
from pathlib import Path
from typing import Self

from measure.class_definition import ClassDefinition
from measure.comments import Comments
from measure.findings import Location, Note
from measure.function import Function
from measure.scope import Home, Scope
from measure.syntax import FUNCTION_NODES


class SourceFile:
    """Bir Python kaynağı; ölçümler dosyayı değil bu nesneyi sorgular."""

    def __init__(self, path: str | Path, text: str) -> None:
        self._scope = Scope(path)
        self._text = text
        self._tree = ast.parse(text, filename=str(path))

    @classmethod
    def read(cls, path: str | Path) -> Self:
        return cls(path, Path(path).read_text(encoding="utf-8"))

    def holds(self, note: Note) -> bool:
        return self._scope.owns(note.location)

    def module_home(self) -> Home:
        return self._scope.module_home()

    def location(self, line: int, name: str) -> Location:
        return self._scope.location_at(line, name)

    def top_level_functions(self) -> list[Function]:
        return [Function(node, self._scope) for node in self._tree.body if isinstance(node, FUNCTION_NODES)]

    def classes(self) -> list[ClassDefinition]:
        return [ClassDefinition(node, self._scope) for node in self._tree.body if isinstance(node, ast.ClassDef)]

    def functions(self) -> list[Function]:
        """Modül düzeyi fonksiyonlar ve sınıf metotları."""
        return self.top_level_functions() + [method for cls in self.classes() for method in cls.methods()]

    def top_level_nodes(self) -> list[ast.stmt]:
        return list(self._tree.body)

    def docstring(self) -> str:
        return ast.get_docstring(self._tree) or ""

    def comments(self) -> Comments:
        return Comments(self._scope, self._text)

