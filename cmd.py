#!/bin/env python3
# SPDX-FileCopyrightText: 2024, Jakob Bornecrantz.
# SPDX-License-Identifier: MIT OR Apache-2.0 OR BSL-1.0

import sys
import os

def get_script_dir():
    absolute_script_path = os.path.abspath(__file__)
    absolute_dir = os.path.dirname(absolute_script_path)
    return absolute_dir

def get_path_in_script_dir(*paths):
    tmp = get_script_dir()
    for path in paths:
        tmp = os.path.join(tmp, path)
    return tmp

# Setup sys path so we can import our helpers
sys.path.insert(0, get_path_in_script_dir('src'))


from clang.cindex import Index, TranslationUnit, Cursor, CursorKind, Type, TypeKind
from dataclasses import dataclass

import crosse.llvm
import crosse.lang.d
import crosse.lang.volt
from crosse.objects import *
from crosse.clang import is_function_declaration, is_enum_declaration


# Shared between for all runs.
index: Index
index = Index.create()


####
# Functions
#

def create_enum(cursor: Cursor, language: str) -> Enum:
    if language == 'volt':
        return crosse.lang.volt.create_enum(cursor)
    elif language == 'd':
        return crosse.lang.d.create_enum(cursor)
    else:
        raise "Error"


def create_function(cursor: Cursor, language: str) -> Function:
    if language == 'volt':
        return crosse.lang.volt.create_function(cursor)
    elif language == 'd':
        return crosse.lang.d.create_function(cursor)
    else:
        raise "Error"


def create_modules() -> dict[str, Module]:
    module_names = {
        'Analysis',
        'BitReader',
        'BitWriter',
        'Comdat',
        'Core',
        'DebugInfo',
        'ErrorHandling',
        'ExecutionEngine',
        'Initialization',
        'Linker',
        'Support',
        'Target',
        'TargetMachine',
        'Types',
    }
    ret = dict()

    for name in module_names:
        ret[name] = Module(name)

    return ret


def create_empty_range(first: int, to_non_inclusive: int):
    return Range(start = first, end = to_non_inclusive - 1, decl = None)


def add_declaration_to_module(first: int, version: int, module: Module, decl: Declaration):

    s: Symbol
    if not decl.name in module.symbols:
        s = Symbol(decl.name)
        module.symbols[decl.name] = s
    else:
        s = module.symbols[decl.name]

    if len(s.ranges) == 0:
        # First time seeing this symbole.
        if first < version:
            s.ranges.append(create_empty_range(first, version))
            print("LLVM {} introduced {} {}.{}".format(version, decl.kind_str, module.name, decl.name))
        s.ranges.append(Range(version, version, decl))
        return

    r = s.ranges[-1]
    assert(r.decl != None)

    if r.decl.type_str == decl.type_str:
        # decl appears again, set the latest version.
        # Also use the latest decl if the argument names have been fixed.
        assert(r.end < version)
        r.end = version
        r.decl = decl
        return

    r.decl.end = version - 1
    s.ranges.append(Range(version, version, decl))

    print("LLVM {} changed {} {}.{}".format(version, decl.kind_str, module.name, decl.name))


def depricate_module_declarations(version: int, module: Module):

    for symbol in module.symbols.values():
        r = symbol.ranges[-1]
        assert(r.end <= version)

        if r.end == version:
            continue

        if r.decl == None:
            # Already has no function, up the version.
            r.end = version
            continue

        # This function wasn't been added in this version, remove it.
        print('LLVM {} removed {} {}.{}'.format(version, r.decl.kind_str, module.name, r.decl.name))
        symbol.ranges.append(Range(version, version, None))


