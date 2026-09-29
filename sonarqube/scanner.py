"""SonarQube tarayıcısı: klasörü salt okunur bağlayıp tarar, sunucu raporu işleyene dek bekler (tasarım K7).

Tarayıcının yazdığı her şey geçici bir çalışma klasörüne gider; taranan depoya dosya yazılmaz. İmaj, sunucu gibi,
imaj kimliğiyle sabittir (8.1.0.6389); yükseltmeden sonra öğrenme testleri yeniden koşulur.
"""
import os
import subprocess
import tempfile
import time
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from sonarqube.web import SonarQubeError, WebApi

IMAGE = "sonarsource/sonar-scanner-cli@sha256:a3f4215076706c95a17a68c19322ee916e40a3acd081a8c1a1e839e0194afa57"
# Adı `test_` ile başlayan üretim dosyası tahmin açıkken sessizce atlanır (öğrenme testi).
COMMON_PROPERTIES = {"sonar.python.version": "3.13", "sonar.python.testFileHeuristic.disabled": "true",
                     "sonar.working.directory": "/scan/.scannerwork"}
REPORT_TASK = Path(".scannerwork") / "report-task.txt"
TASK_ID_KEY = "ceTaskId="
WAITING = frozenset({"PENDING", "IN_PROGRESS"})
SUCCESS = "SUCCESS"
TIMED_OUT = "zaman aşımı"
POLL_SECONDS = 2
MAX_POLLS = 90
OUTPUT_TAIL = 3000


class ScanError(SonarQubeError):
    """Tarama bir şey kanıtlayamaz: tarayıcı başarısız oldu ya da sunucu raporu işleyemedi."""


@dataclass(frozen=True)
class Scan:
    """Bir tarama: taranan kök ve tarayıcıya verilen özellikler."""

    root: Path
    properties: Mapping[str, str]


class Scanner:
    """Tarayıcı konteyneri. Token yalnız konteynerin ortam değişkeninde ve istek başlığında durur."""

    def __init__(self, url: str, token: str) -> None:
        self._url = url
        self._token = token
        self._web = WebApi(url, token)

    def scan(self, scan: Scan) -> None:
        """Kökü verilen özelliklerle tarar; sunucu raporu işleyene dek bekler."""
        with tempfile.TemporaryDirectory() as work:
            self._run(self._container(scan.root, Path(work)) + arguments(scan.properties))
            self._wait(task_id(Path(work) / REPORT_TASK))

    def _container(self, root: Path, work: Path) -> list[str]:
        """Kök salt okunur bağlanır; tarayıcının yazdığı her şey çalışma klasörüne gider."""
        return ["docker", "run", "--rm", "--network", "host", "--user", f"{os.getuid()}:{os.getgid()}",
                "-e", "SONAR_TOKEN", "-e", "SONAR_USER_HOME=/scan/.sonar", "-e", f"SONAR_HOST_URL={self._url}",
                "-v", f"{root}:/usr/src:ro", "-v", f"{work}:/scan", IMAGE]

    def _run(self, command: list[str]) -> None:
        run = subprocess.run(command, env={**os.environ, "SONAR_TOKEN": self._token}, capture_output=True, text=True)
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
        return str(self._web.get("api/ce/task", {"id": task})["task"]["status"])


def arguments(properties: Mapping[str, str]) -> list[str]:
    """Ortak ayarlar ve taramanın kendi özellikleri, tarayıcının `-D` argümanları olarak."""
    return [f"-D{name}={value}" for name, value in {**COMMON_PROPERTIES, **properties}.items()]


def task_id(report: Path) -> str:
    """Tarayıcının bıraktığı `report-task.txt` içindeki analiz görevinin kimliği."""
    [task] = [line.removeprefix(TASK_ID_KEY) for line in report.read_text(encoding="utf-8").splitlines()
              if line.startswith(TASK_ID_KEY)]
    return task
