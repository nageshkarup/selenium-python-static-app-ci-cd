#!/bin/bash

# Activate the virtual environment
source .venv/bin/activate

# Start the HTTP server in the background
python3 -m http.server 8000 &
SERVER_PID=$!

# Give the server a moment to start
sleep 3

pytest tests/selenium_script.py

# Kill the server after tests are done
kill $SERVER_PID
