"""Ölçümün akışı: kaynakların fonksiyonlarını, sınıflarını ve kendilerini ölçer, notları sıralar."""
from measure.class_checks import CLASS_CHECKS
from measure.construction import Constructions
from measure.demeter import TrainWrecks
from measure.function_checks import FUNCTION_CHECKS
from measure.source_checks import SOURCE_CHECKS
from measure.switch_check import OneSwitch
from measure.test_checks import TEST_CHECKS


class Measurement:
    """Kaynak kümesinin ölçümü. Testler üretim koduyla aynı ölçümlerden geçer, üstüne test ölçümleri eklenir
    (Bl.9 · Keeping Tests Clean)."""

    def __init__(self, sources):
        self._sources = sources

    def notes(self):
        return sorted(self._function_notes() + self._class_notes() + self._source_notes() + self._switch_notes()
                      + self._demeter_notes())

    def _functions(self):
        return [function for source in self._sources for function in source.functions()]

    def _function_notes(self):
        return [function.note(finding) for function in self._functions()
                for check in self._checks_of(function) for finding in check.findings()]

    @staticmethod
    def _checks_of(function):
        kinds = FUNCTION_CHECKS + TEST_CHECKS if function.is_test() else FUNCTION_CHECKS
        return [kind(function) for kind in kinds]

    def _class_notes(self):
        return [definition.note(finding) for definition in self._classes()
                for check in [kind(definition) for kind in CLASS_CHECKS] for finding in check.findings()]

    def _classes(self):
        return [definition for source in self._sources for definition in source.classes()]

    def _source_notes(self):
        return [note for source in self._sources for check in [kind(source) for kind in SOURCE_CHECKS]
                for note in check.notes()]

    def _switch_notes(self):
        return OneSwitch(self._functions()).notes()

    def _demeter_notes(self):
        constructions = Constructions.among(self._functions())
        return [note for source in self._sources for note in TrainWrecks(source, constructions).notes()]
