"""Prosedürel (Bl.6): AST düğümlerine sorulan genel sorular.
AST, Python'un sabit düğüm türlerinden oluşan bir veri yapısıdır; türler değişmez, sorular çoğalır.
Bl.6'ya göre bu durumda veri yapısı + fonksiyon seçilir. Tür dallanması Python'un `isinstance`'ına aittir.
"""
import ast

FUNCTION_NODES = (ast.FunctionDef, ast.AsyncFunctionDef)
NESTED_SCOPES = FUNCTION_NODES + (ast.ClassDef, ast.Lambda)
BLOCK_NODES = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try, ast.Match)


def walk_own(scope):
    """Kapsamın kendi düğümleri; iç içe fonksiyona, sınıfa ve lambda'ya inilmez."""
    stack = [node for node in scope.body if not isinstance(node, NESTED_SCOPES)]
    while stack:
        node = stack.pop()
        yield node
        stack += [child for child in ast.iter_child_nodes(node) if not isinstance(child, NESTED_SCOPES)]


def nesting(node, depth=0):
    children = [child for child in ast.iter_child_nodes(node) if not isinstance(child, NESTED_SCOPES)]
    return max((nesting(child, depth + isinstance(child, BLOCK_NODES)) for child in children), default=depth)


def is_name(node, name):
    return isinstance(node, ast.Name) and node.id == name


def is_self_attribute(node):
    return isinstance(node, ast.Attribute) and is_name(node.value, "self")


def self_attributes(node):
    return {child.attr for child in ast.walk(node) if is_self_attribute(child)}


def assignment_targets(node):
    if isinstance(node, ast.Assign):
        return node.targets
    return [node.target] if isinstance(node, (ast.AugAssign, ast.AnnAssign)) else []


def root_name(node):
    """`a.b[c].d` → `a`; kök bir ad değilse boş."""
    while isinstance(node, (ast.Attribute, ast.Subscript)):
        node = node.value
    return node.id if isinstance(node, ast.Name) else ""


def last_name(node):
    """`a.b.c` → `c`, `c` → `c`; ad değilse boş."""
    if isinstance(node, ast.Attribute):
        return node.attr
    return node.id if isinstance(node, ast.Name) else ""


def is_none(node):
    return isinstance(node, ast.Constant) and node.value is None


def is_string_literal(node):
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        return all(is_string_literal(element) for element in node.elts)
    return isinstance(node, ast.Constant) and isinstance(node.value, str)


def is_empty_body(statements):
    """Yalnız `pass`, `...` ya da belge dizgisinden oluşan gövde."""
    return all(isinstance(statement, ast.Pass) or _is_constant_expression(statement) for statement in statements)


def _is_constant_expression(statement):
    return isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Constant)
