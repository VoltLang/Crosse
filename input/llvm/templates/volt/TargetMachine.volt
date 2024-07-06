// SPDX-FileCopyrightText: 2007-2024, LLVM Developers.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

module lib.llvm.c.TargetMachine;

public import lib.llvm.c.Types;
import lib.llvm.c.Target;


struct LLVMTargetMachine {} alias  LLVMTargetMachineRef = LLVMTargetMachine*;
struct LLVMTarget {} alias LLVMTargetRef = LLVMTarget*;


extern(C):

//#--- Auto generated below ---#
