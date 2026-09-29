"""Çalışma zamanının SonarQube sınırı (tasarım K2): durum, iki tarama, bulgular.

measure_code yalnız bu sınıfı tanır. SonarQube'un JSON'u dışarı çıkmaz, yerine kendi küçük veri yapımız döner
(Bl.8 · Using Third-Party Code).
"""
from enum import Enum

from sonarqube.web import Unreachable, WebApi


class ServerStatus(Enum):
    UP = "UP"
    STARTING = "STARTING"
    DOWN = "DOWN"


# Burada olmayan her durum (DOWN, DB_MIGRATION_NEEDED) sunucunun kullanılamadığını söyler.
STATUSES = {"UP": ServerStatus.UP, "STARTING": ServerStatus.STARTING, "RESTARTING": ServerStatus.STARTING,
            "DB_MIGRATION_RUNNING": ServerStatus.STARTING}


class SonarQubeServer:
    def __init__(self, url: str, token: str) -> None:
        self._web = WebApi(url, token)

    def status(self) -> ServerStatus:
        """Ulaşılamayan sunucu da ayakta değildir (K8)."""
        try:
            return server_status(str(self._web.get("api/system/status", {})["status"]))
        except Unreachable:
            return ServerStatus.DOWN


def server_status(reported: str) -> ServerStatus:
    return STATUSES.get(reported, ServerStatus.DOWN)
