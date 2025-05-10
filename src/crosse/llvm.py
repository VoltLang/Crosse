# SPDX-FileCopyrightText: 2024, Jakob Bornecrantz.
# SPDX-License-Identifier: MIT OR Apache-2.0 OR BSL-1.0

import os
import clang.cindex
import crosse.clang
from crosse.objects import Module


__type_one_to_one: list[str]
__type_one_to_one = {
    'LLVMAttributeRef',
    'LLVMBasicBlockRef',
    'LLVMBool',
    'LLVMBuilderRef',
    'LLVMComdatRef',
    'LLVMContextRef',
    'LLVMDbgRecordRef',
    'LLVMDiagnosticInfoRef',
    'LLVMDIBuilderRef',
    'LLVMExecutionEngineRef',
    'LLVMGenericValueRef',
    'LLVMJITEventListenerRef',
    'LLVMMCJITMemoryManagerRef',
    'LLVMMemoryBufferRef',
    'LLVMMetadataRef',
    'LLVMModuleProviderRef',
    'LLVMModuleRef',
    'LLVMNamedMDNodeRef',
    'LLVMOperandBundleRef',
    'LLVMPassManagerRef',
    'LLVMPassRegistryRef',
    'LLVMTargetDataRef',
    'LLVMTargetLibraryInfoRef',
    'LLVMTargetMachineOptionsRef',
    'LLVMTargetMachineRef',
    'LLVMTargetRef',
    'LLVMTypeRef',
    'LLVMUseRef',
    'LLVMValueRef',

    'LLVMMemoryManagerAllocateCodeSectionCallback',
    'LLVMMemoryManagerAllocateDataSectionCallback',
    'LLVMMemoryManagerDestroyCallback',
    'LLVMMemoryManagerFinalizeMemoryCallback',
    'LLVMYieldCallback',

    'LLVMAtomicOrdering',
    'LLVMAtomicRMWBinOp',
    'LLVMAttributeIndex',
    'LLVMCodeGenFileType',
    'LLVMCodeGenOptLevel',
    'LLVMCodeModel',
    'LLVMComdatSelectionKind',
    'LLVMDiagnosticHandler',
    'LLVMDiagnosticSeverity',
    'LLVMDIFlags',
    'LLVMDLLStorageClass',
    'LLVMDWARFEmissionKind',
    'LLVMDWARFMacinfoRecordType',
    'LLVMDWARFSourceLanguage',
    'LLVMDWARFTypeEncoding',
    'LLVMFastMathFlags',
    'LLVMFatalErrorHandler',
    'LLVMGEPNoWrapFlags',
    'LLVMGlobalISelAbortMode',
    'LLVMInlineAsmDialect',
    'LLVMIntPredicate',
    'LLVMLinkage',
    'LLVMMetadataKind',
    'LLVMModuleFlagBehavior',
    'LLVMOpcode',
    'LLVMRealPredicate',
    'LLVMRelocMode',
    'LLVMTailCallKind',
    'LLVMThreadLocalMode',
    'LLVMTypeKind',
    'LLVMUnnamedAddr',
    'LLVMValueKind',
    'LLVMVerifierFailureAction',
    'LLVMVisibility',
}

