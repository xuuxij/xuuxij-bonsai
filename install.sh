#!/bin/sh
# Installs xuuxij-bonsai from GitHub.
#
#   curl -fsSL https://raw.githubusercontent.com/xuuxij/xuuxij-bonsai/main/install.sh | sh
#   curl -fsSL https://raw.githubusercontent.com/xuuxij/xuuxij-bonsai/main/install.sh | sh -s -- --system
#
# The program goes into ~/.local/bin (with --system into /usr/local/bin, which asks for
# sudo), the default settings into ~/.config/xuuxij-bonsai.conf unless you already have
# one. Needs python3 with its curses module, which every Linux python3 has, and curl or
# wget. Run it again to update; your settings file is never overwritten.
set -e

RAW="https://raw.githubusercontent.com/xuuxij/xuuxij-bonsai/main"
if [ "${1:-}" = "--system" ]; then
    BIN=/usr/local/bin
    SUDO=sudo
else
    BIN="$HOME/.local/bin"
    SUDO=""
fi

command -v python3 >/dev/null 2>&1 || { echo "xuuxij-bonsai needs python3 (3.8 or later)"; exit 1; }
python3 -c "import curses" 2>/dev/null || { echo "this python3 is missing its curses module"; exit 1; }

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
fetch() {
    if command -v curl >/dev/null 2>&1; then curl -fsSL "$1" -o "$2"
    elif command -v wget >/dev/null 2>&1; then wget -qO "$2" "$1"
    else echo "needs curl or wget"; exit 1
    fi
}
fetch "$RAW/xuuxij-bonsai" "$tmp/xuuxij-bonsai"
fetch "$RAW/xuuxij-bonsai.conf" "$tmp/xuuxij-bonsai.conf"
python3 -m py_compile "$tmp/xuuxij-bonsai"

$SUDO mkdir -p "$BIN"
$SUDO install -m 755 "$tmp/xuuxij-bonsai" "$BIN/xuuxij-bonsai"
mkdir -p "$HOME/.config"
if [ -f "$HOME/.config/xuuxij-bonsai.conf" ]; then
    echo "kept your settings: ~/.config/xuuxij-bonsai.conf"
else
    install -m 644 "$tmp/xuuxij-bonsai.conf" "$HOME/.config/xuuxij-bonsai.conf"
    echo "settings: ~/.config/xuuxij-bonsai.conf"
fi
echo "installed: $BIN/xuuxij-bonsai"
case ":$PATH:" in
    *":$BIN:"*) echo "run:       xuuxij-bonsai      (any key ends it)" ;;
    *) echo "run:       $BIN/xuuxij-bonsai      (any key ends it; $BIN is not on your PATH yet)" ;;
esac
echo "screensaver in tmux: add to ~/.tmux.conf"
echo "    set -g lock-after-time 300"
echo "    set -g lock-command '$BIN/xuuxij-bonsai'"
