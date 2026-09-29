import unittest

from sonarqube.rules import CLOSED, MAPPED, MappedRule, Rules

BASE = {"python:S1172": {}, "python:S1481": {}, "python:LineLength": {"maximumLineLength": "80"}}
RULES = Rules({"python:LineLength": MappedRule("Bl.5 · Horizontal Formatting", {"maximumLineLength": "120"}),
               "python:S139": MappedRule("Bl.2 · N1")},
              {"python:S1172": "polimorfik arayüz parametresini ölü sayar"})


class ProfileTest(unittest.TestCase):
    def test_closed_rule_leaves_the_base(self) -> None:
        self.assertNotIn("python:S1172", RULES.profile_from(BASE))

    def test_other_base_rules_stay_as_they_are(self) -> None:
        self.assertEqual(RULES.profile_from(BASE)["python:S1481"], {})

    def test_mapped_rule_is_added(self) -> None:
        self.assertIn("python:S139", RULES.profile_from(BASE))

    def test_mapped_rule_carries_the_book_threshold(self) -> None:
        self.assertEqual(RULES.profile_from(BASE)["python:LineLength"], {"maximumLineLength": "120"})


class UnknownRulesTest(unittest.TestCase):
    def test_rule_the_server_does_not_know_is_reported(self) -> None:
        self.assertEqual(RULES.unknown({"python:S1172", "python:LineLength"}), ["python:S139"])

    def test_closed_rule_must_be_known_too(self) -> None:
        self.assertEqual(RULES.unknown({"python:S139", "python:LineLength"}), ["python:S1172"])


class RuleTableTest(unittest.TestCase):
    def test_no_rule_is_both_mapped_and_closed(self) -> None:
        self.assertEqual(MAPPED.keys() & CLOSED.keys(), set())


if __name__ == "__main__":
    unittest.main()
