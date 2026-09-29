"""Tanımın yaşadığı yer: dosya ve sarmalayan sınıflar. Notun yeri buradan doğar."""
from __future__ import annotations

import ast
from pathlib import Path

from measure.findings import Location
from measure.syntax import Definition

OWNER_SEPARATOR = "."
# Tanımın evi: (dosya, sahibi olan sınıf); ad aranacak yer yoksa boş demet.
Home = tuple[str, ...]


class Scope:
    """Bir dosyanın ya da sınıfın içi; tanımları yerleriyle adlandırır."""

    def __init__(self, path: str | Path, owner: str = "") -> None:
        self._path = str(path)
        self._owner = owner

    def location(self, node: Definition) -> Location:
        return self.location_at(node.lineno, self._qualified(node.name))

    def location_at(self, line: int, name: str) -> Location:
        return Location(self._path, line, name)

    def home(self) -> Home:
        """Tanımın yaşadığı yer: dosya ve sahibi olan sınıf."""
        return self._path, self._owner

    def module_home(self) -> Home:
        return self._path, ""

    def owns(self, location: Location) -> bool:
        return location.path == self._path

    def inner(self, node: ast.ClassDef) -> Scope:
        return Scope(self._path, self._qualified(node.name))

    def _qualified(self, name: str) -> str:
        return f"{self._owner}{OWNER_SEPARATOR}{name}" if self._owner else name