__volt_type_dict: dict[str, str]
__volt_type_dict = {
    'int': 'i32',
    'int *': 'i32',
    'long long': 'i64',
    'unsigned int': 'u32',
    'unsigned int *': 'u32*',
    'const unsigned int *': 'const(u32)*',
    'unsigned long long': 'u64',
    'uint8_t': 'u8',
    'uint16_t': 'u16',
    'uint32_t': 'u32',
    'int64_t': 'i64',
    'int64_t *': 'i64*',
    'uint64_t': 'u64',
    'uint64_t *': 'u64*',
    'uint64_t[]': 'u64*',
    'const uint64_t[]': 'const(u64)*',
    'size_t': 'size_t',
    'size_t *': 'size_t*',
    'double': 'f64',
    'void *': 'void*',
    'char *': 'char*',
    'char **': 'char**',
    'const char *': 'const(char)*',
    'const char *const *': 'const(const(char)*)*',

    'LLVMAttributeRef *': 'LLVMAttributeRef*',
    'LLVMBasicBlockRef *': 'LLVMBasicBlockRef*',
    'LLVMExecutionEngineRef *': 'LLVMExecutionEngineRef*',
    'LLVMGenericValueRef *': 'LLVMGenericValueRef*',
    'LLVMMemoryBufferRef *': 'LLVMMemoryBufferRef*',
    'LLVMMetadataRef *': 'LLVMMetadataRef*',
    'LLVMModuleRef *': 'LLVMModuleRef*',
    'LLVMOperandBundleRef *': 'LLVMOperandBundleRef*',
    'LLVMTargetRef *': 'LLVMTargetRef*',
    'LLVMTypeRef *': 'LLVMTypeRef*',
    'LLVMValueRef *': 'LLVMValueRef*',

    'enum LLVMByteOrdering': 'LLVMByteOrdering',
    'struct LLVMMCJITCompilerOptions *': 'LLVMMCJITCompilerOptions*',

    'LLVMBool *': 'LLVMBool*',
    'LLVMModuleFlagEntry *': 'LLVMModuleFlagEntry*',
    'LLVMValueMetadataEntry *': 'LLVMValueMetadataEntry*',
}

for t in __type_one_to_one:
    __volt_type_dict[t] = t


def type_to_volt(type: clang.cindex.Type) -> str:
    t = type.spelling
    if t in __volt_type_dict:
        return __volt_type_dict[t]
    else:
        print('Unknown type {}'.format(t))
        return t


__d_type_dict: dict[str, str]
__d_type_dict = {}

for k in __volt_type_dict:
    v = __volt_type_dict[k]
    v = v.replace('u8', 'ubyte')
    v = v.replace('i16', 'short')
    v = v.replace('u16', 'ushort')
    v = v.replace('i32', 'int')
    v = v.replace('u32', 'uint')
    v = v.replace('i64', 'long')
    v = v.replace('u64', 'ulong')
    v = v.replace('f64', 'double')
    __d_type_dict[k] = v


def type_to_d(type: clang.cindex.Type) -> str:
    t = type.spelling
    if t in __d_type_dict:
        return __d_type_dict[t]
    else:
        print('Unknown type {}'.format(t))
        return t


__file_to_module: dict[str, str]
__file_to_module = {
    'Analysis.h': 'Analysis',
    'BitReader.h': 'BitReader',
    'BitWriter.h': 'BitWriter',
    'Comdat.h': 'Comdat',
    'Core.h': 'Core',
    'DebugInfo.h': 'DebugInfo',
    'ErrorHandling.h': 'ErrorHandling',
    'ExecutionEngine.h': 'ExecutionEngine',
    'Initialization.h': 'Initialization',
    'Linker.h': 'Linker',
    'Support.h': 'Support',
    'Target.h': 'Target',
    'TargetMachine.h': 'TargetMachine',
    'Types.h': 'Types',
}

__file_to_module_init_func: dict[str, str]
__file_to_module_init_func = {
    'Targets.def': 'Target',
    'Disassemblers.def': 'Target',
    'AsmParsers.def': 'Target',
    'AsmPrinters.def': 'Target',
}

__file_to_module_ignore: dict[str, bool]
__file_to_module_ignore = {
    '__sigset_t.h': True,
    'atomic_wide_counter.h': True,
    'byteswap.h': True,
    'inttypes.h': True,
    'math.h': True,
    'mathcalls-helper-functions.h': True,
    'mathcalls.h': True,
    'pthreadtypes.h': True,
    'select.h': True,
    'struct_mutex.h': True,
    'struct_rwlock.h': True,
    'struct_timespec.h': True,
    'struct_timeval.h': True,
    'thread-shared-types.h': True,
    'thread-shared-types.h': True,
    'types.h': True,
    'uintn-identity.h': True,
}

def cursor_file_to_module(cursor: clang.cindex.Cursor) -> (bool, str):
    file = os.path.basename(str(cursor.location.file))

    if file in __file_to_module:
        return (True, __file_to_module[file])

    if crosse.clang.is_function_declaration(cursor) and str(cursor.spelling).startswith('LLVMInitialize'):
        if file in __file_to_module_init_func:
            return (True, __file_to_module_init_func[file])

    if not file in __file_to_module_ignore:
        print("The file '{}' that '{}' was in had no mapping".format(file, cursor.spelling))

    return (False, None)


