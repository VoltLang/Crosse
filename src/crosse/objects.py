# SPDX-FileCopyrightText: 2024, Jakob Bornecrantz.
# SPDX-License-Identifier: MIT OR Apache-2.0 OR BSL-1.0

from dataclasses import dataclass


##
#
@dataclass
class Declaration:
    name: str
    kind_str: str
    type_str: str
    d_decl: str
    volt_decl: str

    def __init__(self, name: str, kind_str: str, type_str: str, d_decl: str, volt_decl: str):
        self.name = name
        self.kind_str = kind_str
        self.type_str = type_str
        self.d_decl = d_decl
        self.volt_decl = volt_decl

##
#
@dataclass
class Function(Declaration):

    def __init__(self, name: str, type_str: str, d_decl: str, volt_decl: str):
        super().__init__(name, 'function', type_str, d_decl, volt_decl)

##
#
@dataclass
class Enum(Declaration):

    def __init__(self, name: str, type_str: str, d_decl: str, volt_decl: str):
        super().__init__(name, 'enum', type_str, d_decl, volt_decl)

##
#
@dataclass
class Range:
    start: int
    end: int
    decl: Declaration

    def __init__(self, start: int, end: int, decl: Declaration):
        self.start = start
        self.end = end
        self.decl = decl

##
#
@dataclass
class Symbol:
    name: str
    ranges: list[Range]

    def __init__(self, name: str):
        self.name = name
        self.ranges = []

##
#
@dataclass
class Module:
    name: str
    symbols: dict[str, Symbol]

    def __init__(self, name: str):
        self.name = name
        self.symbols = dict()
