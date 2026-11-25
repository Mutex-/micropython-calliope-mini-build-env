#!/usr/bin/env bash
# Build the firmware inside the container.
#   ./docker-build.sh                 # make all  -> micropython/build/firmware.hex
#   ./docker-build.sh make qstrs      # any command, run in micropython/
#   ./docker-build.sh bash            # interactive shell
# Env: IMAGE (default calliope-mpy), SRC (default ./micropython), FORCE_YOTTA_UP=1
set -euo pipefail
cd "$(dirname "$0")"

IMAGE=${IMAGE:-calliope-mpy}
SRC=$(realpath "${SRC:-micropython}")

if command -v docker >/dev/null; then
  RT=docker; userargs=(--user "$(id -u):$(id -g)")
elif command -v podman >/dev/null; then
  RT=podman; userargs=(--userns=keep-id)
else
  echo "need docker or podman" >&2; exit 1
fi

if [ ! -e "$SRC/.git" ]; then
  if [ "$SRC" = "$PWD/micropython" ] && [ -f .gitmodules ]; then
    git submodule update --init micropython
  else
    git clone -b calliope-v1-fixes https://github.com/Mutex-/micropython-calliope-mini.git "$SRC"
  fi
fi

if ! "$RT" image inspect "$IMAGE" >/dev/null 2>&1; then
  "$RT" build -t "$IMAGE" .
fi

tty=(); [ -t 0 ] && tty=(-it)
cmd=("$@"); [ ${#cmd[@]} -eq 0 ] && cmd=(make all)

# Mount at the same absolute path as on the host: yotta writes absolute paths
# into build/ and .yotta.json, so host and container builds stay interchangeable.
exec "$RT" run --rm "${tty[@]}" "${userargs[@]}" \
  -e FORCE_YOTTA_UP="${FORCE_YOTTA_UP:-0}" \
  -v "$SRC:$SRC" -w "$SRC" \
  "$IMAGE" "${cmd[@]}"
