#!/bin/sh
set -e

MODEL_DIR="/app/ml_data"
MARKER_FILE="$MODEL_DIR/.models_created"

mkdir -p "$MODEL_DIR"

if [ -f "$MARKER_FILE" ]; then
    echo "Моделі вже створені $(cat $MARKER_FILE)"
    exit 0
fi

python /app/ml/create_models.py

echo "Created at: $(date)" > "$MARKER_FILE"
