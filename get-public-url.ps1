param(
    [int]$Port = 8000,
    [string]$Url = "http://localhost:8000",
    [int]$WaitSeconds = 40
)

$ErrorActionPreference = "Stop"

function Test-PortOpen {
    param([int]$Port)
    try { return Test-NetConnection -ComputerName "127.0.0.1" -Port $Port -InformationLevel Quiet } catch { return $false }
}

if (-not (Test-PortOpen -Port $Port)) {
    $venvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
    $pythonExe = if (Test-Path $venvPython) { $venvPython } else { "python" }
    Start-Process -FilePath $pythonExe -ArgumentList "manage.py runserver 0.0.0.0:$Port" -WorkingDirectory $PSScriptRoot
    Start-Sleep -Seconds 2
}

$cloudflaredCmd = Get-Command cloudflared -ErrorAction SilentlyContinue
if (-not $cloudflaredCmd) {
    Write-Output "CLOUDFLARED_NOT_FOUND"
    exit 1
}

$logOut = Join-Path $env:TEMP ("cloudflared-" + [guid]::NewGuid().ToString() + ".out.log")
$logErr = Join-Path $env:TEMP ("cloudflared-" + [guid]::NewGuid().ToString() + ".err.log")

Start-Process -FilePath $cloudflaredCmd.Source -ArgumentList "tunnel --url $Url --no-autoupdate --loglevel info" -RedirectStandardOutput $logOut -RedirectStandardError $logErr | Out-Null

$url = $null
for ($i = 0; $i -lt $WaitSeconds; $i++) {
    Start-Sleep -Seconds 1
    $content = ""
    if (Test-Path $logOut) { $content += (Get-Content $logOut -Raw) }
    if (Test-Path $logErr) { $content += (Get-Content $logErr -Raw) }
    $matches = [regex]::Matches($content, "https://[a-zA-Z0-9-]+\\.trycloudflare\\.com")
    foreach ($m in $matches) {
        if ($m.Value -notlike "https://api.trycloudflare.com") {
            $url = $m.Value
            break
        }
    }
    if ($url) { break }
}

if ($url) {
    Write-Output $url
} else {
    Write-Output "URL_NOT_FOUND"
}
