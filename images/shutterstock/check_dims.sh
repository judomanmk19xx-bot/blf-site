#!/bin/bash
cd /Users/tringuyen/.buzz/OUTBOX/BLF_PROFILE/images/shutterstock_final
for f in *.jpg; do
  dims=$(sips -g pixelWidth -g pixelHeight "$f" 2>/dev/null | grep pixel | awk '{print $2}' | paste -sd'x' -)
  echo "$f: $dims"
done
