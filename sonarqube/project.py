"""SonarQube'da taranan proje: anahtarı ve iki taramanın özellikleri (tasarım K7).

Anahtar kök klasörün adıdır; testler ayrıca `<ad>-testler` projesinde taranır.
"""
from collections.abc import Sequence
from pathlib import Path

from sonarqube.scanner import Scan

TESTS_SUFFIX = "-testler"


class Project:
    """Kök ve köke göre test klasörleri; en az bir test klasörü vardır."""

    def __init__(self, root: Path, tests: Sequence[str]) -> None:
        self._root = root
        self._tests = tests

    def keys(self) -> tuple[str, str]:
        """Ana projenin ve test projesinin anahtarı."""
        return self._root.name, self._root.name + TESTS_SUFFIX

    def component(self, path: str) -> str:
        """Dosyanın sunucudaki adı; test dosyası da ana projede dizinlidir."""
        return f"{self._root.name}:{path}"

    def scans(self) -> list[Scan]:
        """Ana taramada testler test olarak bildirilir: teste özel kurallar yalnız orada çalışır. Test taramasında
        kaynak olarak bildirilir: genel kurallar testlere yalnız orada uygulanır (Bl.9 · Keeping Tests Clean)."""
        main, tests = self.keys()
        folders = ",".join(self._tests)
        excluded = ",".join(f"{folder}/**" for folder in self._tests)
        main_scan = {"sonar.projectKey": main, "sonar.sources": ".", "sonar.exclusions": excluded,
                     "sonar.tests": folders}
        return [Scan(self._root, main_scan), Scan(self._root, {"sonar.projectKey": tests, "sonar.sources": folders})]
