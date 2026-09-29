"""SonarQube'un web API'si: sınır ailesinin ortak kapısı (tasarım K2, K5, Bl.8 · Clean Boundaries).

Token yalnız istek başlığında durur. Sunucunun reddi, isteğin kendisiyle birlikte hataya dönüşür (Bl.7).
"""
import json
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Mapping
from typing import Any

PAGE_SIZE = 500

# Sunucunun JSON cevabı; alanlarını sınır sınıfları okur, dışarı ham sözlük çıkmaz.
Json = dict[str, Any]


class SonarQubeError(Exception):
    """Sunucu isteği reddetti ya da sunucuya ulaşılamadı."""


class Unreachable(SonarQubeError):
    """Sunucuya ulaşılamadı: kapalı ya da adres yanlış."""


class WebApi:
    def __init__(self, url: str, token: str) -> None:
        self._url = url
        self._token = token

    def get(self, api: str, parameters: Mapping[str, str]) -> Json:
        url = f"{self._url}/{api}?{urllib.parse.urlencode(parameters)}"
        return dict(json.loads(self._send(urllib.request.Request(url, headers=self._headers()))))

    def pages(self, api: str, parameters: Mapping[str, str]) -> list[Json]:
        """Sayfalı arama API'sinin bütün sayfaları; kaç sayfa olduğunu ilk sayfanın toplamı söyler."""
        pages = [self.get(api, _page(parameters, 1))]
        return pages + [self.get(api, _page(parameters, number)) for number in range(2, _page_count(pages[0]) + 1)]

    def post(self, api: str, parameters: Mapping[str, str]) -> None:
        form = urllib.parse.urlencode(parameters).encode()
        self._send(urllib.request.Request(f"{self._url}/{api}", data=form, headers=self._headers(), method="POST"))

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token}"}

    def _send(self, request: urllib.request.Request) -> bytes:
        try:
            with urllib.request.urlopen(request) as response:
                return bytes(response.read())
        except urllib.error.HTTPError as error:
            raise SonarQubeError(_refusal(request, error)) from error
        except urllib.error.URLError as error:
            raise Unreachable(f"{self._url} adresine ulaşılamadı: {error.reason}") from error


def _page(parameters: Mapping[str, str], number: int) -> dict[str, str]:
    return {**parameters, "ps": str(PAGE_SIZE), "p": str(number)}


def _page_count(first: Json) -> int:
    return -(-int(first["total"]) // PAGE_SIZE)


def _refusal(request: urllib.request.Request, error: urllib.error.HTTPError) -> str:
    """Reddedilen istek ve sunucunun gerekçesi; token başlıkta durduğu için metne girmez."""
    return f"{request.get_method()} {request.full_url}: {error.code} {error.read().decode()}"
