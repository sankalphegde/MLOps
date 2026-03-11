# Lab 4 - Docker Lab 1 (Customized)

This lab containerizes a simple Python app that prints environment-based
configuration and runtime details. It is intentionally different from the
reference lab by adding environment variables and runtime metadata output.

## What Was Changed
- Custom app logic in `src/app.py` (prints app name, city, UTC time, and metadata).
- New environment variables: `APP_NAME`, `CITY`, `GREETING`, `SHOW_DETAILS`.
- New Dockerfile with explicit runtime defaults.
- Added `.dockerignore`.

## Build
```bash
cd "Lab 4"
docker build -t docker-lab1-custom:1.0 .
```

## Run (default values)
```bash
docker run --rm docker-lab1-custom:1.0
```

## Run (custom values)
```bash
docker run --rm \
  -e APP_NAME="MLOps Docker Lab 1" \
  -e CITY="Boston" \
  -e GREETING="Hi from Docker" \
  -e SHOW_DETAILS="false" \
  docker-lab1-custom:1.0
```

## Expected Output
```text
Greeting: Hi from Docker
App: MLOps Docker Lab 1
City: Boston
UTC Time: 2026-03-10T01:23:45+00:00
Hostname: <container-id>
User: <user>
Python: hidden
Platform: hidden
```
