#!/bin/bash

set -e  # Exit on any error

# Apply database migrations
make mig

# Collect static files
make collect

echo ""
echo "========== Starting Tunnels =========="

# Start jprq tunnel
if [ -n "$JPRQ_AUTH_KEY" ]; then
  echo "Authenticating jprq..."
  jprq auth "$JPRQ_AUTH_KEY"
  echo "Starting jprq tunnel on port 8000..."
  jprq http 8000 -s "$JPRQ_URL" > jprq.log 2>&1 &
  sleep 2
  JPRQ_URL=$(grep -o 'https://[a-zA-Z0-9.-]*\.jprq\.site' jprq.log | head -n1)
fi

# Start ngrok tunnel
NGROK_URL=""
if [ -n "$NGROK_AUTH_TOKEN" ]; then
  echo "Authenticating ngrok..."
  ngrok config add-authtoken "$NGROK_AUTH_TOKEN"
  echo "Starting ngrok tunnel on port 1298..."
  ngrok http 8000 > /dev/null &
  sleep 2
  NGROK_URL=$(curl --silent http://localhost:4040/api/tunnels \
    | grep -o 'https://[a-zA-Z0-9.-]*\.ngrok-free\.app' | head -n1)
fi

# Show tunnel URLs
echo ""
echo "========== Public URLs =========="
[ -n "$JPRQ_URL" ] && echo "🌀 jprq  → $JPRQ_URL"
[ -n "$NGROK_URL" ] && echo "🚀 ngrok → $NGROK_URL"
echo "================================="

# Start the Uvicorn ASGI server
echo "Starting Uvicorn ASGI server..."
make run-asgi