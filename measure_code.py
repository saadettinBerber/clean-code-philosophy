"""Clean Code ölçümü. Yazılmış kodda nereye bakılması gerektiğini söyler; eşik alarmdır, ölçüt değildir.
Her ALARM okunarak "gerçek, düzeltildi" ya da "yanlış pozitif, çünkü…" diye karara bağlanır
(tamam-tanimi.md, §0 madde 6).

Kullanım: python3 measure_code.py [--project KÖK] <dosya ya da dizin> ...

Not yalnız verilen dosyalara yazılır. Proje kökündeki öbür kaynaklar da okunur, çünkü fabrikalar ve switch'ler
dosya ötesi bilgidir. Kök varsayılan olarak çalışma dizinidir.
"""
import argparse
import os
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path, PurePath

from measure.findings import Note, render
from measure.measurement import Measurement
from measure.source_file import SourceFile

PYTHON_FILES = "*.py"
HIDDEN_PREFIX = "."


def main() -> None:
    for note in notes(parsed(sys.argv[1:])):
        print(render(note))


def parsed(arguments: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean Code ölçümü; çıktı alarmdır, okunarak karara bağlanır.")
    parser.add_argument("paths", nargs="+", metavar="yol", help="ölçülecek dosya ya da dizin")
    parser.add_argument("--project", dest="project", default=".", metavar="KÖK", help="bilinen kaynakların kökü")
    return parser.parse_args(arguments)


def notes(options: argparse.Namespace) -> list[Note]:
    measured = python_files(options.paths)
    project = unmeasured(python_files([options.project]), measured)
    return Measurement(read(measured), known(project)).notes()


def python_files(arguments: Iterable[str]) -> list[Path]:
    """Dizinler içindeki .py dosyalarına açılır; dosyalar olduğu gibi kalır."""
    paths = [Path(argument) for argument in arguments]
    return [found for path in paths for found in (visible(path.rglob(PYTHON_FILES), path) if path.is_dir() else [path])]


def visible[P: PurePath](found: Iterable[P], root: PurePath) -> list[P]:
    """Kökün altında gizli bir dizinden (`.git`, `.venv`, çalışma ağacı kopyası) geçmeyen yollar."""
    return sorted(path for path in found
                  if not any(part.startswith(HIDDEN_PREFIX) for part in path.relative_to(root).parts))


def unmeasured[P: PurePath](project: Iterable[P], measured: Iterable[PurePath]) -> list[P]:
    """Projenin ölçülmeyen kaynakları; ölçülen dosya başka bir yazımla gelse de ikinci kez okunmaz."""
    taken = {os.path.abspath(path) for path in measured}
    return [path for path in project if os.path.abspath(path) not in taken]


def read(measured: Iterable[Path]) -> list[SourceFile]:
    return [SourceFile.read(path) for path in measured]


def known(project: Iterable[Path]) -> list[SourceFile]:
    return [source for path in project for source in parsed_or_unknown(path)]


def parsed_or_unknown(path: Path) -> list[SourceFile]:
    """Ayrıştırılamayan proje dosyası yalnız bilinmez; adı ve nedeni standart hataya yazılır, ölçüm sürer.
    Ölçülen dosyadaki hata ise ölçümü durdurur (`read`)."""
    try:
        return [SourceFile.read(path)]
    except (SyntaxError, UnicodeDecodeError) as error:
        return unknown(path, error)


def unknown(path: Path, error: Exception) -> list[SourceFile]:
    print(f"{path}: bilinmiyor, ayrıştırılamadı ({type(error).__name__})", file=sys.stderr)
    return []


if __name__ == "__main__":
    main()
