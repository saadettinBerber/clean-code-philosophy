"""Ölçümün çıktısı: bulgu, yeri ve ikisini birleştiren not. Veri yapılarıdır, davranış taşımaz (Bl.6)."""
from dataclasses import dataclass

ALARM = "ALARM"
LOOK = "bak  "


@dataclass(frozen=True, order=True)
class Location:
    path: str
    line: int
    name: str


@dataclass(frozen=True, order=True)
class Finding:
    level: str
    message: str


@dataclass(frozen=True, order=True)
class Note:
    location: Location
    finding: Finding


def alarm(message):
    return Finding(ALARM, message)


def look(message):
    return Finding(LOOK, message)


def render(note):
    where, finding = note.location, note.finding
    return f"{where.path}:{where.line}: {finding.level} {where.name}: {finding.message}"
