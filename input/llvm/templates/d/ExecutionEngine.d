/*#D*/
// SPDX-FileCopyrightText: 2007-2024, LLVM Developers.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

module lib.llvm.c.ExecutionEngine;

public import lib.llvm.c.Types;
import lib.llvm.c.Target;
import lib.llvm.c.TargetMachine;


private alias uintptr_t = size_t;
private alias uint8_t = ubyte;


struct LLVMGenericValue {} alias LLVMGenericValueRef = LLVMGenericValue*;
struct LLVMExecutionEngine {} alias LLVMExecutionEngineRef = LLVMExecutionEngine*;
struct LLVMMCJITMemoryManager {} alias LLVMMCJITMemoryManagerRef = LLVMMCJITMemoryManager*;


struct LLVMMCJITCompilerOptions {
	uint OptLevel;
	LLVMCodeModel CodeModel;
	bool NoFramePointerElim;
	bool EnableFastISel;
	LLVMMCJITMemoryManagerRef MCJMM;
}

alias LLVMMemoryManagerAllocateCodeSectionCallback = uint8_t function(void *Opaque, uintptr_t Size, uint Alignment, uint SectionID, const(char)* SectionName);
alias LLVMMemoryManagerAllocateDataSectionCallback = uint8_t function(void *Opaque, uintptr_t Size, uint Alignment, uint SectionID, const(char)* SectionName, LLVMBool IsReadOnly);
alias LLVMMemoryManagerFinalizeMemoryCallback = LLVMBool function(void *Opaque, char **ErrMsg);
alias LLVMMemoryManagerDestroyCallback = void function(void *Opaque);


extern(C):

//#--- Auto generated below ---#
