FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
      cron ca-certificates git tini && \
    rm -rf /var/lib/apt/lists/*

# Get the branch with locking/time control
WORKDIR /opt/app
RUN git clone https://github.com/radamhu/familylink.git . && \
    pip install --no-cache-dir .

# runtime files + logs
RUN mkdir -p /data /var/log/cron
VOLUME ["/data"]

# copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV TZ=UTC
ENTRYPOINT ["/usr/bin/tini","--","/entrypoint.sh"]
