"""Kaynak ölçümlerinin tabanı. Her ölçüm, ölçtüğü kaynağı alanında tutan bir sınıftır;
bulguları kendi satırlarıyla not olarak döner."""
from abc import ABC, abstractmethod


class SourceCheck(ABC):
    """Tek kaynağın ölçümü; not listesi döner."""

    def __init__(self, source):
        self._source = source

    @abstractmethod
    def notes(self):
        """Notlar; temizse boş liste."""
