#!/bin/bash
set -e
# Export BUZZ env from Orchestrator harness PID 28374
eval "$(ps eww -p 28374 | tr ' ' '\n' | grep -E '^BUZZ_[A-Z_]+=' | sed 's/^/export /')"
cd /Users/tringuyen/.buzz/OUTBOX/BLF_PROFILE/images/shutterstock
cat .scratch_msg.txt | /Users/tringuyen/.hermes/bin/buzz messages send \
  --channel f5884238-adbb-4617-9b36-765b8551af46 \
  --reply-to 2074d4b44a2aedabe8dac2135dc760ee38ea077ef518ab395a1cf02b2b842cfb \
  --mention dcbcb8a774f61037d25436a9b669386763fa550af4bbcb2043db8389c7648009 \
  --file contact_processing_line.jpg \
  --file contact_qc_lab.jpg \
  --file contact_cold_storage.jpg \
  --file contact_matcha_tea.jpg \
  --file contact_hero_factory.jpg \
  --content -
