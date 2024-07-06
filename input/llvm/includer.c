// SPDX-FileCopyrightText: 2024, Jakob Bornecrantz.
// SPDX-License-Identifier: MIT OR Apache-2.0 OR BSL-1.0

#include <llvm-c/Analysis.h>
#include <llvm-c/BitReader.h>
#include <llvm-c/BitWriter.h>
#include <llvm-c/Comdat.h>
#include <llvm-c/Core.h>
#include <llvm-c/DebugInfo.h>
#include <llvm-c/ExecutionEngine.h>
#if CROSSE_LLVM_VERSION < 17
#include <llvm-c/Initialization.h>
#endif
#include <llvm-c/Linker.h>
#include <llvm-c/Support.h>
#include <llvm-c/Target.h>
#include <llvm-c/TargetMachine.h>
