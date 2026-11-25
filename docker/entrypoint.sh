#!/usr/bin/env bash
# Runs inside the container, in the mounted micropython/ source tree.
set -euo pipefail

TARGET_NAME=bbc-microbit-classic-gcc-nosd
TARGET="$TARGET_NAME@https://github.com/lancaster-university/yotta-target-bbc-microbit-classic-gcc-nosd"

if [ ! -f module.json ]; then
  echo "entrypoint: no module.json in $PWD - mount the micropython source tree here" >&2
  exit 1
fi

# Git refuses to work in a repo owned by another uid (makeversionhdr.py calls git).
git config --global --add safe.directory '*'

# Fetch the yotta target + modules from GitHub only when missing
# (anonymous GitHub API limit is 60 requests/hour).
if [ ! -d yotta_modules/nrf51-sdk ] || [ "${FORCE_YOTTA_UP:-0}" = 1 ]; then
  yotta target "$TARGET"
  yotta up
fi

# The CMake cache stores the absolute compiler path. If it was configured by a
# host build (different toolchain location), start the build directory fresh.
cache="build/$TARGET_NAME/CMakeCache.txt"
if [ -f "$cache" ]; then
  cached=$(sed -n 's/^ARM_NONE_EABI_GCC:FILEPATH=//p' "$cache")
  if [ -n "$cached" ] && [ "$cached" != "$(command -v arm-none-eabi-gcc)" ]; then
    echo "entrypoint: CMake cache is from another toolchain ($cached), wiping build/$TARGET_NAME"
    rm -rf "build/$TARGET_NAME"
  fi
fi

exec "$@"
