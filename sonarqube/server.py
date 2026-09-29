"""Çalışma zamanının SonarQube sınırı (tasarım K2): durum, iki tarama, bulgular.

measure_code yalnız bu sınıfı tanır. SonarQube'un JSON'u dışarı çıkmaz, yerine kendi küçük veri yapımız döner
(Bl.8 · Using Third-Party Code).
"""
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum

from sonarqube.project import Project
from sonarqube.scanner import Scanner
from sonarqube.web import Json, Unreachable, WebApi

ISSUE_SEARCH = "api/issues/search"
# Dosya düzeyindeki bulgunun (S104 gibi) satırı yoktur; dosyanın başına, modüle yazılır.
FILE_LEVEL_LINE = 1


@dataclass(frozen=True)
class ReportedIssue:
    """SonarQube'un bulgusu, kendi küçük veri yapımızda; yol proje köküne göre."""

    rule: str
    path: str
    line: int
    message: str
    kind: str


class ServerStatus(Enum):
    UP = "UP"
    STARTING = "STARTING"
    DOWN = "DOWN"


# Burada olmayan her durum (DOWN, DB_MIGRATION_NEEDED) sunucunun kullanılamadığını söyler.
STATUSES = {"UP": ServerStatus.UP, "STARTING": ServerStatus.STARTING, "RESTARTING": ServerStatus.STARTING,
            "DB_MIGRATION_RUNNING": ServerStatus.STARTING}


class SonarQubeServer:
    """Sınır ailesinin önündeki tek kapı (FACADE; tamam-tanimi · kalıp tablosu, Bl.8): tarayıcıyla web API'sini
    koordine eder, karar vermez. İki alanın ayrı metotlara düşmesi bu yüzdendir."""

    def __init__(self, url: str, token: str) -> None:
        self._web = WebApi(url, token)
        self._scanner = Scanner(url, token)

    def status(self) -> ServerStatus:
        """Ulaşılamayan sunucu da ayakta değildir (K8)."""
        try:
            return server_status(str(self._web.get("api/system/status", {})["status"]))
        except Unreachable:
            return ServerStatus.DOWN

    def analyze(self, project: Project) -> None:
        """İki tarama (K7); her biri sunucu raporu işleyene dek bekler."""
        for scan in project.scans():
            self._scanner.scan(scan)

    def issues(self, project: Project) -> list[ReportedIssue]:
        """Ana projenin ve test projesinin açık bulguları."""
        pages = [page for key in project.keys()
                 for page in self._web.pages(ISSUE_SEARCH, {"components": key, "resolved": "false"})]
        return distinct(reported(issue) for page in pages for issue in page["issues"])


def server_status(state: str) -> ServerStatus:
    return STATUSES.get(state, ServerStatus.DOWN)


def reported(issue: Json) -> ReportedIssue:
    """Bileşen `anahtar:yol` biçimindedir; yol proje anahtarından arınır."""
    _, path = str(issue["component"]).split(":", 1)
    line = int(issue.get("line", FILE_LEVEL_LINE))
    return ReportedIssue(str(issue["rule"]), path, line, str(issue["message"]), str(issue["type"]))


def distinct(issues: Iterable[ReportedIssue]) -> list[ReportedIssue]:
    """Hem üretimde hem testte çalışan kural (pilot: S5778) test dosyasını iki taramada da bulur; bir kez sayılır."""
    return list(dict.fromkeys(issues))
