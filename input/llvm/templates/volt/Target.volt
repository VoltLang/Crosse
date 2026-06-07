// SPDX-FileCopyrightText: {{ copyright_years }}, LLVM Developers.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

module lib.llvm.c.Target;

public import lib.llvm.c.Types;


struct LLVMTargetData {} alias  LLVMTargetDataRef = LLVMTargetData*;
struct LLVMTargetLibraryInfo {} alias  LLVMTargetLibraryInfoRef = LLVMTargetLibraryInfo*;


extern(C):

//#--- Auto generated below ---#
