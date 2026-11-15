#!/bin/bash

set -e

echo "Starting The Last Quest builds..."

gh workflow run build.yml --ref main

sleep 3

RUN_ID=$(gh run list \
    --workflow build.yml \
    --limit 1 \
    --json databaseId \
    --jq '.[0].databaseId')

echo "Watching build #$RUN_ID..."

gh run watch "$RUN_ID" --exit-status

mkdir -p dist

gh run download "$RUN_ID" -D dist

echo "All builds downloaded to ./dist"
