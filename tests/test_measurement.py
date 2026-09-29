import unittest

from measure.findings import Finding, Location, Note, look, render
from measure.measurement import Measurement
from tests.snippets import Snippet, names

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
PROJECT_PATH = "proje.py"
CLEAN = "def total(rows: list[int]) -> int:\n    return sum(rows)\n"


def switching(name: str) -> str:
    return (f'def {name}(shape: Shape) -> int:\n    if shape.kind == "circle":\n        return 1\n'
            '    elif shape.kind == "square":\n        return 2\n')


class SourceFileTest(unittest.TestCase):
    def test_methods_are_named_after_their_class(self) -> None:
        notes = [function.note(look("")) for function in Snippet(MEASURED).functions()]
        self.assertEqual([note.location.name for note in notes], ["total", "Report.__init__", "Report.add"])


class MeasurementTest(unittest.TestCase):
    def test_notes_carry_where_they_were_found(self) -> None:
        notes = Measurement([Snippet(MEASURED)]).notes()
        self.assertIn(("Report.add", ADD_METHOD_LINE), [(note.location.name, note.location.line) for note in notes])

    def test_clean_code_gives_no_notes(self) -> None:
        self.assertEqual(Measurement([Snippet(CLEAN)]).notes(), [])

    def test_test_functions_also_pass_the_test_checks(self) -> None:
        self.assertNotEqual(Measurement([Snippet("def test_total(self):\n    pass\n")]).notes(), [])

    def test_factories_of_every_measured_source_are_known(self) -> None:
        factory = Snippet("class Project:\n    def load(self) -> Progress:\n        return Progress(self)\n")
        user = Snippet("def pages(project: Project) -> list[Page]:\n    return project.load().pages()\n")
        self.assertEqual(Measurement([factory, user]).notes(), [])

    def test_production_functions_skip_the_test_checks(self) -> None:
        self.assertEqual(Measurement([Snippet("def total(self) -> None:\n    pass\n")]).notes(), [])


class ProjectTest(unittest.TestCase):
    """Proje kaynakları yalnız bilinir: dosya ötesi bilgi onlardan gelir, notları yazılmaz."""

    def test_unmeasured_project_sources_get_no_notes(self) -> None:
        project = Snippet("def f(a, b, c, d):\n    return a\n", path=PROJECT_PATH)
        self.assertEqual(Measurement([Snippet(CLEAN)], [project]).notes(), [])

    def test_factories_of_the_project_are_known(self) -> None:
        factory = Snippet("class Project:\n    def load(self) -> Progress:\n        return Progress(self)\n",
                          path=PROJECT_PATH)
        user = Snippet("def pages(project: Project) -> list[Page]:\n    return project.load().pages()\n")
        self.assertEqual(Measurement([user], [factory]).notes(), [])

    def test_switch_on_the_same_field_in_the_project_counts(self) -> None:
        project = Snippet(switching("perimeter"), path=PROJECT_PATH)
        self.assertEqual(names(Measurement([Snippet(switching("area"))], [project]).notes()), ["area"])

    def test_measured_source_also_given_as_project_is_counted_once(self) -> None:
        source = Snippet(switching("area"))
        self.assertEqual(Measurement([source], [source]).notes(), [])


class RenderTest(unittest.TestCase):
    def test_note_reads_like_a_compiler_message(self) -> None:
        note = Note(Location("a.py", SOME_LINE, "f"), Finding("ALARM", "iki iş"))
        self.assertEqual(render(note), f"a.py:{SOME_LINE}: ALARM f: iki iş")


if __name__ == "__main__":
    unittest.main()
