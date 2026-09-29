"""Pilotun SonarQube keşifleri, gerçek sunucuda (Bl.8 · Learning Tests Are Better Than Free).

Hızlı takıma girmez; SonarQube her güncellendiğinde yeniden koşulur:
    python3 -m unittest discover -s learning_tests -t .
Proje tek taramayla ölçülür; her keşif ayrı bir testtir. Kaynak: sonarqube-pilot-raporu.md §5, §7.
"""
import re
import unittest

from learning_tests.scan import TOKEN_FILE, SonarQube

LONG_LINE = f"TITLE = '{'x' * 130}'\n"
PRODUCTION_NAMED_LIKE_A_TEST = "def checks() -> list[str]:\n    return []\n\n\n" + LONG_LINE
LONG_LINE_NUMBER = 5
TEST_WITH_LONG_LINE = ("import unittest\n\n\nclass TitleTest(unittest.TestCase):\n"
                       "    def test_title(self) -> None:\n"
                       f"        self.assertEqual(len('{'x' * 130}'), 130)\n")
TEST_LONG_LINE_NUMBER = 6
THREE_AND_FOUR_ARGUMENTS = ("def three(a, b, c):\n    return a + b + c\n\n\n"
                            "def four(a, b, c, d):\n    return a + b + c + d\n")
FOUR_ARGUMENTS_LINE = 5
PRICE_TABLE = """def price_table(rows, currency):
    lines = []
    for row in rows:
        net = row.price * row.count
        tax = net * row.tax_rate / 100
        discount = row.discount if row.discount else 0
        gross = net + tax - discount
        label = row.name.strip().title()
        code = row.code.upper()
        lines.append((code, label, net, tax, gross, currency))
    total = sum(row.price * row.count for row in rows)
    taxes = sum(row.price * row.count * row.tax_rate / 100 for row in rows)
    lines.append(("TOPLAM", "", total, taxes, total + taxes, currency))
    return lines
"""
PRICE_TABLE_LINES = len(PRICE_TABLE.splitlines())
PRICE_TABLE_WITH_ITEM = re.sub(r"\brow\b", "item", PRICE_TABLE)

PROJECT_FILES = {
    "src/test_checks.py": PRODUCTION_NAMED_LIKE_A_TEST,
    "tests/test_title.py": TEST_WITH_LONG_LINE,
    "test_sources/test_title.py": TEST_WITH_LONG_LINE,
    "src/arguments.py": THREE_AND_FOUR_ARGUMENTS,
    "src/prices.py": PRICE_TABLE,
    "src/prices_copy.py": PRICE_TABLE,
    "src/prices_with_item.py": PRICE_TABLE_WITH_ITEM,
}


class PilotDiscoveriesTest(unittest.TestCase):
    sonarqube: SonarQube

    @classmethod
    def setUpClass(cls) -> None:
        cls.sonarqube = SonarQube(TOKEN_FILE.read_text(encoding="utf-8").strip())
        cls.sonarqube.analyze(PROJECT_FILES)

    def test_production_file_named_like_a_test_is_measured(self) -> None:
        """Test tahmini kapalıyken `test_*.py` adı üretim dosyasını test yapmaz, kurallar ona uygulanır."""
        self.assertEqual(self.sonarqube.issue_lines("python:LineLength", "src/test_checks.py"), [LONG_LINE_NUMBER])

    def test_rules_skip_files_declared_as_tests(self) -> None:
        """Kural kapsamı varsayılan olarak yalnız üretim kodu (`scope()` → MAIN); arayüz 'ALL' gösterse de."""
        self.assertEqual(self.sonarqube.issue_lines("python:LineLength", "tests/test_title.py"), [])

    def test_rules_apply_to_tests_declared_as_sources(self) -> None:
        """Aynı test dosyası kaynak olarak bildirilince kurallar ona da uygulanır: testler ayrı projede taranır (K7)."""
        lines = self.sonarqube.issue_lines("python:LineLength", "test_sources/test_title.py")
        self.assertEqual(lines, [TEST_LONG_LINE_NUMBER])

    def test_argument_limit_is_the_largest_allowed_count(self) -> None:
        """S107 `max=3`: 3 argümana izin var, 4 bulgu verir. Kitabın "3 argüman alarm" eşiği `max=2` ister."""
        self.assertEqual(self.sonarqube.issue_lines("python:S107", "src/arguments.py"), [FOUR_ARGUMENTS_LINE])

    def test_exact_copy_is_found(self) -> None:
        """CPD token'ları olduğu gibi karşılaştırır; en az 100 token ve 10 satırlık birebir kopya bulunur."""
        self.assertEqual(self.sonarqube.duplicated_lines("src/prices.py"), PRICE_TABLE_LINES)

    def test_copy_with_one_renamed_variable_is_not_found(self) -> None:
        """Adlar normalleştirilmez: tek değişkenin adı değişince kopya görünmez olur; G5 okuma maddesi kalır."""
        self.assertEqual(self.sonarqube.duplicated_lines("src/prices_with_item.py"), 0)


if __name__ == "__main__":
    unittest.main()
