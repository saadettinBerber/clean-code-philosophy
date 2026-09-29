"""SonarQubeServer gerçek sunucuya karşı (tasarım §7.3 · Bl.8 outbound tests).

Üretim kodunun sınırı kullandığı gibi kullanır; SonarQube yükseltilince öğrenme testleriyle birlikte koşulur:
    python3 -m unittest discover -s learning_tests -t .
"""
import unittest

from learning_tests.scan import SERVER, TOKEN_FILE
from sonarqube.server import ServerStatus, SonarQubeServer

CLOSED_PORT = "http://127.0.0.1:9"


class StatusTest(unittest.TestCase):
    def test_running_server_is_up(self) -> None:
        server = SonarQubeServer(SERVER, TOKEN_FILE.read_text(encoding="utf-8").strip())
        self.assertIs(server.status(), ServerStatus.UP)

    def test_unreachable_server_is_down(self) -> None:
        self.assertIs(SonarQubeServer(CLOSED_PORT, "token").status(), ServerStatus.DOWN)


if __name__ == "__main__":
    unittest.main()
