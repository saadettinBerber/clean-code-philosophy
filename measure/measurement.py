"""Ölçümün akışı: kaynakların fonksiyonlarını, sınıflarını ve kendilerini ölçer, notları sıralar."""
from collections.abc import Iterable, Sequence

from measure.class_checks import CLASS_CHECKS
from measure.class_definition import ClassDefinition
from measure.construction import Constructions
from measure.demeter import TrainWrecks
from measure.findings import Note
from measure.function import Function
from measure.function_checks import FunctionCheck
from measure.function_checks import FUNCTION_CHECKS
from measure.source_checks import SOURCE_CHECKS
from measure.source_file import SourceFile
from measure.switch_check import OneSwitch
from measure.test_checks import TEST_CHECKS


class Measurement:
    """Kaynak kümesinin ölçümü. Testler üretim koduyla aynı ölçümlerden geçer, üstüne test ölçümleri eklenir
    (Bl.9 · Keeping Tests Clean).

    Not yalnız ölçülen kaynaklara yazılır. Projenin öbür kaynakları yalnız bilinir: fabrikalar ve aynı ayırıcıya
    dallanan switch'ler dosya ötesi bilgidir, tek dosya ölçülürken de bütün projeden gelir."""

    def __init__(self, sources: Iterable[SourceFile], project: Iterable[SourceFile] = ()) -> None:
        self._sources = list(sources)
        self._known = self._sources + [source for source in project if source not in self._sources]

    def notes(self) -> list[Note]:
        return sorted(self._function_notes() + self._class_notes() + self._source_notes() + self._switch_notes()
                      + self._demeter_notes())

    def _functions(self) -> list[Function]:
        return [function for source in self._sources for function in source.functions()]

    def _known_functions(self) -> list[Function]:
        return [function for source in self._known for function in source.functions()]

    def _measured_only(self, notes: Sequence[Note]) -> list[Note]:
        return [note for note in notes if any(source.holds(note) for source in self._sources)]

    def _function_notes(self) -> list[Note]:
        return [function.note(finding) for function in self._functions()
                for check in self._checks_of(function) for finding in check.findings()]

    @staticmethod
    def _checks_of(function: Function) -> list[FunctionCheck]:
        kinds = FUNCTION_CHECKS + TEST_CHECKS if function.is_test() else FUNCTION_CHECKS
        return [kind(function) for kind in kinds]

    def _class_notes(self) -> list[Note]:
        return [definition.note(finding) for definition in self._classes()
                for check in [kind(definition) for kind in CLASS_CHECKS] for finding in check.findings()]

    def _classes(self) -> list[ClassDefinition]:
        return [definition for source in self._sources for definition in source.classes()]

    def _source_notes(self) -> list[Note]:
        return [note for source in self._sources for check in [kind(source) for kind in SOURCE_CHECKS]
                for note in check.notes()]

    def _switch_notes(self) -> list[Note]:
        return self._measured_only(OneSwitch(self._known_functions()).notes())

    def _demeter_notes(self) -> list[Note]:
        constructions = Constructions.among(self._known)
        return [note for source in self._sources for note in TrainWrecks(source, constructions).notes()]
