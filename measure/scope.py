"""Tanımın yaşadığı yer: dosya ve sarmalayan sınıflar. Notun yeri buradan doğar."""
from measure.findings import Location

OWNER_SEPARATOR = "."


class Scope:
    """Bir dosyanın ya da sınıfın içi; tanımları yerleriyle adlandırır."""

    def __init__(self, path, owner=""):
        self._path = str(path)
        self._owner = owner

    def location(self, node):
        return self.location_at(node.lineno, self._qualified(node.name))

    def location_at(self, line, name):
        return Location(self._path, line, name)

    def inner(self, node):
        return Scope(self._path, self._qualified(node.name))

    def _qualified(self, name):
        return f"{self._owner}{OWNER_SEPARATOR}{name}" if self._owner else name
