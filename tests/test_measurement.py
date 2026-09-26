import unittest

from measure.findings import Finding, Location, Note, look, render
from measure.measurement import Measurement
from tests.snippets import Snippet

MEASURED = """
class Report:
    def __init__(self):
        self._rows = []

    def add(self, row, width, strict=False):
        self._rows.append(row)


def total(rows):
    return sum(rows)
"""
ADD_METHOD_LINE = 6
SOME_LINE = 3


class SourceFileTest(unittest.TestCase):
    def test_methods_are_named_after_their_class(self):
        notes = [function.note(look("")) for function in Snippet(MEASURED).functions()]
        self.assertEqual([note.location.name for note in notes], ["total", "Report.__init__", "Report.add"])


class MeasurementTest(unittest.TestCase):
    def test_notes_carry_where_they_were_found(self):
        notes = Measurement([Snippet(MEASURED)]).notes()
        self.assertIn(("Report.add", ADD_METHOD_LINE), [(note.location.name, note.location.line) for note in notes])

    def test_clean_code_gives_no_notes(self):
        self.assertEqual(Measurement([Snippet("def total(rows):\n    return sum(rows)\n")]).notes(), [])

    def test_test_functions_also_pass_the_test_checks(self):
        self.assertNotEqual(Measurement([Snippet("def test_total(self):\n    pass\n")]).notes(), [])

    def test_factories_of_every_measured_source_are_known(self):
        factory = Snippet("class Project:\n    def load(self):\n        return Progress(self)\n")
        user = Snippet("def pages(project):\n    return project.load().pages()\n")
        self.assertEqual(Measurement([factory, user]).notes(), [])

    def test_production_functions_skip_the_test_checks(self):
        self.assertEqual(Measurement([Snippet("def total(self):\n    pass\n")]).notes(), [])


class RenderTest(unittest.TestCase):
    def test_note_reads_like_a_compiler_message(self):
        note = Note(Location("a.py", SOME_LINE, "f"), Finding("ALARM", "iki iş"))
        self.assertEqual(render(note), f"a.py:{SOME_LINE}: ALARM f: iki iş")


if __name__ == "__main__":
    unittest.main()
