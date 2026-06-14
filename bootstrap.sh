#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-.}"
TOOL="${2:-auto}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"${ROOT}/scripts/install.sh" --tool "${TOOL}" --target "${TARGET}"
