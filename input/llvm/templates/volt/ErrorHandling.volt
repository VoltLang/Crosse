/*#D*/
// SPDX-FileCopyrightText: 2007-2024, LLVM Developers.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

module lib.llvm.c.ErrorHandling;

public import lib.llvm.c.Types;


alias LLVMFatalErrorHandler = extern(C) fn(Reason: const(char)*);


extern(C):

//#--- Auto generated below ---#
