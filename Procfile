web: bash deploy.sh && gunicorn -k uvicorn.workers.UvicornWorker main:app --workers 2 --bind 0.0.0.0:$PORT --forwarded-allow-ips="*"
