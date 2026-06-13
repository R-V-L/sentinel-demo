#!/bin/bash
set -e

PORT="${PORT:-5100}"
HOST="${HOST:-127.0.0.1}"

echo "=== Sentinel Hardware Demo ==="
echo "Starting at http://${HOST}:${PORT}"
echo ""
echo "  Simple:  http://${HOST}:${PORT}/simple/"
echo "  Guarded: http://${HOST}:${PORT}/guard/"
echo "  Dynamic: http://${HOST}:${PORT}/dynamic/"
echo ""

exec uv run --with flask --with gunicorn gunicorn app:app \
    --bind="${HOST}:${PORT}" \
    --workers=1 \
    --reload \
    --access-logfile=-
