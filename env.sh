# Source this file:  source env.sh
# Sets up the self-contained MicroPython / Calliope mini v1 build environment.
_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-${(%):-%x}}")" && pwd)"
export CALLIOPE_ENV="$_ROOT"
export PATH="$_ROOT/tools/gcc-arm-none-eabi-10.3-2021.10/bin:$_ROOT/.venv/bin:$_ROOT/tools:$PATH"
export UV_PYTHON_INSTALL_DIR="$_ROOT/tools/python"
export UV_CACHE_DIR="$_ROOT/tools/uv-cache"
export VIRTUAL_ENV="$_ROOT/.venv"
# yotta's registry is gone; never prompt for login
export YOTTA_NO_LOGIN=1
unset _ROOT
