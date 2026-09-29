"""Prosedürel (Bl.6): AST düğümlerine sorulan genel sorular.
AST, Python'un sabit düğüm türlerinden oluşan bir veri yapısıdır; türler değişmez, sorular çoğalır.
Bl.6'ya göre bu durumda veri yapısı + fonksiyon seçilir. Tür dallanması Python'un `isinstance`'ına aittir.
"""
import ast
from collections.abc import Iterator, Sequence
from typing import TypeGuard

FUNCTION_NODES = (ast.FunctionDef, ast.AsyncFunctionDef)
NESTED_SCOPES = FUNCTION_NODES + (ast.ClassDef, ast.Lambda)
BLOCK_NODES = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try, ast.Match)
OPTIONAL_FORMS = frozenset({"Optional", "Union"})
FunctionNode = ast.FunctionDef | ast.AsyncFunctionDef
Definition = FunctionNode | ast.ClassDef


def walk_own(scope: FunctionNode) -> Iterator[ast.AST]:
    """Kapsamın kendi düğümleri; iç içe fonksiyona, sınıfa ve lambda'ya inilmez."""
    stack: list[ast.AST] = [node for node in scope.body if not isinstance(node, NESTED_SCOPES)]
    while stack:
        node = stack.pop()
        yield node
        stack += [child for child in ast.iter_child_nodes(node) if not isinstance(child, NESTED_SCOPES)]


def nesting(node: ast.AST, depth: int = 0) -> int:
    children = [child for child in ast.iter_child_nodes(node) if not isinstance(child, NESTED_SCOPES)]
    return max((nesting(child, depth + isinstance(child, BLOCK_NODES)) for child in children), default=depth)


def is_name(node: ast.AST | None, name: str) -> TypeGuard[ast.Name]:
    return isinstance(node, ast.Name) and node.id == name


def is_class_name(name: str) -> bool:
    """Sınıf adı büyük harfle başlar (PEP 8); sabitler de tümü büyük harfle yazıldığı için ayrılır.
    Modüle özel sınıfın (`_Parser`) baştaki alt çizgisi adın biçimini değiştirmez."""
    public_name = name.lstrip("_")
    return public_name[:1].isupper() and not public_name.isupper()


def is_self_attribute(node: ast.AST | None) -> TypeGuard[ast.Attribute]:
    return isinstance(node, ast.Attribute) and is_name(node.value, "self")


def self_attributes(node: ast.AST) -> set[str]:
    return {child.attr for child in ast.walk(node) if is_self_attribute(child)}


def assignment_targets(node: ast.AST) -> list[ast.expr]:
    """Atamanın hedefleri; `a, b = ...` demeti tek tek hedeflerine açılır."""
    if isinstance(node, ast.Assign):
        return [target for written in node.targets for target in _unpacked(written)]
    return [node.target] if isinstance(node, (ast.AugAssign, ast.AnnAssign)) else []


def _unpacked(target: ast.expr) -> list[ast.expr]:
    if isinstance(target, (ast.Tuple, ast.List)):
        return [inner for element in target.elts for inner in _unpacked(element)]
    return _unpacked(target.value) if isinstance(target, ast.Starred) else [target]


def root_name(node: ast.expr) -> str:
    """`a.b[c].d` → `a`; kök bir ad değilse boş."""
    while isinstance(node, (ast.Attribute, ast.Subscript)):
        node = node.value
    return node.id if isinstance(node, ast.Name) else ""


def last_name(node: ast.expr) -> str:
    """`a.b.c` → `c`, `c` → `c`; ad değilse boş."""
    if isinstance(node, ast.Attribute):
        return node.attr
    return node.id if isinstance(node, ast.Name) else ""


def end_line(node: ast.stmt | ast.expr) -> int:
    """Düğümün bittiği satır. Ayrıştırılmış kodda hep vardır; yoksa başladığı satır sayılır."""
    return node.end_lineno if node.end_lineno is not None else node.lineno


def end_position(node: ast.stmt | ast.expr) -> tuple[int, int]:
    """Düğümün bittiği (satır, sütun); sütun yoksa başladığı sütun sayılır."""
    return end_line(node), node.end_col_offset if node.end_col_offset is not None else node.col_offset


def is_none(node: ast.AST | None) -> bool:
    return isinstance(node, ast.Constant) and node.value is None


def admits_none(annotation: ast.expr) -> bool:
    """Türün en dış düzeyi None'a izin veriyor mu: `None`, `X | None`, `Optional[X]`, `Union[X, None]`.
    Kabın içindeki None (`list[X | None]`) sayılmaz: kap boş dönmez."""
    if isinstance(annotation, ast.BinOp) and isinstance(annotation.op, ast.BitOr):
        return admits_none(annotation.left) or admits_none(annotation.right)
    if isinstance(annotation, ast.Subscript) and last_name(annotation.value) in OPTIONAL_FORMS:
        return last_name(annotation.value) == "Optional" or any(map(admits_none, _unpacked(annotation.slice)))
    return is_none(annotation)


def is_string_literal(node: ast.AST | None) -> bool:
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        return all(is_string_literal(element) for element in node.elts)
    return isinstance(node, ast.Constant) and isinstance(node.value, str)


def is_empty_body(statements: Sequence[ast.stmt]) -> bool:
    """Yalnız `pass`, `...` ya da belge dizgisinden oluşan gövde."""
    return all(isinstance(statement, ast.Pass) or _is_constant_expression(statement) for statement in statements)


def _is_constant_expression(statement: ast.stmt) -> bool:
    return isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Constant)
