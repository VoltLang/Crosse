/*#D*/
// SPDX-FileCopyrightText: 2007-2024, LLVM Developers.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

module lib.llvm.c.ExecutionEngine;

public import lib.llvm.c.Types;
import lib.llvm.c.Target;
import lib.llvm.c.TargetMachine;


private alias uintptr_t = size_t;
private alias uint8_t = u8;


struct LLVMGenericValue {} alias LLVMGenericValueRef = LLVMGenericValue*;
struct LLVMExecutionEngine {} alias LLVMExecutionEngineRef = LLVMExecutionEngine*;
struct LLVMMCJITMemoryManager {} alias LLVMMCJITMemoryManagerRef = LLVMMCJITMemoryManager*;


struct LLVMMCJITCompilerOptions {
	OptLevel: uint;
	CodeModel: LLVMCodeModel;
	NoFramePointerElim: bool;
	EnableFastISel: bool;
	MCJMM: LLVMMCJITMemoryManagerRef;
}

alias LLVMMemoryManagerAllocateCodeSectionCallback = fn(Opaque: void*, Size: uintptr_t, Alignment: uint, SectionID: uint, SectionName: const(char)*) uint8_t;
alias LLVMMemoryManagerAllocateDataSectionCallback = fn(Opaque: void*, Size: uintptr_t, Alignment: uint, SectionID: uint, SectionName: const(char)*, IsReadOnly: LLVMBool) uint8_t;
alias LLVMMemoryManagerFinalizeMemoryCallback = fn(Opaque: void*, ErrMsg: char**) LLVMBool;
alias LLVMMemoryManagerDestroyCallback = fn(Opaque: void*);


extern(C):

//#--- Auto generated below ---#
