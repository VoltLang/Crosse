# SPDX-FileCopyrightText: 2024, Jakob Bornecrantz.
# SPDX-License-Identifier: MIT OR Apache-2.0 OR BSL-1.0
#!/bin/bash

CROSSE_DIR="/home/jakob/Volt/crosse"
LLVM_DIR="/home/jakob/Prog/LLVM/llvm-project"

cd $LLVM_DIR

# Reversed to better deal with files being removed staying around.
VERSIONS=(18 17 16 15 14 13 12 11 11 10)
FILES=(
"Analysis.h"
"BitReader.h"
"BitWriter.h"
"Comdat.h"
"Core.h"
"DataTypes.h"
"DebugInfo.h"
"Deprecated.h"
"ErrorHandling.h"
"ExecutionEngine.h"
"ExternC.h"
"Initialization.h"
"Linker.h"
"Support.h"
"Target.h"
"TargetMachine.h"
"Types.h"
)

do_the_copy () {
	VERSION=$1
	VERSION_DIR="${CROSSE_DIR}/input/llvm/llvm-${VERSION}/llvm-c"

	rm -rf "${VERSION_DIR}"
	mkdir -p "${VERSION_DIR}"

	for FILE in ${FILES[@]}; do
		FULL="llvm/include/llvm-c/${FILE}"
		if [ -f ${FULL} ]; then
			cp "${FULL}" "${VERSION_DIR}"
		fi
	done
}

git reset --hard
git checkout main
git rebase

# Copy top of tree.
do_the_copy "19"

# Go through the versions we are looking for.
for VERSION in ${VERSIONS[@]}; do
	git checkout "origin/release/${VERSION}.x" -- "llvm/include/llvm-c"

	do_the_copy "${VERSION}"
done

# Restore the source tree.
git reset --hard
