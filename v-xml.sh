#!/bin/env bash

files=$(git ls-files 'docs/schemas/*.xml' || true)
if [ -z "$files" ]; then
  echo "No XML files found"
  exit 0
fi
for f in $files; do
  if ! xmllint --xpath "boolean(//*[local-name()='MetadataVersion'])" "$f" 2>/dev/null | grep 'true'; then
    echo "MetadataVersion missing in $f"
    xmllint "$f" # Show the XML file content for debugging
    exit 1
  fi
done
