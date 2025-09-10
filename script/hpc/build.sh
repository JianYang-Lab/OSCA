#!/usr/bin/env bash

set -e  # 如果出错立即退出
CWD=$(pwd)

# ========= 可配置变量 =========
LINUX_DEPLOY_BIN=${LINUX_DEPLOY_BIN:/storage/yangjianLab/misc_share/tools/linuxdeploy-x86_64.AppImage}
APP_IMAGE_TOOL_BIN=${APP_IMAGE_TOOL_BIN:/storage/yangjianLab/misc_share/tools/appimagetool-x86_64.AppImage}
APP_IMAGE_RUNTIME_FILE=${APP_IMAGE_RUNTIME_FILE:/storage/yangjianLab/misc_share/tools/runtime-x86_64}

MKL_ROOT_PATH=${MKL_ROOT_PATH:-/storage/yangjianLab/sharedata/softwares/mkl_v2022.0.1_d20220120/mkl/2022.0.1/lib/cmake/mkl}
RMATH_ROOT_PATH=${RMATH_ROOT_PATH:-/storage/yangjianLab/sharedata/softwares/Rmath_v3.6.3_d20211126}
RMATH_INCLUDE_DIR=${RMATH_INCLUDE_DIR:-${RMATH_ROOT_PATH}/include}
RMATH_LIBRARY=${RMATH_LIBRARY:-${RMATH_ROOT_PATH}/lib/libRmath.so}

INSTALL_PREFIX="${CWD}/build/Release/installed/usr"
APPDIR="$(dirname ${INSTALL_PREFIX})"
BUILD_DIR="build/Release"

echo "==== [OSCA Build Script] ===="
echo "Current working directory: ${CWD}"
echo "Using linuxdeploy: ${LINUX_DEPLOY_BIN}"
echo "Using appimagetool: ${APP_IMAGE_TOOL_BIN}"
echo "Using runtime: ${APP_IMAGE_RUNTIME_FILE}"

# ====== 加载依赖模块（视你的环境而定）======
module load gcc/8.4.0 cmake intelmkl gsl

# ====== CMake 配置阶段 ======
cmake -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=${INSTALL_PREFIX} \
      -DRMATH_INCLUDE_DIR=${RMATH_INCLUDE_DIR} \
      -DRMATH_LIBRARY=${RMATH_LIBRARY} \
      -B ${BUILD_DIR} -S .

# ====== 编译阶段 ======
cmake --build ${BUILD_DIR}

# ====== 安装阶段 ======
cmake --install ${BUILD_DIR}

cp /storage/yangjianLab/sharedata/softwares/Rmath_v3.6.3_d20211126/lib/libRmath.so build/Release/installed/usr/lib/
strip build/Release/installed/usr/lib/libRmath.so

# ====== 打包阶段（AppImage）======
${LINUX_DEPLOY_BIN} \
  --appdir "${APPDIR}" \
  --executable "${INSTALL_PREFIX}/bin/osca" \
  --desktop-file "${INSTALL_PREFIX}/share/applications/osca.desktop" \
  --icon-file "${INSTALL_PREFIX}/share/icons/hicolor/256x256/apps/osca.png" \
  --output appimage

${APP_IMAGE_TOOL_BIN} "${APPDIR}" \
  --runtime-file "${APP_IMAGE_RUNTIME_FILE}"    

echo "==== [DONE] OSCA build and AppImage complete. ===="
