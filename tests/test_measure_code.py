import unittest
from pathlib import PurePosixPath

from measure_code import unmeasured, visible

ROOT = PurePosixPath("proje")


class VisibleTest(unittest.TestCase):
    def test_files_under_hidden_directories_are_skipped(self):
        paths = [ROOT / "a.py", ROOT / ".venv" / "b.py", ROOT / ".kilo" / "kopya" / "c.py"]
        self.assertEqual(visible(paths, ROOT), [ROOT / "a.py"])

    def test_a_hidden_root_given_on_purpose_is_searched(self):
        root = PurePosixPath(".kilo/kopya")
        self.assertEqual(visible([root / "a.py"], root), [root / "a.py"])


class UnmeasuredTest(unittest.TestCase):
    def test_measured_file_is_not_read_again_from_the_project(self):
        project = [PurePosixPath("measure/a.py"), PurePosixPath("measure/b.py")]
        self.assertEqual(unmeasured(project, [PurePosixPath("./measure/a.py")]), [PurePosixPath("measure/b.py")])


if __name__ == "__main__":
    unittest.main()
