/*#D*/
// SPDX-FileCopyrightText: {{ copyright_years }}, LLVM Developers.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

module lib.llvm.c.Core;

public import lib.llvm.c.Types;


enum LLVMAttributeIndex : uint {
	Return = 0U,
	Function = cast(uint)-1,
}


alias LLVMDiagnosticHandler = extern(C) void function(LLVMDiagnosticInfoRef, void *);
alias LLVMYieldCallback = extern(C) void function(LLVMContextRef, void *);


extern(C):

//#--- Auto generated below ---#
