# SPDX-FileCopyrightText: 2024, Jakob Bornecrantz.
# SPDX-License-Identifier: MIT OR Apache-2.0 OR BSL-1.0

import clang.cindex

from crosse.objects import *
import crosse.llvm


def create_volt_and_d_enum(cursor: clang.cindex.Cursor) -> Enum:

    name: str
    raw_members: list[str]
    pretty_members: list[str]
    type_str: str
    decl_str: str

    name = str(cursor.spelling)
    raw_members = list()
    pretty_members = list()

    # Strip away the typedef.
    if cursor.kind == clang.cindex.CursorKind.TYPEDEF_DECL:
        cursor = list(cursor.get_children())[0]

    children = cursor.get_children()
    for child in children:
        mn = crosse.llvm.strip_enum_member_name(name, child.spelling)

        # Used for the type string, doesn't need to be pretty just correct.
        raw_members.append(mn + '=' + str(child.enum_value))

        # What goes into the source.
        pretty_value = crosse.llvm.get_enum_value(name, child)
        pretty_members.append(mn + ' = ' + pretty_value)

    # Used for checking if the enum is the same.
    type_str = str.join('#', raw_members)

    # Pretty, can change with versions.
    decl_str = 'enum ' + name + ' {\n'
    for member in pretty_members:
        decl_str = '{}\t{},\n'.format(decl_str, member)

    decl_str = decl_str + '}'

    return Enum(name = name, type_str = type_str, d_decl = decl_str, volt_decl = decl_str)
