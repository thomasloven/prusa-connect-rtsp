# Prusa Connect RTSP

Grab frames from a RTSP stream and publish them to Prusa connect

## Run from docker image

```bash
# Update the environment variables to suit your needs
# PRUSA_CONNECT_FINGERPRINT is a unique string that you can choose (16 characters or more).
# A UUID works well. Ex: https://duckduckgo.com/?hps=1&q=uuid&atb=v363-1&ia=answer
docker run \
    -e PRUSA_CONNECT_RTSP_URL="rtsp://USERNAME:PASSWORD@HOSTNAMEorIP:554/stream1" \
    -e PRUSA_CONNECT_FINGERPRINT="***" \
    -e PRUSA_CONNECT_TOKEN="***" \
    -e LOGURU_LEVEL=INFO \
    ghcr.io/beccazero/prusa-connect-rtsp:main
```

## Run locally

```bash
git clone https://github.com/beccazero/prusa-connect-rtsp.git
cd prusa-connect-rtsp
poetry install

# Create a .env file from the example
cp .env.example .env
# Modify the .env file with your values
vim .env

python prusa_connect_rtsp/main.py
```

## Build and run docker container

```bash
# Create a .env file from the example
cp .env.example .env
# Modify the .env file with your values
vim .env
# Build the container
docker build -t prusa-connect-rtsp
# Start the container
docker run --env-file .env prusa-connect-rtsp 
```
