import unittest

from sonarqube.server import ServerStatus, distinct, reported, server_status

TEST_ISSUE = {"rule": "python:S5778", "component": "felsefe-testler:tests/test_a.py", "line": 7,
              "message": "Refactor", "type": "CODE_SMELL"}
FILE_ISSUE = {"rule": "python:S104", "component": "felsefe:measure/big.py", "message": "Too long", "type": "CODE_SMELL"}


class ServerStatusTest(unittest.TestCase):
    def test_up_is_up(self) -> None:
        self.assertIs(server_status("UP"), ServerStatus.UP)

    def test_restarting_server_will_be_up_soon(self) -> None:
        self.assertIs(server_status("RESTARTING"), ServerStatus.STARTING)

    def test_server_waiting_for_a_database_migration_is_down(self) -> None:
        self.assertIs(server_status("DB_MIGRATION_NEEDED"), ServerStatus.DOWN)


class ReportedTest(unittest.TestCase):
    def test_path_is_relative_to_the_project_root(self) -> None:
        self.assertEqual(reported(TEST_ISSUE).path, "tests/test_a.py")

    def test_file_level_issue_is_placed_on_the_first_line(self) -> None:
        self.assertEqual(reported(FILE_ISSUE).line, 1)

    def test_issue_found_by_both_scans_counts_once(self) -> None:
        issue = reported(TEST_ISSUE)
        self.assertEqual(distinct([issue, issue]), [issue])


if __name__ == "__main__":
    unittest.main()
