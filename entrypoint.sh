#!/usr/bin/env bash
set -euo pipefail

# build crontab from env
: "${CRON_SCHEDULE:?CRON_SCHEDULE env required}"
echo "${CRON_SCHEDULE} /usr/local/bin/python -m familylink.cli /data/config.csv >> /var/log/cron/runner.log 2>&1" > /etc/cron.d/familylink
chmod 0644 /etc/cron.d/familylink
crontab /etc/cron.d/familylink

service cron start

# first-time auth happens on first run if needed
# also run once at boot so policy is applied immediately
python -m familylink.cli /data/config.csv >> /var/log/cron/runner.log 2>&1 || true

tail -F /var/log/cron/runner.log
