# SPDX-FileCopyrightText: 2024, Jakob Bornecrantz.
# SPDX-License-Identifier: MIT OR Apache-2.0 OR BSL-1.0

import clang.cindex

from crosse.objects import *
import crosse.llvm
import crosse.lang.shared


def create_enum(cursor: clang.cindex.Cursor) -> Enum:
    return crosse.lang.shared.create_volt_and_d_enum(cursor)

def create_function(cursor: clang.cindex.Cursor) -> Function:

    ret: clang.cindex.Type

    name: str
    ret_str: str
    decl_str: str
    args_str: str

    type_strs: list[str]
    arg_strs: list[str]


    name = str(cursor.spelling)

    type_strs = list()
    arg_strs = list()

    for arg in cursor.get_arguments():
        full: str
        type_str: str
        arg_name: str

        arg_name = arg.spelling
        type_str = crosse.llvm.type_to_d(arg.type)

        if arg_name != None and len(arg_name) > 0:
            full = '{} {}'.format(type_str, arg_name)
        else:
            full = type_str

        type_strs.append(type_str)
        arg_strs.append(full)

    type_str = str.join(', ', type_strs)
    args_str = str.join(', ', arg_strs)

    decl_str = '{}({})'.format(name, args_str)

    ret = cursor.result_type
    if str(ret.spelling) != 'void':
        d_ret_str = crosse.llvm.type_to_d(ret)

        type_str = type_str + '#' + d_ret_str
        decl_str = d_ret_str + ' ' + decl_str
    else:
        decl_str = 'void ' + decl_str

    # Add the final semicolon.
    decl_str = decl_str + ';'

    return Function(name = name, type_str = type_str, d_decl = decl_str, volt_decl = decl_str)
