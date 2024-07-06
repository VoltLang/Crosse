# SPDX-FileCopyrightText: 2024, Jakob Bornecrantz.
# SPDX-License-Identifier: MIT OR Apache-2.0 OR BSL-1.0

import clang.cindex

def is_function_declaration(node: clang.cindex.Cursor) -> bool:
    if node.kind != clang.cindex.CursorKind.FUNCTION_DECL:
        return False
    return True

def is_enum_declaration(node: clang.cindex.Cursor) -> bool:
    if node.kind != clang.cindex.CursorKind.ENUM_DECL:
        return False
    return True

def is_enum_typedef_declaration(node: clang.cindex.Cursor) -> bool:
    if node.kind != clang.cindex.CursorKind.TYPEDEF_DECL:
        return False

    c = list(node.get_children())
    if len(c) == 1 and c[0].kind == clang.cindex.CursorKind.ENUM_DECL:
        return True

    return False
