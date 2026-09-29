import unittest

from export_sonar_profile import ProfileChanges, changes

COMMENT_PATTERN = {"legalTrailingCommentPattern": r"^#\s*+noqa\b.*$"}
TARGET = {"python:S139": COMMENT_PATTERN, "python:S1481": {}}
NO_CHANGE = ProfileChanges({}, [])


class ChangesTest(unittest.TestCase):
    def test_profile_that_matches_the_target_needs_no_change(self) -> None:
        self.assertEqual(changes(TARGET, TARGET), NO_CHANGE)

    def test_missing_rule_is_activated(self) -> None:
        self.assertEqual(changes({"python:S1481": {}}, TARGET).activate, {"python:S139": COMMENT_PATTERN})

    def test_rule_outside_the_target_is_deactivated(self) -> None:
        self.assertEqual(changes({**TARGET, "python:S1172": {}}, TARGET).deactivate, ["python:S1172"])

    def test_rule_with_another_threshold_is_activated_again(self) -> None:
        current = {**TARGET, "python:S139": {"legalTrailingCommentPattern": r"^#.*$"}}
        self.assertEqual(changes(current, TARGET).activate, {"python:S139": COMMENT_PATTERN})

    def test_defaults_the_server_adds_are_no_change(self) -> None:
        self.assertEqual(changes({**TARGET, "python:S1481": {"regex": "^_$"}}, TARGET), NO_CHANGE)


if __name__ == "__main__":
    unittest.main()
