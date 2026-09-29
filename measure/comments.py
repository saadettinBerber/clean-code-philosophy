"""Kaynağın yorumları. Dizgilerin içindeki `#` yorum sayılmaz; yorum dizgeciği (token) okunur."""
import io
import re
import tokenize
from collections.abc import Sequence
from itertools import groupby
from typing import NamedTuple

from measure.findings import Location
from measure.scope import Scope

COMMENT_PREFIX = re.compile(r"^#\s?")
COMMENTS_SUBJECT = "yorum"


class Comment(NamedTuple):
    location: Location
    text: str


class Comments:
    """Bir kaynağın yorumları, yerleriyle birlikte."""

    def __init__(self, scope: Scope, text: str) -> None:
        self._scope = scope
        self._text = text

    def all(self) -> list[Comment]:
        """Her yorum; `#` atılmış."""
        return [self._located(*_numbered(token)) for token in self._tokens()]

    def blocks(self) -> list[Comment]:
        """Ardışık satırlardaki tam satır yorumlar tek blok olur; yeri ilk satırıdır."""
        full_lines = [_numbered(token) for token in self._tokens() if token.line.lstrip().startswith("#")]
        runs = groupby(enumerate(full_lines), key=lambda pair: pair[1][0] - pair[0])
        return [self._located(*_joined([comment for _, comment in run])) for _, run in runs]

    def _located(self, line: int, text: str) -> Comment:
        return Comment(self._scope.location_at(line, COMMENTS_SUBJECT), text)

    def _tokens(self) -> list[tokenize.TokenInfo]:
        tokens = tokenize.generate_tokens(io.StringIO(self._text).readline)
        return [token for token in tokens if token.type == tokenize.COMMENT]


def _numbered(token: tokenize.TokenInfo) -> tuple[int, str]:
    return token.start[0], COMMENT_PREFIX.sub("", token.string)


def _joined(run: Sequence[tuple[int, str]]) -> tuple[int, str]:
    return run[0][0], "\n".join(content for _, content in run)
