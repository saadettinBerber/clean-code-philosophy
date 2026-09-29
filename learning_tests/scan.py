"""Öğrenme testlerinin projesini gerçek SonarQube sunucusuna taratır, sonucu web API'sinden okur.

Üçüncü tarafı doğrudan çağırır: sınır nesnesi (`SonarQubeServer`) henüz yok, bu testler onun neye dayanacağını
öğrenir (Bl.8 · Learning Tests). `ogrenme-testleri` projesi bir kez, yönetim yetkisiyle pilot profiline bağlanmıştır.
"""
import json
import os
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Mapping
from pathlib import Path
from typing import Any

SERVER = "http://127.0.0.1:9000"
SCANNER = "sonarsource/sonar-scanner-cli@sha256:a3f4215076706c95a17a68c19322ee916e40a3acd081a8c1a1e839e0194afa57"
TOKEN_FILE = Path.home() / ".config" / "secrets" / "sonarqube-token"
PROJECT = "ogrenme-testleri"
PROFILE = "Pilot · tüm kurallar"
SCAN_PROPERTIES = (f"-Dsonar.projectKey={PROJECT}", "-Dsonar.sources=src",
                   "-Dsonar.python.version=3.13", "-Dsonar.python.testFileHeuristic.disabled=true",
                   "-Dsonar.working.directory=/scan/.scannerwork")
REPORT_TASK = Path(".scannerwork") / "report-task.txt"
TASK_ID_KEY = "ceTaskId="
WAITING = frozenset({"PENDING", "IN_PROGRESS"})
SUCCESS = "SUCCESS"
TIMED_OUT = "zaman aşımı"
POLL_SECONDS = 2
MAX_POLLS = 90
OUTPUT_TAIL = 3000

Json = dict[str, Any]


class ScanError(Exception):
    """Tarama ya da sorgu bir şey kanıtlayamaz: profil yanlış, tarayıcı başarısız, sunucu işleyemedi ya da reddetti."""


class SonarQube:
    """Gerçek sunucu: tarayıcı konteyneri ve web API'si. Token yalnız ortam değişkeninde ve istek başlığında durur."""

    def __init__(self, token: str) -> None:
        self._token = token

    def analyze(self, files: Mapping[str, str]) -> None:
        """Bellekteki projeyi geçici klasöre yazar, klasörü salt okunur bağlayıp tarar, sunucu işleyene dek bekler."""
        self._require_profile()
        with tempfile.TemporaryDirectory() as project, tempfile.TemporaryDirectory() as work:
            write_files(files, Path(project))
            self._scan(Path(project), Path(work))
            self._wait(task_id(Path(work) / REPORT_TASK))

    def issue_lines(self, rule: str, path: str) -> list[int]:
        """Dosyada kuralın açık bulgularının satırları. Arama API'si tanımadığı dosyaya da boş liste döner;
        boş cevap "bakılmadı" anlamına gelmesin diye dosya önce sorulur."""
        self._require_file(path)
        found = self._get("api/issues/search", {"components": f"{PROJECT}:{path}", "rules": rule, "resolved": "false"})
        return sorted(int(issue["line"]) for issue in found["issues"])

    def _require_profile(self) -> None:
        """Kitap eşikleri pilot profilinde; başka profille taranan proje keşifleri yanlış sınar."""
        [profile] = self._get("api/qualityprofiles/search", {"project": PROJECT, "language": "py"})["profiles"]
        if profile["name"] != PROFILE:
            raise ScanError(f"{PROJECT} '{profile['name']}' profiline bağlı, beklenen '{PROFILE}'")

    def _require_file(self, path: str) -> None:
        """Sunucunun dizinlemediği dosya için ölçüm API'si 404 döner."""
        self._get("api/measures/component", {"component": f"{PROJECT}:{path}", "metricKeys": "lines"})

    def _scan(self, project: Path, work: Path) -> None:
        run = subprocess.run(scanner_command(project, work), env={**os.environ, "SONAR_TOKEN": self._token},
                             capture_output=True, text=True)
        if run.returncode:
            raise ScanError(f"tarayıcı {run.returncode} koduyla bitti:\n{run.stdout[-OUTPUT_TAIL:]}")

    def _wait(self, task: str) -> None:
        statuses = (self._polled_status(task) for _ in range(MAX_POLLS))
        status = next((status for status in statuses if status not in WAITING), TIMED_OUT)
        if status != SUCCESS:
            raise ScanError(f"sunucu raporu işleyemedi: {status} (görev {task})")

    def _polled_status(self, task: str) -> str:
        """Biraz bekleyip analiz görevinin durumunu sorar."""
        time.sleep(POLL_SECONDS)
        return str(self._get("api/ce/task", {"id": task})["task"]["status"])

    def _get(self, api: str, parameters: Mapping[str, str]) -> Json:
        try:
            return self._response(api, parameters)
        except urllib.error.HTTPError as error:
            raise ScanError(f"{api} {dict(parameters)}: {error.code} {error.read().decode()}") from error

    def _response(self, api: str, parameters: Mapping[str, str]) -> Json:
        request = urllib.request.Request(f"{SERVER}/{api}?{urllib.parse.urlencode(parameters)}",
                                         headers={"Authorization": f"Bearer {self._token}"})
        with urllib.request.urlopen(request) as response:
            return dict(json.load(response))


def write_files(files: Mapping[str, str], root: Path) -> None:
    for path, code in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(code, encoding="utf-8")


def scanner_command(project: Path, work: Path) -> list[str]:
    """Proje klasörü salt okunur bağlanır; tarayıcının yazdığı her şey çalışma klasörüne gider."""
    return ["docker", "run", "--rm", "--network", "host", "--user", f"{os.getuid()}:{os.getgid()}",
            "-e", "SONAR_TOKEN", "-e", "SONAR_USER_HOME=/scan/.sonar", "-e", f"SONAR_HOST_URL={SERVER}",
            "-v", f"{project}:/usr/src:ro", "-v", f"{work}:/scan", SCANNER, *SCAN_PROPERTIES]


def task_id(report: Path) -> str:
    """Tarayıcının bıraktığı `report-task.txt` içindeki analiz görevinin kimliği."""
    [task] = [line.removeprefix(TASK_ID_KEY) for line in report.read_text(encoding="utf-8").splitlines()
              if line.startswith(TASK_ID_KEY)]
    return task
