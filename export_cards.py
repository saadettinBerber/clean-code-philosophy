"""kitap-disi-kartlar.json'u kitap okuyucusuna data/offbook.js olarak aktarır.

Kartlar zihin haritasındaki ◇ kalıplarla birebir eşleşmek zorundadır; eşleşmezse
ya da bir kart eksik alanlıysa aktarım hiçbir şey yazmadan durur.
Kullanım: python3 export_cards.py [okuyucu-klasörü]
"""
import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
CARDS_SOURCE = HERE / "kitap-disi-kartlar.json"
MIND_MAP = HERE / "zihin-haritasi.md"
DEFAULT_READER = Path.home() / "Desktop" / "Clean Code" / "kitap"
TARGET_IN_READER = Path("data") / "offbook.js"
READER_PAGE = "data/pages/page-{}.js"
HEADER = "// ÜRETİLİR: 'Clean Code/felsefe/export_cards.py' yazar, elle düzenlenmez. Kaynak: kitap-disi-kartlar.json\n"
OFFBOOK_MARK = "◇"
PATTERN_AFTER_ARROW = re.compile(r"→\s*([A-Z][A-Z ]*[A-Z])")
LANGS = ("en", "tr")
BILINGUAL_FIELDS = ("title", "summary", "tip")
CODE_SAMPLES = ("bad", "good")
# JSON kaynağından okunan nesne; alanları kaynağa göre değişir, doğrulama `validate`dedir.
Json = dict[str, Any]


class CardError(Exception):
    """Kart kaynağı okuyucuya aktarılamayacak durumda."""


def reader_root() -> Path:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_READER
    if not (root / "index.html").is_file():
        raise CardError(f"Okuyucu bulunamadı: {root}")
    return root


def offbook_patterns_in_map() -> set[str]:
    leaves = [line for line in MIND_MAP.read_text(encoding="utf-8").splitlines() if OFFBOOK_MARK in line]
    return {match.group(1) for line in leaves for match in PATTERN_AFTER_ARROW.finditer(line)}


def require_bilingual(unit: object, where: str) -> None:
    for lang in LANGS:
        if not isinstance(unit, dict) or not str(unit.get(lang, "")).strip():
            raise CardError(f"{where}: '{lang}' metni eksik")


def check_sample(sample: object, where: str) -> None:
    if not isinstance(sample, dict) or not sample.get("lang") or not sample.get("code"):
        raise CardError(f"{where}: lang ve code zorunlu")
    require_bilingual(sample.get("why"), f"{where}.why")


def check_related(card: Json, reader: Path) -> None:
    for link in card.get("related", []):
        require_bilingual(link, f"{card['id']}.related")
        if not (reader / READER_PAGE.format(link.get("page"))).is_file():
            raise CardError(f"{card['id']}: okuyucuda sayfa {link.get('page')} yok")


def required_id(found: object) -> str:
    """Kart kimliği zorunludur: tekrar denetimi ve okuyucu kartı onunla tanır."""
    if not found:
        raise CardError("<kimliksiz kart>: id zorunlu")
    return str(found)


def check_card(card: Json, sources: Json, reader: Path) -> None:
    card_id = required_id(card.get("id"))
    if not card.get("pattern"):
        raise CardError(f"{card_id}: pattern zorunlu")
    if card.get("source") not in sources:
        raise CardError(f"{card_id}: bilinmeyen kaynak '{card.get('source')}'")
    for field in BILINGUAL_FIELDS:
        require_bilingual(card.get(field), f"{card_id}.{field}")
    for sample in CODE_SAMPLES:
        check_sample(card.get(sample), f"{card_id}.{sample}")
    check_related(card, reader)


def all_cards(document: Json) -> list[Json]:
    return [card for group in document["groups"] for card in group["cards"]]


def check_unique_ids(cards: list[Json]) -> None:
    ids = [card["id"] for card in cards]
    duplicates = sorted({card_id for card_id in ids if ids.count(card_id) > 1})
    if duplicates:
        raise CardError(f"Tekrarlanan kart kimlikleri: {', '.join(duplicates)}")


def check_matches_map(cards: list[Json]) -> None:
    in_cards = {card["pattern"] for card in cards}
    in_map = offbook_patterns_in_map()
    if in_cards != in_map:
        raise CardError(f"Haritada kartı olmayan: {sorted(in_map - in_cards)}; "
                        f"kartı olup haritada olmayan: {sorted(in_cards - in_map)}")


def validate(document: Json, reader: Path) -> None:
    cards = all_cards(document)
    for group in document["groups"]:
        require_bilingual(group.get("title"), f"grup {group.get('id')}")
    for card in cards:
        check_card(card, document["sources"], reader)
    check_unique_ids(cards)
    check_matches_map(cards)


def joined_code(sample: Json) -> Json:
    code = sample["code"]
    return {**sample, "code": "\n".join(code) if isinstance(code, list) else code}


def export_card(card: Json, sources: Json) -> Json:
    exported = {**card, "source": sources[card["source"]], "offbook": True}
    for sample in CODE_SAMPLES:
        exported[sample] = joined_code(card[sample])
    return exported


def export_document(document: Json) -> Json:
    sources = document["sources"]
    groups = [{"id": g["id"], "title": g["title"], "cards": [export_card(c, sources) for c in g["cards"]]}
              for g in document["groups"]]
    return {"mark": OFFBOOK_MARK, "groups": groups}


def render(exported: Json) -> str:
    return f"{HEADER}window.OFFBOOK = {json.dumps(exported, ensure_ascii=False, indent=1)};\n"


def main() -> None:
    try:
        reader = reader_root()
        document = json.loads(CARDS_SOURCE.read_text(encoding="utf-8"))
        validate(document, reader)
    except (CardError, json.JSONDecodeError) as error:
        sys.exit(f"Aktarım durdu: {error}")
    target = reader / TARGET_IN_READER
    target.write_text(render(export_document(document)), encoding="utf-8")
    print(f"{CARDS_SOURCE.name} → {target} ({len(all_cards(document))} kart)")


if __name__ == "__main__":
    main()