__strip_map: dict[str, list[str]]
__strip_map = {
    'LLVMAtomicOrdering': ['LLVMAtomicOrdering'],
    'LLVMAtomicRMWBinOp': ['LLVMAtomicRMWBinOp'],
    'LLVMByteOrdering': ['LLVM'],
    'LLVMCallConv': ['LLVM', 'CallConv'],
    'LLVMCodeGenFileType': ['LLVM', 'File'],
    'LLVMCodeGenOptLevel': ['LLVMCodeGenLevel'],
    'LLVMCodeModel': ['LLVMCodeModel'],
    'LLVMComdatSelectionKind': ['LLVM', 'SelectionKind'],
    'LLVMDiagnosticSeverity': ['LLVMDS'],
    'LLVMDIFlags': ['LLVMDIFlag'],
    'LLVMDLLStorageClass': ['LLVM', 'StorageClass'],
    'LLVMDWARFEmissionKind': ['LLVMDWARFEmission'],
    'LLVMDWARFMacinfoRecordType': ['LLVMDWARFMacinfoRecordType'],
    'LLVMDWARFSourceLanguage': ['LLVMDWARFSourceLanguage'],
    'LLVMGlobalISelAbortMode': ['LLVMGlobalISelAbort'],
    'LLVMInlineAsmDialect': ['LLVMInlineAsmDialect'],
    'LLVMIntPredicate': ['LLVMInt'],
    'LLVMLandingPadClauseTy': ['LLVMLandingPad'],
    'LLVMLinkage': ['LLVM', 'Linkage'],
    'LLVMLinkerMode': ['LLVMLinker'],
    'LLVMModuleFlagBehavior': ['LLVMModuleFlagBehavior'],
    'LLVMOpcode': ['LLVM'],
    'LLVMRealPredicate': ['LLVMReal'],
    'LLVMRelocMode': ['LLVMReloc'],
    'LLVMTailCallKind': ['LLVMTailCallKind'],
    'LLVMThreadLocalMode': ['LLVM', 'ThreadLocal'],
    'LLVMTypeKind': ['LLVM', 'TypeKind'],
    'LLVMUnnamedAddr': ['LLVM', 'Addr'],
    'LLVMValueKind': ['LLVM', 'ValueKind'],
    'LLVMVerifierFailureAction': ['LLVM', 'Action'],
    'LLVMVisibility': ['LLVM', 'Visibility'],
}

def strip_enum_member_name(parent: str, name: str) -> str:
    # Only accept known enums.
    if not parent in __strip_map:
        print(parent)
        assert(parent in __strip_map)

    l = __strip_map[parent]
    for to_remove in l:
        name = name.replace(to_remove, '')

    return name


def get_enum_value(parent: str, node: clang.cindex.Cursor) -> str:
    v = list(node.get_children())

    if len(v) == 0:
        # No initialisers, use calculated value.
        return str(node.enum_value)


    # Should only be one child.
    assert(len(v) == 1)

    # Unwrap.
    v = v[0]

    # Make some single integer literals prettier.
    if v.kind == clang.cindex.CursorKind.INTEGER_LITERAL:
        tokens = list(v.get_tokens())

        if len(tokens) > 1:
            return str(node.enum_value)

        p = str(tokens[0].spelling)

        if p.startswith('0x'):
            return p
        else:
            return str(node.enum_value)

    # Handle expression and make them pretty
    result = ''
    for t in v.get_tokens():
        txt = t.spelling

        if t.kind == clang.cindex.TokenKind.LITERAL:
            result = result + txt
            continue
        elif t.kind == clang.cindex.TokenKind.IDENTIFIER:
            result = result + strip_enum_member_name(parent, txt)
            continue

        if txt == '|':
            result = result + ' | '
        elif txt == '<<':
            result = result + ' << '
        elif txt == '(' or txt == ')':
            result = result + txt
        else:
            print(txt)
            assert(False)

    return result


def apply_touch_ups(mods: dict[str, Module]):


    core = mods['Core']
    del core.symbols['LLVMInitializeCore']

    return
