"""Clean Code ölçümü. Yazılmış kodda nereye bakılması gerektiğini söyler; eşik alarmdır, ölçüt değildir.
Her ALARM okunarak "gerçek, düzeltildi" ya da "yanlış pozitif, çünkü…" diye karara bağlanır
(tamam-tanimi.md, §0 madde 6).

Kullanım: python3 measure_code.py <dosya ya da dizin> ...
"""
import sys
from pathlib import Path

from measure.findings import render
from measure.measurement import Measurement
from measure.source_file import SourceFile

PYTHON_FILES = "*.py"


def python_files(arguments):
    """Dizinler içindeki .py dosyalarına açılır; dosyalar olduğu gibi kalır."""
    paths = [Path(argument) for argument in arguments]
    return [found for path in paths for found in (sorted(path.rglob(PYTHON_FILES)) if path.is_dir() else [path])]


def main():
    sources = [SourceFile.read(path) for path in python_files(sys.argv[1:])]
    for note in Measurement(sources).notes():
        print(render(note))


if __name__ == "__main__":
    main()
