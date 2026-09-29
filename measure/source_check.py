"""Kaynak ölçümlerinin tabanı. Her ölçüm, ölçtüğü kaynağı alanında tutan bir sınıftır;
bulguları kendi satırlarıyla not olarak döner."""
from abc import ABC, abstractmethod

from measure.findings import Note
from measure.source_file import SourceFile


class SourceCheck(ABC):
    """Tek kaynağın ölçümü; not listesi döner."""

    def __init__(self, source: SourceFile) -> None:
        self._source = source

    @abstractmethod
    def notes(self) -> list[Note]:
        """Notlar; temizse boş liste."""
