"""SonarQube'da taranan proje: anahtarı ve iki taramanın özellikleri (tasarım K7).

Anahtar kök klasörün adıdır; testler ayrıca `<ad>-testler` projesinde taranır.
"""
from collections.abc import Sequence
from pathlib import Path

TESTS_SUFFIX = "-testler"


class Project:
    """Kök ve köke göre test klasörleri; en az bir test klasörü vardır."""

    def __init__(self, root: Path, tests: Sequence[str]) -> None:
        self._root = root
        self._tests = tests

    def keys(self) -> tuple[str, str]:
        """Ana projenin ve test projesinin anahtarı."""
        return self._root.name, self._root.name + TESTS_SUFFIX

    def scans(self) -> list[dict[str, str]]:
        """Ana taramada testler test olarak bildirilir: teste özel kurallar yalnız orada çalışır. Test taramasında
        kaynak olarak bildirilir: genel kurallar testlere yalnız orada uygulanır (Bl.9 · Keeping Tests Clean)."""
        main, tests = self.keys()
        folders = ",".join(self._tests)
        excluded = ",".join(f"{folder}/**" for folder in self._tests)
        return [{"sonar.projectKey": main, "sonar.sources": ".", "sonar.exclusions": excluded, "sonar.tests": folders},
                {"sonar.projectKey": tests, "sonar.sources": folders}]
