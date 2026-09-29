"""zihin-haritasi.md'yi kitap okuyucusuna data/mindmap.js olarak aktarır.

Okuyucu file:// ile de açılır; orada fetch çalışmadığı için Markdown bir JS değişkenine gömülür.
Kullanım: python3 export_map.py [okuyucu-klasörü]
"""
import json
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "zihin-haritasi.md"
DEFAULT_READER = Path.home() / "Desktop" / "Clean Code" / "kitap"
TARGET_IN_READER = Path("data") / "mindmap.js"
HEADER = "// ÜRETİLİR: 'Clean Code/felsefe/export_map.py' yazar, elle düzenlenmez. Kaynak: zihin-haritasi.md\n"


def reader_root() -> Path:
    return Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_READER


def render(markdown: str) -> str:
    return f"{HEADER}window.MINDMAP_SOURCE = {json.dumps(markdown, ensure_ascii=False)};\n"


def main() -> None:
    root = reader_root()
    if not (root / "index.html").is_file():
        sys.exit(f"Okuyucu bulunamadı: {root}")
    target = root / TARGET_IN_READER
    target.write_text(render(SOURCE.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"{SOURCE.name} → {target}")


if __name__ == "__main__":
    main()
