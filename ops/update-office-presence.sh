#!/bin/bash
set -euo pipefail
cd /Users/obsidianassistant/clawd/apps/Star-Office-UI
/usr/local/bin/python3.12 scripts/update_office_presence.py >> /tmp/star-office-presence.log 2>&1
