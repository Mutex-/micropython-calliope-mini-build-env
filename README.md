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

### Running scripts from the PC

```sh
source env.sh
micropython/tools/pyboard.py /dev/ttyACM0 ../scripts/test.py   # runs it, prints its output
```

`pyboard.py` needs pyserial, which `setup.sh` installs into `.venv`. Close any `picocom` session first: two programs on one serial port each get part of the data.

`pyboard.py` sends the script through the REPL, so the board holds the whole source text in RAM while compiling it. With about 9 KB free, scripts from roughly 3 KB up fail with `MemoryError: memory allocation failed` before their first line runs (the error has no line number). Copy those to the board's flash instead, where they compile without that copy:

```sh
ufs put robot.py            # then in the REPL: import robot
ufs put robot.py main.py    # or as main.py: runs at every boot (Ctrl-C in the REPL stops it)
ufs ls                      # list files; ufs rm <name> deletes one
```

`ufs` comes from microfs, which `setup.sh` installs. Flashing new firmware erases the files.

The scripts in `micropython/examples/` are written for the micro:bit and import `microbit`. This firmware's module is `calliopemini`, and `microbit` is an alias for it, so they run unchanged. All 31 started without errors on a Calliope mini v1.

### Extra Python packages

After `source env.sh`, `pip install <package>` installs into `.venv`. Without `env.sh`, `pip` is Arch's system pip, which refuses with "externally-managed-environment". `uv pip install <package>` also targets `.venv` once `env.sh` is sourced.

## Docker / Podman

The `Dockerfile` builds a toolchain-only image: Python 3.8, yotta and the pinned versions from `docker/requirements.txt`, ARM GCC 10.3 for amd64 or arm64, and the real `srecord`. The source tree isn't copied into the image. It's bind-mounted when the container runs.

```sh
./docker-build.sh                  # make all -> micropython/build/firmware.hex
./docker-build.sh make qstrs       # any command, run inside micropython/ (here: force a qstr regeneration)
./docker-build.sh bash             # shell in the container
```

- The wrapper works with either `docker` or `podman`. It runs as your uid so build files stay yours, and it initialises the `micropython` submodule if needed.
- The image is built on first use and rebuilt automatically whenever `Dockerfile` or `docker/` changes (it carries a hash of them as a label).
- The whole repository is mounted at its host path: yotta writes absolute paths, and in a submodule checkout the firmware's git data lives in `.git/modules/`, which the version header needs. If the CMake cache came from the host toolchain, the container wipes `build/bbc-microbit-classic-gcc-nosd` once. When you switch back to a native build, run `rm -rf micropython/build` first.
- yotta modules are fetched only if they're missing. Set `FORCE_YOTTA_UP=1` to refresh them.

## Why these pins

- **yotta** is unmaintained and its registry is offline. The target and all modules are pulled from GitHub.
- **CMake 4.x** (the Arch system version) won't accept the old `cmake_minimum_required` used by yotta, so the venv ships CMake 3.22.
- **markupsafe ≥ 2.1** removed `soft_unicode`, which yotta's jinja2 still imports.
- **Header dependencies:** yotta's `mbed-gcc` target uses CMake's pre-3.20 placeholder `<DEPFILE>` in its dependency flags. CMake 3.22 doesn't expand it, so ninja recorded no header dependencies and changing a header recompiled nothing. The firmware Makefile corrects the downloaded target before every build, and rebuilds from clean the first time.
- The fork's **`master`** branch is plain BBC micro:bit code. The Calliope pins, buttons, RGB LED, motor and mic are on `v1.1.1-cmini_classic`.

## Adding Python names (qstrs)

New names visible from Python (a module attribute, a method, a type name) are handled by the build. Use them as `MP_QSTR_name` in the C code, or add `Q(name)` to `micropython/inc/microbit/qstrdefsport.h`, then run `make -C micropython all` as usual (or `./docker-build.sh`).

`make all` regenerates `inc/genhdr/qstrdefs.generated.h` whenever a file in `source/` or `inc/microbit/` has changed (about 3 s), via `tools/updateqstrs.sh`:

- **Table unchanged:** the old header is put back with its original timestamp, so nothing recompiles.
- **Table changed:** `build/bbc-microbit-classic-gcc-nosd` is removed first and the firmware builds from clean. New names shift every name's number and nearly every object includes the table, so this costs little, and it keeps the build consistent even where header tracking falls short. (Before header dependencies were fixed, an incremental build left objects compiled against the old table, and that firmware hung at boot with no REPL.)

Commit the regenerated header together with the change that caused it. `make -C micropython qstrs` forces a regeneration without any source change.
