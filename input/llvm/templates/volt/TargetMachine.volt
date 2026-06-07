// SPDX-FileCopyrightText: {{ copyright_years }}, LLVM Developers.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

module lib.llvm.c.TargetMachine;

public import lib.llvm.c.Types;
import lib.llvm.c.Target;


struct LLVMTargetMachine {} alias  LLVMTargetMachineRef = LLVMTargetMachine*;
struct LLVMTarget {} alias LLVMTargetRef = LLVMTarget*;
version (LLVMVersion18AndAbove) {
	struct LLVMTargetMachineOptions {} alias LLVMTargetMachineOptionsRef = LLVMTargetMachineOptions*;
}


extern(C):

//#--- Auto generated below ---#
