#!/usr/bin/env bash
# find_empty_date_folders.sh
# Recursively finds (and optionally deletes) empty folders matching yyyy-mm-dd
#
# Usage:
#   ./find_empty_date_folders.sh <directory>           # list only
#   ./find_empty_date_folders.sh <directory> --delete  # list + delete

set -uo pipefail

# -- Arguments ----------------------------------------------------------------
TARGET_DIR="${1:-}"
DELETE=false

shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --delete) DELETE=true ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

if [[ -z "$TARGET_DIR" ]]; then
  echo "Usage: $0 <directory> [--delete]" >&2
  exit 1
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Error: '$TARGET_DIR' is not a valid directory." >&2
  exit 1
fi

TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

# -- Pattern: yyyy-mm-dd with range validation ---------------------------------
DATE_REGEX='^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'

# -- Search -------------------------------------------------------------------
echo "=== $(date '+%Y-%m-%d %H:%M:%S') ==="
found=0

mapfile -d '' dirs < <(find "$TARGET_DIR" -mindepth 1 -type d -print0 2>/dev/null || true)

for dir in "${dirs[@]+"${dirs[@]}"}"; do
  basename="$(basename "$dir")"
  if [[ "$basename" =~ $DATE_REGEX ]]; then
    if [[ -d "$dir" && -z "$(ls -A "$dir" 2>/dev/null)" ]]; then
      rel_path="${dir#"$TARGET_DIR"/}"
      if [[ "$DELETE" == true ]]; then
        rmdir "$dir"
      fi
      echo "$rel_path"
      ((found++)) || true
    fi
  fi
done

# -- Summary ------------------------------------------------------------------
if [[ $found -eq 0 ]]; then
  exit 0
elif [[ "$DELETE" == true ]]; then
  echo "Deleted $found empty date folder(s)."
else
  echo "Found $found empty date folder(s)."
fi