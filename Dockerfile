# MicroPython build environment for the Calliope mini v1 (nRF51822, yotta + microbit-dal).
# Toolchain-only image: the source tree is bind-mounted at run time (see docker-build.sh).
#
#   docker build -t calliope-mpy .
#   ./docker-build.sh            # = make all
#
# Python 3.8: yotta 0.20.5 is unmaintained and breaks on newer interpreters.
FROM python:3.8-slim-bookworm

ARG GCC_VERSION=10.3-2021.10
ARG TARGETARCH

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      bzip2 ca-certificates curl git make srecord \
 && rm -rf /var/lib/apt/lists/*

# GNU Arm Embedded 10.3-2021.10, the version upstream CI uses.
RUN set -eux; \
    case "${TARGETARCH:-amd64}" in \
      amd64) host=x86_64 ;; \
      arm64) host=aarch64 ;; \
      *) echo "unsupported arch: $TARGETARCH" >&2; exit 1 ;; \
    esac; \
    curl -fsSL "https://developer.arm.com/-/media/Files/downloads/gnu-rm/${GCC_VERSION}/gcc-arm-none-eabi-${GCC_VERSION}-${host}-linux.tar.bz2" \
      | tar xj -C /opt; \
    ln -s "/opt/gcc-arm-none-eabi-${GCC_VERSION}" /opt/gcc-arm; \
    /opt/gcc-arm/bin/arm-none-eabi-gcc --version | head -1

# yotta + CMake 3.22 (CMake 4 rejects yotta's generated files) + markupsafe 2.0.1
# (2.1 dropped soft_unicode). Versions are a freeze of a known-good native build.
COPY docker/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh

ENV PATH=/opt/gcc-arm/bin:$PATH \
    HOME=/tmp \
    YOTTA_NO_LOGIN=1 \
    PYTHONDONTWRITEBYTECODE=1

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["make", "all"]
