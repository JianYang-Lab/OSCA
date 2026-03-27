#!/bin/bash
set -e

APP_NAME="osca"
BUILD_DIR="build/Release"
INSTALL_DIR="$BUILD_DIR/installed"
PACKAGE_DIR="${APP_NAME}-package"
EXECUTABLE_PATH="$INSTALL_DIR/usr/bin/$APP_NAME"

echo "[1/5] CMake 构建并安装..."
CC=gcc CXX=g++ cmake -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$INSTALL_DIR/usr" \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -B "$BUILD_DIR" -S .
cmake --build "$BUILD_DIR" --target install

echo "[2/5] 准备打包目录..."
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR/bin"

cp "$EXECUTABLE_PATH" "$PACKAGE_DIR/bin/$APP_NAME"

# 仅 macOS 下用 dylibbundler 修复动态库依赖，Linux/Windows 不用
if [[ "$(uname)" == "Darwin" ]]; then
  echo "[3/5] 修复 dylib 路径..."
  dylibbundler -od -b \
    -x "$PACKAGE_DIR/bin/$APP_NAME" \
    -d "$PACKAGE_DIR/lib" \
    -p @executable_path/../lib
fi

echo "[4/5] 生成启动脚本..."
cat > "$PACKAGE_DIR/run.sh" <<EOF
#!/bin/bash
DIR=\$(cd "\$(dirname "\$0")"; pwd)
EOF

if [[ "$(uname)" == "Darwin" ]]; then
  cat >> "$PACKAGE_DIR/run.sh" <<EOF
export DYLD_LIBRARY_PATH="\$DIR/lib"
EOF
fi

cat >> "$PACKAGE_DIR/run.sh" <<EOF
"\$DIR/bin/$APP_NAME" "\$@"
EOF

chmod +x "$PACKAGE_DIR/run.sh"

echo "[5/5] 打包完成，目录: $PACKAGE_DIR"
