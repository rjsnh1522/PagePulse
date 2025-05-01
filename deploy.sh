# deploy.sh

# Define the path to your JS file
JS_FILE="static/tracker.js"

# Determine if it's a production or local environment
if [ "$RAILWAY_ENV" == "production" ]; then
    API_URL="https://pagepulse-production.up.railway.app/v1/analytics"
else
    API_URL="http://localhost:8080/v1/analytics"
fi

# Replace API_URL in the JavaScript file
sed -i '' "s|const API_URL = .*|const API_URL = \"$API_URL\";|" $JS_FILE

# Print the value to ensure it's correctly replaced
echo "API_URL set to: $API_URL"
