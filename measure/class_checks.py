"""Sınıf ölçümleri (Bl.5, Bl.6, Bl.10). Her ölçüm, ölçtüğü sınıfı alanında tutan bir sınıftır.
Boyut yalnız alarmdır; sorumluluk kümeleri sınıfın boyu ne olursa olsun çıkarılır (SuperDashboard).
"""
from abc import ABC, abstractmethod

from measure.class_definition import ClassDefinition
from measure.findings import Finding, alarm, look

MAX_CLASS_LINES = 200
SINGLE_RESPONSIBILITY = 1


class ClassCheck(ABC):
    """Tek sınıfın ölçümü; bulgu listesi döner."""

    def __init__(self, definition: ClassDefinition) -> None:
        self._class = definition

    @abstractmethod
    def findings(self) -> list[Finding]:
        """Bulgular; temizse boş liste."""


class ClassSize(ClassCheck):
    def findings(self) -> list[Finding]:
        lines = self._class.length()
        return [alarm(f"{lines} satır, alarm {MAX_CLASS_LINES} (Bl.10 · Classes Should Be Small!)")] if lines > MAX_CLASS_LINES else []


class Responsibilities(ClassCheck):
    def findings(self) -> list[Finding]:
        clusters = self._class.responsibility_clusters()
        if len(clusters) <= SINGLE_RESPONSIBILITY:
            return []
        described = " | ".join(f"{names} ← {fields}" for names, fields in clusters)
        return [alarm(f"{len(clusters)} ayrık sorumluluk kümesi: {described} (Bl.10 · SRP)")]


class Cohesion(ClassCheck):
    def findings(self) -> list[Finding]:
        if self._class.is_data_structure():
            return []
        return [look(f"alan '{field}' yalnız {users or ['kurucu']} kullanıyor (Bl.10 · Cohesion)")
                for field, users in sorted(self._class.field_users().items()) if len(users) <= SINGLE_RESPONSIBILITY]


class FieldsOutsideConstructor(ClassCheck):
    def findings(self) -> list[Finding]:
        return [alarm(f"alan '{field}' kurucu dışında doğuyor (Bl.5 · Variable Declarations; Bl.10 · Cohesion)")
                for field in sorted(self._class.late_fields())]


class Hybrid(ClassCheck):
    def findings(self) -> list[Finding]:
        state, behavior = self._class.public_state(), self._class.behavior_methods()
        if self._class.is_test_case() or not (state and behavior):
            return []
        return [alarm(f"melez: açık durum {state} ile davranış {behavior} bir arada (Bl.6 · Hybrids; G14)")]


class UnusedSelf(ClassCheck):
    def findings(self) -> list[Finding]:
        return [look(f"metot '{method.name()}' self'i kullanmıyor (G14 · Feature Envy; G18)")
                for method in self._class.methods() if method.ignores_self()]


CLASS_CHECKS = (ClassSize, Responsibilities, Cohesion, FieldsOutsideConstructor, Hybrid, UnusedSelf)
