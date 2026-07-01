FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY . .

EXPOSE 8000

# Shell form (not exec form) so ${PORT} expands — Render injects PORT and
# expects the app to bind to it; falls back to 8000 for local docker-compose.
# --proxy-headers trusts X-Forwarded-For from the platform's load balancer,
# which rate limiting (rate_limiter.py) needs to see the real client IP.
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'