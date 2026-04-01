#!/usr/bin/env bash
# Simple deploy helper for PythonAnywhere
# Requires env vars: PYUSERNAME, DOMAIN, PA_TOKEN, BRANCH (optional, default main)

BRANCH=${BRANCH:-main}

set -euo pipefail

echo "Committing local changes (if any)..."
git add -A || true
if ! git diff --staged --quiet; then
  git commit -m "Deploy: $BRANCH" || true
fi

echo "Pushing branch $BRANCH to origin..."
git push origin $BRANCH

if [ -z "${PYUSERNAME:-}" ] || [ -z "${DOMAIN:-}" ] || [ -z "${PA_TOKEN:-}" ]; then
  echo "Environment variables PYUSERNAME, DOMAIN and PA_TOKEN must be set." >&2
  exit 1
fi

API_URL="https://www.pythonanywhere.com/api/v0/user/${PYUSERNAME}/webapps/${DOMAIN}/reload/"
echo "Triggering PythonAnywhere reload for ${DOMAIN}..."

resp=$(curl -s -X POST -H "Authorization: Token ${PA_TOKEN}" -H "Content-Type: application/json" "${API_URL}" || true)
if [ -z "$resp" ]; then
  echo "Reload request failed or returned empty response." >&2
  echo "After pushing, run migrations and collectstatic on PythonAnywhere via Bash console:" >&2
  echo "  cd ~/your-repo && git pull && workon <virtualenv> && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput" >&2
  exit 1
fi

echo "Reload response: $resp"
#!/usr/bin/env bash
set -euo pipefail

# Deploy script for PythonAnywhere
# Usage:
#   export PYUSERNAME=myusername
#   export DOMAIN=aaditech2.pythonanywhere.com
#   export PA_TOKEN=<your-pythonanywhere-api-token>
#   ./scripts/deploy_pythonanywhere.sh [branch]

BRANCH=${1:-main}
COMMIT_MSG=${DEPLOY_MSG:-"Deploy: ${BRANCH}"}

echo "Running pre-deploy checks..."
git status --porcelain

echo "Committing any local changes (if present)..."
git add -A
git commit -m "$COMMIT_MSG" || echo "No changes to commit"

echo "Pushing branch '$BRANCH' to origin..."
git push origin "$BRANCH"

if [ -z "${PYUSERNAME:-}" ] || [ -z "${DOMAIN:-}" ] || [ -z "${PA_TOKEN:-}" ]; then
  echo "Environment variables PYUSERNAME, DOMAIN and PA_TOKEN must be set."
  echo "Example: export PYUSERNAME=myuser; export DOMAIN=aaditech2.pythonanywhere.com; export PA_TOKEN=xxxx"
  exit 1
fi

echo "Triggering PythonAnywhere webapp reload for $DOMAIN..."
API_URL="https://www.pythonanywhere.com/api/v0/user/$PYUSERNAME/webapps/$DOMAIN/reload/"

HTTP_RESPONSE=$(curl -s -w "HTTPSTATUS:%{http_code}" -X POST "$API_URL" -H "Authorization: Token $PA_TOKEN" -H "Content-Type: application/json")
HTTP_BODY=$(echo "$HTTP_RESPONSE" | sed -e 's/HTTPSTATUS:.*//g')
HTTP_STATUS=$(echo "$HTTP_RESPONSE" | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

echo "API status: $HTTP_STATUS"
echo "$HTTP_BODY"

if [ "$HTTP_STATUS" -ne 200 ] && [ "$HTTP_STATUS" -ne 202 ]; then
  echo "Reload failed (status $HTTP_STATUS). You may need to run migrations and collectstatic on PythonAnywhere."
  echo "See the README in this repo for manual post-deploy commands."
  exit 1
fi

echo "Reload triggered successfully."
echo "Note: run migrations and collectstatic on PythonAnywhere via the Web console or a bash console:"
echo "  cd ~/your-repo && git pull && workon <virtualenv> && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput"
