#!/bin/bash

export FLASK_APP=$(pwd)/autoapp.py
export FLASKAPP_SECRET=kjfdhdfkjiuetyrkhjg
export FLASK_DEBUG=0

export FLASK_SERVER_PORT=80
export FLASK_SERVER_INTERFACES=0.0.0.0

echo "Initialising the server...."
flask run --port=$FLASK_SERVER_PORT --host=$FLASK_SERVER_INTERFACES
