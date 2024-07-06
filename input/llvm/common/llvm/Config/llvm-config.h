// SPDX-FileCopyrightText: 2024, Jakob Bornecrantz.
// SPDX-License-Identifier: MIT OR Apache-2.0 OR BSL-1.0

#pragma once

/*
 * Bare minimum for files to compile.
 */

#define LLVM_NATIVE_ASMPARSER LLVMInitializeX86AsmParser
#define LLVM_NATIVE_ASMPRINTER LLVMInitializeX86AsmPrinter
#define LLVM_NATIVE_DISASSEMBLER LLVMInitializeX86Disassembler
#define LLVM_NATIVE_TARGET LLVMInitializeX86Target
#define LLVM_NATIVE_TARGETINFO LLVMInitializeX86TargetInfo
#define LLVM_NATIVE_TARGETMC LLVMInitializeX86TargetMC
