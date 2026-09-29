"""SonarQube kurallarının kitapla bağı; tek kaynak (tasarım K4). Sunucudaki profil bu tablodan üretilir (K5).

Eşlenen kural kitabın bir maddesini ölçülür yapar; eşiği kitaptan gelir. Kapatılan kural kitapla çelişir ya da
measure_code'un zaten ölçtüğü maddeyi ikinci kez söyler; gerekçesiyle durur. Tamam tanımı kural numarası taşımaz.
"""
from collections.abc import Mapping
from dataclasses import dataclass, field

Parameters = Mapping[str, str]


@dataclass(frozen=True)
class MappedRule:
    """Kitaba bağlanan kural: dayandığı kitap başlığı ve kitaptan gelen eşikleri."""

    source: str
    parameters: Parameters = field(default_factory=dict)


class Rules:
    """Eşlenen ve kapatılan kurallar; profilin formülünü bilir."""

    def __init__(self, mapped: Mapping[str, MappedRule], closed: Mapping[str, str]) -> None:
        self._mapped = mapped
        self._closed = closed

    def profile(self, base: Mapping[str, Parameters]) -> dict[str, Parameters]:
        """Formül (K5): taban profil − kapatılanlar + eşlenenler; eşlenenler kitabın eşikleriyle."""
        kept = {rule: parameters for rule, parameters in base.items() if rule not in self._closed}
        return kept | {rule: mapped.parameters for rule, mapped in self._mapped.items()}


# Tek sözcüklü satır sonu yorumu da N1'dir (`d = 0  # gün`); yalnız S1309'un G4 diye bildirdiği noqa serbest.
MAPPED: Mapping[str, MappedRule] = {
    "python:S139": MappedRule("Bl.2 · Use Intention-Revealing Names; N1",
                              {"legalTrailingCommentPattern": r"^#\s*+noqa\b.*$"}),
    "python:S1309": MappedRule("G4 · Overridden Safeties"),
    "python:NoSonar": MappedRule("G4 · Overridden Safeties"),
    "python:S1845": MappedRule("Bl.2 · Avoid Disinformation"),
    "python:LineLength": MappedRule("Bl.5 · Horizontal Formatting", {"maximumLineLength": "120"}),
    "python:S104": MappedRule("Bl.5 · Vertical Formatting", {"maximum": "500"}),
    "python:S1192": MappedRule("G25 · Replace Magic Numbers with Named Constants"),
}

CLOSED: Mapping[str, str] = {
    "python:S1172": "polimorfik arayüzün istediği parametreyi ölü sayar (Bl.3 · Switch Statements)",
    "python:S2325": "kitap aynı durumu feature envy sayar, metodu taşır (G14, G18)",
    "python:S1720": "zorunlu yorum (Bl.4 · Mandated Comments)",
    "python:S1142": "küçük fonksiyonda erken return serbest (Bl.3 · Structured Programming)",
    "python:S1707": "yorumda yazar bilgisi istenmez (Bl.4 · Attributions and Bylines; C1)",
    "python:S1722": "Python 2 kuralı, Python 3'te anlamsız",
    "python:S138": "measure_code kitabın eşiğiyle ölçüyor (Bl.3 · Small!)",
    "python:S134": "measure_code kitabın eşiğiyle ölçüyor (Bl.3 · Blocks and Indenting)",
    "python:S107": "measure_code kitabın eşiğiyle ölçüyor (Bl.3 · Function Arguments)",
    "python:S6538": "measure_code ölçüyor (Dil eşlemesi · İmza türü)",
    "python:S6540": "measure_code ölçüyor (Dil eşlemesi · İmza türü)",
    "python:S6543": "measure_code ölçüyor (G26; Dil eşlemesi · İmza türü)",
}

RULES = Rules(MAPPED, CLOSED)
