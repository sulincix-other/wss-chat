#!/bin/bash
if [ ! -d venv ] ; then
    python3 -m venv venv
    source venv/bin/activate
    pip3 install fastapi uvicorn websockets
fi
source venv/bin/activate
python3 main.py
