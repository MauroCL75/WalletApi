#!/bin/sh

docker run -d -p 8000:8000 --name walletApi --restart=unless-stopped walletapi:latest uvicorn --host 0.0.0.0 main:app
