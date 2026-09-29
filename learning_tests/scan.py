"""Öğrenme testlerinin projesini gerçek SonarQube sunucusuna taratır, sonucu web API'sinden okur.

Üçüncü tarafın uç noktalarını doğrudan çağırır; bu testler SonarQube'un neye dayanılabilir olduğunu öğrenir
(Bl.8 · Learning Tests). Tarama ve istek sınır ailesinin kapılarından geçer (`sonarqube/scanner.py`, `web.py`).
`ogrenme-testleri` projesi bir kez, yönetim yetkisiyle pilot profiline bağlanmıştır.
"""
import tempfile
from collections.abc import Mapping
from pathlib import Path

from sonarqube.scanner import Scan, Scanner
from sonarqube.web import Json, WebApi

SERVER = "http://127.0.0.1:9000"
TOKEN_FILE = Path.home() / ".config" / "secrets" / "sonarqube-token"
PROJECT = "ogrenme-testleri"
PROFILE = "Pilot · tüm kurallar"
SCAN_PROPERTIES = {"sonar.projectKey": PROJECT, "sonar.sources": "src,test_sources", "sonar.tests": "tests"}


class WrongProfile(Exception):
    """Proje pilot profiline bağlı değil; keşifler yanlış eşiklerle sınanırdı."""


class SonarQube:
    """Öğrenme projesini tarayan ve sorgulayan gerçek sunucu."""

    def __init__(self, token: str) -> None:
        self._web = WebApi(SERVER, token)
        self._scanner = Scanner(SERVER, token)

    def analyze(self, files: Mapping[str, str]) -> None:
        """Bellekteki projeyi geçici klasöre yazıp tarar."""
        self._require_profile()
        with tempfile.TemporaryDirectory() as project:
            write_files(files, Path(project))
            self._scanner.scan(Scan(Path(project), SCAN_PROPERTIES))

    def issue_lines(self, rule: str, path: str) -> list[int]:
        """Dosyada kuralın açık bulgularının satırları. Arama API'si tanımadığı dosyaya da boş liste döner;
        boş cevap "bakılmadı" anlamına gelmesin diye dosya önce sorulur."""
        self._require_file(path)
        query = {"components": f"{PROJECT}:{path}", "rules": rule, "resolved": "false"}
        found = self._web.get("api/issues/search", query)
        return sorted(int(issue["line"]) for issue in found["issues"])

    def duplicated_lines(self, path: str) -> int:
        """Dosyada kopyası başka yerde bulunan satırların sayısı (CPD)."""
        [measure] = self._measures(path, "duplicated_lines")
        return int(measure["value"])

    def _require_profile(self) -> None:
        """Kitap eşikleri pilot profilinde; başka profille taranan proje keşifleri yanlış sınar."""
        [profile] = self._web.get("api/qualityprofiles/search", {"project": PROJECT, "language": "py"})["profiles"]
        if profile["name"] != PROFILE:
            raise WrongProfile(f"{PROJECT} '{profile['name']}' profiline bağlı, beklenen '{PROFILE}'")

    def _require_file(self, path: str) -> None:
        """Sunucunun dizinlemediği dosya için ölçüm API'si 404 döner."""
        self._measures(path, "lines")

    def _measures(self, path: str, metric: str) -> list[Json]:
        found = self._web.get("api/measures/component", {"component": f"{PROJECT}:{path}", "metricKeys": metric})
        return list(found["component"]["measures"])


def write_files(files: Mapping[str, str], root: Path) -> None:
    for path, code in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(code, encoding="utf-8")
