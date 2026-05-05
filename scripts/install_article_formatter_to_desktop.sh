#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SRC_DIR/article_formatter_desktop.py"

if [[ ! -f "$SRC" ]]; then
  echo "未找到源文件: $SRC"
  exit 1
fi

DESKTOP_DIR="${HOME}/Desktop"
mkdir -p "$DESKTOP_DIR"
TARGET="$DESKTOP_DIR/article_formatter_desktop.py"
cp "$SRC" "$TARGET"
chmod +x "$TARGET"

LAUNCHER="$DESKTOP_DIR/自动排版文章工具.command"
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env bash
python3 "$TARGET"
EOF
chmod +x "$LAUNCHER"

echo "已安装到桌面:"
echo "- $TARGET"
echo "- $LAUNCHER"
