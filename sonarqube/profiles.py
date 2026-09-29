"""SonarQube'un Python kalite profilleri: tablodan üretilen profilin okunması ve yazılması (tasarım K5).

Okumak Analysis Token'la olur; yazmak yönetim yetkisi, yani User Token ister.
"""
from sonarqube.rules import Parameters
from sonarqube.web import Json, WebApi

LANGUAGE = "py"
RULE_SEARCH = "api/rules/search"


class ProfileError(Exception):
    """Profil bulunamadı ya da tablodan üretilemez."""


class QualityProfile:
    """Sunucudaki tek profil."""

    def __init__(self, web: WebApi, key: str) -> None:
        self._web = web
        self._key = key

    def active_rules(self) -> dict[str, Parameters]:
        """Profilde açık kurallar ve eşikleri."""
        pages = self._web.pages(RULE_SEARCH, {"qprofile": self._key, "activation": "true", "f": "actives"})
        return {rule: _parameters(activations) for page in pages for rule, activations in page["actives"].items()}

    def activate(self, rule: str, parameters: Parameters) -> None:
        """Kuralı açar ya da eşiğini değiştirir; eşik verilmezse kuralın varsayılanı geçer."""
        joined = ";".join(f"{name}={value}" for name, value in parameters.items())
        self._web.post("api/qualityprofiles/activate_rule", {"key": self._key, "rule": rule, "params": joined})

    def deactivate(self, rule: str) -> None:
        self._web.post("api/qualityprofiles/deactivate_rule", {"key": self._key, "rule": rule})

    def copy_to(self, name: str) -> None:
        """Bütün kurallarıyla ve önem dereceleriyle yeni bir profile kopyalar."""
        self._web.post("api/qualityprofiles/copy", {"fromKey": self._key, "toName": name})


class SonarQubeProfiles:
    """Sunucunun Python profilleri ve tanıdığı kurallar."""

    def __init__(self, web: WebApi) -> None:
        self._web = web

    def names(self) -> set[str]:
        return set(self._keys())

    def profile(self, name: str) -> QualityProfile:
        keys = self._keys()
        if name not in keys:
            raise ProfileError(f"sunucuda '{name}' profili yok")
        return QualityProfile(self._web, keys[name])

    def make_default(self, name: str) -> None:
        """Proje başka bir profile bağlanmadıkça ilk taramada bu profili alır."""
        self._web.post("api/qualityprofiles/set_default", {"language": LANGUAGE, "qualityProfile": name})

    def rule_keys(self) -> set[str]:
        """Sunucunun tanıdığı Python kuralları."""
        return {str(rule["key"]) for page in self._web.pages(RULE_SEARCH, {"languages": LANGUAGE, "f": "name"})
                for rule in page["rules"]}

    def _keys(self) -> dict[str, str]:
        found = self._web.get("api/qualityprofiles/search", {"language": LANGUAGE})
        return {str(profile["name"]): str(profile["key"]) for profile in found["profiles"]}


def _parameters(activations: list[Json]) -> Parameters:
    """Profil sorulduğu için kuralın tek etkinleştirmesi vardır."""
    [activation] = activations
    return {str(parameter["key"]): str(parameter["value"]) for parameter in activation["params"]}
