import unittest
from pathlib import Path

from export_cards import CardError, check_card

READER = Path("okuyucu")


class CheckCardTest(unittest.TestCase):
    def test_card_without_id_is_rejected(self) -> None:
        with self.assertRaisesRegex(CardError, "id zorunlu"):
            check_card({"pattern": "ADAPTER"}, {}, READER)


if __name__ == "__main__":
    unittest.main()
