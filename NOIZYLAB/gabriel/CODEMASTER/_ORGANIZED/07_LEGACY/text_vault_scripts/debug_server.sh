#!/bin/bash
echo "Starting Debug Server..."
python3 turbo_server.py > debug_server.log 2>&1
echo "Exit Code: $?" >> debug_server.log
