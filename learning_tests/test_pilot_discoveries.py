"""Pilotun SonarQube keşifleri, gerçek sunucuda (Bl.8 · Learning Tests Are Better Than Free).

Hızlı takıma girmez; SonarQube her güncellendiğinde yeniden koşulur:
    python3 -m unittest discover -s learning_tests -t .
Proje tek taramayla ölçülür; her keşif ayrı bir testtir. Kaynak: sonarqube-pilot-raporu.md §5, §7.
"""
import unittest

from learning_tests.scan import TOKEN_FILE, SonarQube

LONG_LINE = f"TITLE = '{'x' * 130}'\n"
PRODUCTION_NAMED_LIKE_A_TEST = "def checks() -> list[str]:\n    return []\n\n\n" + LONG_LINE
LONG_LINE_NUMBER = 5

PROJECT_FILES = {
    "src/test_checks.py": PRODUCTION_NAMED_LIKE_A_TEST,
}


class PilotDiscoveriesTest(unittest.TestCase):
    sonarqube: SonarQube

    @classmethod
    def setUpClass(cls) -> None:
        cls.sonarqube = SonarQube(TOKEN_FILE.read_text(encoding="utf-8").strip())
        cls.sonarqube.analyze(PROJECT_FILES)

    def test_production_file_named_like_a_test_is_measured(self) -> None:
        """Test tahmini kapalıyken `test_*.py` adı üretim dosyasını test yapmaz, kurallar ona uygulanır."""
        self.assertEqual(self.sonarqube.issue_lines("python:LineLength", "src/test_checks.py"), [LONG_LINE_NUMBER])


if __name__ == "__main__":
    unittest.main()
