# MicroPython build environment for the Calliope mini v1

This setup is self-contained and doesn't need sudo. Everything lives in this directory.

| Component | Version | Where |
|---|---|---|
| Source | `Mutex-/micropython-calliope-mini` @ `calliope-v1-fixes`: Calliope's `v1.1.1-cmini_classic` plus our fixes (fork of `calliope-edu/micropython-calliope-mini`, remote `upstream`) | `micropython/` |
| DAL | `calliope-mini/microbit-dal` @ `v2.1.1-cminiclassic` (via yotta) | `micropython/yotta_modules/` |
| Compiler | GNU Arm Embedded 10.3-2021.10 (the version the upstream CI uses) | `tools/gcc-arm-none-eabi-10.3-2021.10/` |
| Python | 3.8 (managed by uv) + yotta 0.20.5, CMake 3.22.3, Ninja 1.10 | `.venv/`, `tools/python/` |
| `srec_cat` | Shim built on `intelhex` (srecord is AUR-only on Arch) | `tools/srec_cat` |

## Repository layout

This folder is a git repository for the build environment. The firmware source in `micropython/` is a **git submodule** on [`Mutex-/micropython-calliope-mini`](https://github.com/Mutex-/micropython-calliope-mini), branch `calliope-v1-fixes`. The toolchain in `tools/` and `.venv/` aren't tracked; `setup.sh` downloads them.

- **Fresh clone:** `git clone --recurse-submodules <url>`, or plain `git clone` and let `./setup.sh` initialise the submodule.
- **Firmware changes:** commit and push inside `micropython/` (`origin` is the fork, `upstream` is Calliope's original), then record the new commit here with `git add micropython && git commit`.
- **Pull the latest fixes branch:** `git submodule update --remote micropython`.

## Usage

```sh
./setup.sh                    # first time (or on a fresh clone of this folder)
source env.sh                 # works in bash and zsh
make -C micropython all       # -> micropython/build/firmware.hex
```

Flash the firmware by copying `micropython/build/firmware.hex` onto the `MINI` USB drive.
The REPL runs at 115200 baud: `picocom /dev/ttyACM0 -b 115200`.

```python
>>> from calliopemini import *
>>> display.scroll("Hallo")
```

To push a script: `micropython/tools/pyboard.py /dev/ttyACM0 ../scripts/test.py`

## Docker / Podman

The `Dockerfile` builds a toolchain-only image: Python 3.8, yotta and the pinned versions from `docker/requirements.txt`, ARM GCC 10.3 for amd64 or arm64, and the real `srecord`. The source tree isn't copied into the image. It's bind-mounted when the container runs.

```sh
docker build -t calliope-mpy .     # optional: docker-build.sh builds the image if it's missing
./docker-build.sh                  # make all -> micropython/build/firmware.hex
./docker-build.sh make qstrs       # any command, run inside micropython/
./docker-build.sh bash             # shell in the container
```

- The wrapper works with either `docker` or `podman`. It runs as your uid so build files stay yours, and it clones the source if `micropython/` is missing.
- The source is mounted at its host path because yotta writes absolute paths. If the CMake cache came from the host toolchain, the container wipes `build/bbc-microbit-classic-gcc-nosd` once. When you switch back to a native build, run `rm -rf micropython/build` first.
- yotta modules are fetched only if they're missing. Set `FORCE_YOTTA_UP=1` to refresh them.

## Why these pins

- **yotta** is unmaintained and its registry is offline. The target and all modules are pulled from GitHub.
- **CMake 4.x** (the Arch system version) won't accept the old `cmake_minimum_required` used by yotta, so the venv ships CMake 3.22.
- **markupsafe ≥ 2.1** removed `soft_unicode`, which yotta's jinja2 still imports.
- The fork's **`master`** branch is plain BBC micro:bit code. The Calliope pins, buttons, RGB LED, motor and mic are on `v1.1.1-cmini_classic`.

## Adding Python names (qstrs)

New names visible from Python (a module attribute, a method, a type name) need two steps:

1. Add `Q(name)` to `micropython/inc/microbit/qstrdefsport.h`. Names used as `MP_QSTR_name` in the C code are also picked up automatically.
2. Regenerate the table, then do a **clean** build:

   ```sh
   source env.sh
   (cd micropython && ./tools/makeqstrhdr.sh && rm -rf inc/genhdr/qstr inc/genhdr/qstr*.i.last inc/genhdr/qstrdefs.collected.h* inc/genhdr/qstrdefs.preprocessed.h)
   rm -rf micropython/build && make -C micropython all
   ```

This branch's Makefile has no `qstrs` target. The clean build matters: regenerating shifts every name's number, and an incremental build keeps some objects compiled against the old table. Firmware built that way hangs at boot with no REPL.
