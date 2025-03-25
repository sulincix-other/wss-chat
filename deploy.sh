#!/bin/bash
if [ ! -d venv ] ; then
    python3 -m venv venv
    source venv/bin/activate
    pip3 install websockets
    openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365
fi
source venv/bin/activate
python3 main.py