#!/usr/bin/env bash
# One-shot, sudo-free setup of the MicroPython build environment for the Calliope mini v1.
# Everything lands inside this directory. Safe to re-run.
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"

UV_VER=0.5.31
GCC_DIR=gcc-arm-none-eabi-10.3-2021.10
GCC_URL="https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/${GCC_DIR}-x86_64-linux.tar.bz2"
MP_REPO=https://github.com/Mutex-/micropython-calliope-mini.git          # your fork
MP_UPSTREAM=https://github.com/calliope-edu/micropython-calliope-mini.git # Calliope original
MP_BRANCH=calliope-v1-fixes      # v1.1.1-cmini_classic (Calliope mini v1 port) + our fixes; master is plain micro:bit
TARGET='bbc-microbit-classic-gcc-nosd@https://github.com/lancaster-university/yotta-target-bbc-microbit-classic-gcc-nosd'

mkdir -p tools
dl=$(mktemp -d); trap 'rm -rf "$dl"' EXIT

if [ ! -x tools/uv ]; then
  echo ">> uv $UV_VER"
  curl -sSLf -o "$dl/uv.tgz" "https://github.com/astral-sh/uv/releases/download/$UV_VER/uv-x86_64-unknown-linux-gnu.tar.gz"
  tar xzf "$dl/uv.tgz" -C "$dl" && mv "$dl"/uv-x86_64-unknown-linux-gnu/uv tools/
fi

if [ ! -x "tools/$GCC_DIR/bin/arm-none-eabi-gcc" ]; then
  echo ">> ARM GCC 10.3-2021.10"
  curl -sSLf -o "$dl/gcc.tar.bz2" "$GCC_URL"
  tar xjf "$dl/gcc.tar.bz2" -C tools
fi

source "$ROOT/env.sh"

if [ ! -x .venv/bin/yotta ]; then
  echo ">> Python 3.8 venv + yotta"
  uv venv -q --python 3.8 .venv
  # yotta is unmaintained: CMake must be <4 and markupsafe <2.1 (jinja2 soft_unicode)
  uv pip install -q --python .venv/bin/python \
    yotta==0.20.5 cmake==3.22.3 ninja==1.10.2.3 'markupsafe<2.1'
fi

if [ ! -e micropython/.git ]; then
  if [ -f .gitmodules ] && git rev-parse --git-dir >/dev/null 2>&1; then
    # Normal case: this folder is the git repository, micropython/ its submodule.
    echo ">> fetching the micropython submodule"
    git submodule update --init micropython
  else
    # Folder copied without git: clone the fixes branch directly.
    echo ">> cloning $MP_REPO ($MP_BRANCH)"
    git clone -b "$MP_BRANCH" "$MP_REPO" micropython
  fi
  git -C micropython remote add upstream "$MP_UPSTREAM" 2>/dev/null || true
fi

cd micropython
if [ ! -d yotta_modules/nrf51-sdk ] || [ "${FORCE_YOTTA_UP:-0}" = 1 ]; then
  # Each run makes many anonymous GitHub API calls (limit 60/h), so only do it when needed.
  echo ">> yotta target + dependencies (from GitHub)"
  yotta target "$TARGET"
  yotta up
else
  echo ">> yotta modules already present (FORCE_YOTTA_UP=1 to refresh)"
fi

echo
echo "Done. Build with:  source env.sh && make -C micropython all"
echo "Firmware:          micropython/build/firmware.hex"
