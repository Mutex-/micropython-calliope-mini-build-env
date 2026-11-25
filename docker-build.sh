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

# Rebuild the image when the files that define it change, not only when it's missing.
hash=$(cat Dockerfile docker/* | sha256sum | cut -c1-16)
have=$("$RT" image inspect -f '{{ index .Config.Labels "calliope.env-hash" }}' "$IMAGE" 2>/dev/null || true)
if [ "$have" != "$hash" ]; then
  "$RT" build --label "calliope.env-hash=$hash" -t "$IMAGE" .
fi

tty=(); [ -t 0 ] && tty=(-it)
cmd=("$@"); [ ${#cmd[@]} -eq 0 ] && cmd=(make all)

# Mount at the same absolute paths as on the host: yotta writes absolute paths
# into build/ and .yotta.json, so host and container builds stay interchangeable.
# The whole repository goes in, not just micropython/: in a submodule checkout the
# firmware's git data lives in .git/modules/, which makeversionhdr.py needs.
mounts=(-v "$PWD:$PWD")
case "$SRC/" in
  "$PWD"/*) ;;
  *) mounts+=(-v "$SRC:$SRC") ;;
esac

exec "$RT" run --rm "${tty[@]}" "${userargs[@]}" \
  -e FORCE_YOTTA_UP="${FORCE_YOTTA_UP:-0}" \
  "${mounts[@]}" -w "$SRC" \
  "$IMAGE" "${cmd[@]}"
