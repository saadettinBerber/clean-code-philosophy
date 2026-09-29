import unittest

from sonarqube.server import ServerStatus, server_status


class ServerStatusTest(unittest.TestCase):
    def test_up_is_up(self) -> None:
        self.assertIs(server_status("UP"), ServerStatus.UP)

    def test_restarting_server_will_be_up_soon(self) -> None:
        self.assertIs(server_status("RESTARTING"), ServerStatus.STARTING)

    def test_server_waiting_for_a_database_migration_is_down(self) -> None:
        self.assertIs(server_status("DB_MIGRATION_NEEDED"), ServerStatus.DOWN)


if __name__ == "__main__":
    unittest.main()
