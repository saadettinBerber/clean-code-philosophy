"""Kural tablosundan (sonarqube/rules.py) SonarQube'un Python profilini üretir (tasarım K5).

Formül: Sonar way − kapatılanlar + eşlenenler. Profil elle değiştirilmez; sapmayı öğrenme testi yakalar.
"""
from collections.abc import Mapping
from dataclasses import dataclass

from sonarqube.rules import Parameters


@dataclass(frozen=True)
class ProfileChanges:
    """Sunucudaki profili hedefe getiren değişiklikler: açılacak ya da eşiği değişecek kurallar, kapatılacaklar."""

    activate: Mapping[str, Parameters]
    deactivate: list[str]


def changes(current: Mapping[str, Parameters], target: Mapping[str, Parameters]) -> ProfileChanges:
    """Sunucu her eşiği varsayılanıyla da verir; yalnız hedefin yazdığı eşikler karşılaştırılır."""
    stale = {rule: parameters for rule, parameters in target.items()
             if rule not in current or not parameters.items() <= current[rule].items()}
    return ProfileChanges(stale, sorted(current.keys() - target.keys()))
