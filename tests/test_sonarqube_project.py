import unittest
from pathlib import Path

from sonarqube.project import Project

PROJECT = Project(Path("/depo/felsefe"), ["tests", "learning_tests"])


class ProjectTest(unittest.TestCase):
    def test_key_is_the_name_of_the_root(self) -> None:
        self.assertEqual(PROJECT.keys(), ("felsefe", "felsefe-testler"))

    def test_main_scan_declares_test_folders_as_tests(self) -> None:
        self.assertEqual(main_scan()["sonar.tests"], "tests,learning_tests")

    def test_main_scan_leaves_test_folders_out_of_sources(self) -> None:
        self.assertEqual(main_scan()["sonar.exclusions"], "tests/**,learning_tests/**")

    def test_second_scan_declares_test_folders_as_sources(self) -> None:
        [_, tests] = PROJECT.scans()
        self.assertEqual(tests, {"sonar.projectKey": "felsefe-testler", "sonar.sources": "tests,learning_tests"})


def main_scan() -> dict[str, str]:
    [main, _] = PROJECT.scans()
    return main


if __name__ == "__main__":
    unittest.main()
