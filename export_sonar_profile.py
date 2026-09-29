"""Kural tablosundan (sonarqube/rules.py) SonarQube'un Python profilini üretir (tasarım K5).

Formül: Sonar way − kapatılanlar + eşlenenler. Profil elle değiştirilmez; sapmayı öğrenme testi yakalar.
Tabloda sunucunun tanımadığı bir kural varsa hiçbir şey değiştirmeden durur. Profil yoksa Sonar way'den kopyalanır;
sonunda Python'un varsayılan profili olur, yeni projeler onu kendiliğinden alır.
Yönetim yetkisi ister, User Token ile çalışır: python3 export_sonar_profile.py
"""
import sys
from collections.abc import Mapping, Set
from dataclasses import dataclass
from pathlib import Path

from sonarqube.profiles import ProfileError, QualityProfile, SonarQubeProfiles
from sonarqube.rules import BASE_PROFILE, PROFILE, RULES, Parameters
from sonarqube.web import SonarQubeError, WebApi

SERVER = "http://127.0.0.1:9000"
USER_TOKEN = Path.home() / ".config" / "secrets" / "sonarqube-user-token"


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


def export(profiles: SonarQubeProfiles) -> None:
    require_known(profiles.rule_keys())
    ensure_profile(profiles)
    synchronize(profiles.profile(PROFILE), RULES.profile_from(profiles.profile(BASE_PROFILE).active_rules()))
    profiles.make_default(PROFILE)


def require_known(known: Set[str]) -> None:
    unknown = RULES.unknown(known)
    if unknown:
        raise ProfileError(f"tablodaki şu kuralları sunucu tanımıyor: {', '.join(unknown)}")


def ensure_profile(profiles: SonarQubeProfiles) -> None:
    if PROFILE not in profiles.names():
        profiles.profile(BASE_PROFILE).copy_to(PROFILE)


def synchronize(profile: QualityProfile, target: Mapping[str, Parameters]) -> None:
    planned = changes(profile.active_rules(), target)
    apply(planned, profile)
    print(summary(planned))


def apply(planned: ProfileChanges, profile: QualityProfile) -> None:
    for rule, parameters in planned.activate.items():
        profile.activate(rule, parameters)
    for rule in planned.deactivate:
        profile.deactivate(rule)


def summary(planned: ProfileChanges) -> str:
    activated, deactivated = len(planned.activate), len(planned.deactivate)
    return f"'{PROFILE}': {activated} kural açıldı ya da eşiği değişti, {deactivated} kural kapandı."


def main() -> None:
    try:
        export(SonarQubeProfiles(WebApi(SERVER, USER_TOKEN.read_text(encoding="utf-8").strip())))
    except (SonarQubeError, ProfileError, OSError) as error:
        sys.exit(f"Profil üretilemedi: {error}")


if __name__ == "__main__":
    main()