def parse(version: int) -> TranslationUnit:
    # Hard coded system dir.
    system_include_dir = '/usr/lib/clang/14.0.0/include/'

    # Common config and other files.
    llvm_common_dir = get_path_in_script_dir('input', 'llvm', 'common')

    # Where is the interface headers.
    llvm_c_dir = get_path_in_script_dir('input', 'llvm', 'llvm-{}'.format(version))

    # Includes all of the headers.
    includer_file = get_path_in_script_dir('input', 'llvm', 'includer.c')

    translation_unit = index.parse(
        includer_file,
        args=[
            '-xc',
            '-DCROSSE_LLVM_VERSION={}'.format(version),
            '-I', system_include_dir,
            '-I', llvm_common_dir,
            '-I', llvm_c_dir,
        ])

    for diag in translation_unit.diagnostics:
        print(diag)

    return translation_unit


def write_declaration(file, decl: Declaration, indent: str):
    lines = str.split(decl.d_decl, '\n')
    for line in lines:
        file.write('{}{}\n'.format(indent, line))


def write_symbol_declaration(file, first: int, symbol: Symbol, language: str):
    # Simple, the symbol stayed the same through all version.
    if len(symbol.ranges) == 1:
        write_declaration(file, symbol.ranges[0].decl, '')
        return

    first = symbol.ranges[0]
    last = symbol.ranges[-1]

    # Prettier output for a symbol that is depricated, only works in Volt.
    if language == 'volt':
        if len(symbol.ranges) == 2 and last.decl == None:
            # There from the start, removed in a later version.
            assert(first.decl != None)
            file.write('version(!LLVMVersion{}AndAbove) {}\n'.format(last.start, '{'))
            write_declaration(file, first.decl, '\t')
            file.write('}\n')
            return

    # Go through the ranges and print the symbols as they change.
    for r in reversed(symbol.ranges):
        d = r.decl
        if r == last:
            file.write('version(LLVMVersion{}AndAbove) {}\n'.format(r.start, '{'))
            if d == None:
                file.write('\t// Removed\n')
            else:
                write_declaration(file, d, '\t')
        elif r == first:
            if d == None:
                file.write('}\n')
            else:
                file.write('} else {\n')
                write_declaration(file, d, '\t')
                file.write('}\n')
        else:
            file.write('{} else version(LLVMVersion{}AndAbove) {}\n'.format('}', r.start, '{'))
            if d == None:
                file.write('\t// Removed\n')
            else:
                write_declaration(file, d, '\t')
    return


if __name__ == '__main__':

    first = 10
    last = 21
    versions = list(range(first, last+1))
    mods = create_modules()
    language = 'd'

    file = sys.stdout

    for version in versions:
        print('Parsing LLVM {}'.format(version))
        translation_unit = parse(version)

        children = translation_unit.cursor.get_children()
        for child in children:

            # Classify declaration.
            is_func = is_function_declaration(child)
            is_enum = is_enum_declaration(child)
    
            # Simple rejection.
            if not is_func and not is_enum:
                continue
    
            # Get the module and if it's a okay declaration.
            ok, mod = crosse.llvm.cursor_file_to_module(child)
            if not ok:
                continue

            # Get the module this symbol refers to.
            m = mods[mod]

            # Skip anonymous enums
            if is_enum and child.is_anonymous():
                continue

            # It's a function, declare it.
            if is_func:
                f = create_function(child, language)
                add_declaration_to_module(first, version, m, f)

            # It's a enum, declare it.
            if is_enum:
                e = create_enum(child, language)
                add_declaration_to_module(first, version, m, e)

        for mod in mods.values():
            depricate_module_declarations(version, mod)

    crosse.llvm.apply_touch_ups(mods)

    for mod in mods.values():
        filename = mod.name + '.' + language
        src_name = get_path_in_script_dir('input', 'llvm', 'templates', language, filename)
        out_name = get_path_in_script_dir('out', filename)

        src = open(src_name, 'r')
        out = open(out_name, 'w')

        # Copy the template
        out.write(src.read())
        src.close()

        for symbol in mod.symbols.values():
            write_symbol_declaration(out, first, symbol, language)

        out.close()
