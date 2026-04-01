Param(
    [string]$Branch = 'main'
)

# Usage:
# $env:PYUSERNAME='myuser'; $env:DOMAIN='aaditech2.pythonanywhere.com'; $env:PA_TOKEN='token'; ./scripts/deploy_pythonanywhere.ps1

Write-Host "Committing local changes (if any)..."
git add -A
try {
    git commit -m "Deploy: $Branch" | Out-Null
} catch {
    Write-Host "No changes to commit"
}

Write-Host "Pushing branch $Branch to origin..."
git push origin $Branch

if (-not $env:PYUSERNAME -or -not $env:DOMAIN -or -not $env:PA_TOKEN) {
    Write-Error "Environment variables PYUSERNAME, DOMAIN and PA_TOKEN must be set."
    exit 1
}

$apiUrl = "https://www.pythonanywhere.com/api/v0/user/$($env:PYUSERNAME)/webapps/$($env:DOMAIN)/reload/"
Write-Host "Triggering PythonAnywhere reload for $($env:DOMAIN)..."

$headers = @{ Authorization = "Token $($env:PA_TOKEN)"; 'Content-Type' = 'application/json' }
try {
    $resp = Invoke-RestMethod -Uri $apiUrl -Method Post -Headers $headers -ErrorAction Stop
    Write-Host "Reload triggered successfully. Response:`n" ($resp | ConvertTo-Json -Depth 3)
} catch {
    Write-Error "Reload failed: $_"
    Write-Host "After pushing, run migrations and collectstatic on PythonAnywhere via Bash console:"
    Write-Host "  cd ~/your-repo && git pull && workon <virtualenv> && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput"
    exit 1
}
