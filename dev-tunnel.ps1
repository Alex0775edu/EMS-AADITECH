param(
    [string]$Url = "http://localhost:8000",
    [switch]$StartServer
)

$ErrorActionPreference = "Stop"

function Test-PortOpen {
    param([int]$Port)
    try {
        return Test-NetConnection -ComputerName "127.0.0.1" -Port $Port -InformationLevel Quiet
    } catch {
        return $false
    }
}

if ($StartServer -or -not (Test-PortOpen -Port 8000)) {
    $venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
    $pythonExe = if (Test-Path $venvPython) { $venvPython } else { "python" }
    Write-Host "Starting Django server on 0.0.0.0:8000 using $pythonExe ..."
    Start-Process -FilePath $pythonExe -ArgumentList "manage.py runserver 0.0.0.0:8000" -WorkingDirectory $PSScriptRoot
    Start-Sleep -Seconds 2
}

$cloudflaredCmd = Get-Command cloudflared -ErrorAction SilentlyContinue
if (-not $cloudflaredCmd) {
    Write-Error "cloudflared not found. Install Cloudflare Tunnel (cloudflared) and re-run."
}

$printed = $false
Write-Host "Starting Cloudflare Tunnel for $Url"
Write-Host "Press Ctrl+C to stop."

& $cloudflaredCmd.Source tunnel --url $Url --no-autoupdate 2>&1 | ForEach-Object {
    $line = $_.ToString()
    if (-not $printed -and $line -match 'https://[-a-zA-Z0-9]+\.trycloudflare\.com') {
        $publicUrl = $Matches[0]
        Write-Host ""
        Write-Host "Public URL: $publicUrl"
        $printed = $true
    }
    Write-Host $line
}
