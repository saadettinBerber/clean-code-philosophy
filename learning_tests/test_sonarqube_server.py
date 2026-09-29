"""SonarQubeServer gerçek sunucuya karşı (tasarım §7.3 · Bl.8 outbound tests).

Üretim kodunun sınırı kullandığı gibi kullanır; SonarQube yükseltilince öğrenme testleriyle birlikte koşulur:
    python3 -m unittest discover -s learning_tests -t .
`sinir-testi` projesi ilk taramada kendiliğinden kurulur ve varsayılan profili, yani kitabın profilini alır.
"""
import tempfile
import unittest
from pathlib import Path

from learning_tests.scan import SERVER, TOKEN_FILE, write_files
from sonarqube.project import Project
from sonarqube.server import ServerStatus, SonarQubeServer

CLOSED_PORT = "http://127.0.0.1:9"
PROJECT_NAME = "sinir-testi"
SETTINGS_TEST = ("import unittest\n\nfrom settings import Settings\n\n\nclass SettingsTest(unittest.TestCase):\n"
                 "    def test_unknown_mode_is_refused(self) -> None:\n"
                 "        with self.assertRaises(ValueError):\n"
                 "            Settings({'mode': 'kod'}).concepts()\n"
                 f"        self.assertEqual(len('{'x' * 130}'), 130)\n")
TWO_INVOCATIONS_LINE = 8
LONG_LINE = 10
PROJECT_FILES = {
    "limits.py": "MAX_NESTING = 2  # girinti\n",
    "big.py": "".join(f"x{number} = {number}\n" for number in range(501)),
    "tests/test_settings.py": SETTINGS_TEST,
}


def server() -> SonarQubeServer:
    return SonarQubeServer(SERVER, TOKEN_FILE.read_text(encoding="utf-8").strip())


class StatusTest(unittest.TestCase):
    def test_running_server_is_up(self) -> None:
        self.assertIs(server().status(), ServerStatus.UP)

    def test_unreachable_server_is_down(self) -> None:
        self.assertIs(SonarQubeServer(CLOSED_PORT, "token").status(), ServerStatus.DOWN)


class IssuesTest(unittest.TestCase):
    found: list[tuple[str, str, int]]

    @classmethod
    def setUpClass(cls) -> None:
        with tempfile.TemporaryDirectory() as parent:
            root = Path(parent) / PROJECT_NAME
            write_files(PROJECT_FILES, root)
            project = Project(root, ["tests"])
            server().analyze(project)
        cls.found = [(issue.rule, issue.path, issue.line) for issue in server().issues(project)]

    def test_book_profile_reports_a_one_word_trailing_comment(self) -> None:
        """Varsayılan desen `# girinti`yi serbest bırakırdı; kitabın profili N1 sayar."""
        self.assertIn(("python:S139", "limits.py", 1), self.found)

    def test_general_rules_reach_tests_through_the_second_scan(self) -> None:
        self.assertIn(("python:LineLength", "tests/test_settings.py", LONG_LINE), self.found)

    def test_issue_found_by_both_scans_is_reported_once(self) -> None:
        self.assertEqual(self.found.count(("python:S5778", "tests/test_settings.py", TWO_INVOCATIONS_LINE)), 1)

    def test_file_level_issue_is_placed_on_the_first_line(self) -> None:
        self.assertIn(("python:S104", "big.py", 1), self.found)


if __name__ == "__main__":
    unittest.main()
