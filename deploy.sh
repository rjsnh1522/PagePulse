#!/bin/bash

JS_FILE="static/tracker.js"

if [ "$RAILWAY_ENVIRONMENT" == "production" ]; then
    API_URL="https://pagepulse-production.up.railway.app/v1/analytics"
else
    API_URL="http://localhost:8080/v1/analytics"
fi

echo "Updating API_URL in $JS_FILE to: $API_URL"
echo "OS type $OSTYPE"
# Detect OS and apply correct sed command
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s|const API_URL = .*|const API_URL = \"$API_URL\";|" "$JS_FILE"
else
    # Linux
    sed -i "s|const API_URL = .*|const API_URL = \"$API_URL\";|" "$JS_FILE"
fi

echo "✅ API_URL updated successfully."
