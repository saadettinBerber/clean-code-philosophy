"""Sunucudaki profil kural tablosundan üretilenle aynı mı (tasarım K5 · sapma denetimi).

Profil elle değiştirilirse ya da SonarQube yükseltilip Sonar way değişirse düşer.
Çaresi `python3 export_sonar_profile.py`.
Yalnız okur, Analysis Token yeter:
    python3 -m unittest discover -s learning_tests -t .
"""
import unittest

from export_sonar_profile import ProfileChanges, changes
from learning_tests.scan import SERVER, TOKEN_FILE
from sonarqube.profiles import SonarQubeProfiles
from sonarqube.rules import BASE_PROFILE, PROFILE, RULES
from sonarqube.web import WebApi

NO_DRIFT = ProfileChanges({}, [])


class ProfileDriftTest(unittest.TestCase):
    def test_server_profile_is_the_one_the_rule_table_produces(self) -> None:
        profiles = SonarQubeProfiles(WebApi(SERVER, TOKEN_FILE.read_text(encoding="utf-8").strip()))
        target = RULES.profile_from(profiles.profile(BASE_PROFILE).active_rules())
        self.assertEqual(changes(profiles.profile(PROFILE).active_rules(), target), NO_DRIFT)


if __name__ == "__main__":
    unittest.main()
