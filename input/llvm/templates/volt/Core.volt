// SPDX-FileCopyrightText: 2007-2024, LLVM Developers.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

module lib.llvm.c.Core;

public import lib.llvm.c.Types;


enum LLVMAttributeIndex : uint {
	Return = 0U,
	Function = cast(uint)-1,
}


alias LLVMDiagnosticHandler = extern(C) fn(LLVMDiagnosticInfoRef, void*);
alias LLVMYieldCallback = extern(C) fn(LLVMContextRef, void*);


extern(C):

//#--- Auto generated below ---#
