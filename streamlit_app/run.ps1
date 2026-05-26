$ErrorActionPreference = "Stop"

$envPath = Join-Path $PSScriptRoot ".env.local"
$repoRoot = Split-Path $PSScriptRoot -Parent
$pythonPath = Join-Path $repoRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $envPath)) {
    Copy-Item (Join-Path $PSScriptRoot ".env.example") $envPath
    Write-Host "Created .env.local. Add your OPENAI_API_KEY, then rerun this script."
    exit 1
}

Get-Content $envPath | ForEach-Object {
    $line = $_.Trim()
    if (-not $line -or $line.StartsWith("#") -or -not $line.Contains("=")) {
        return
    }

    $name, $value = $line.Split("=", 2)
    [Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), "Process")
}

if (-not $env:OPENAI_API_KEY) {
    Write-Host "Set OPENAI_API_KEY in .env.local before launching the app."
    exit 1
}

& $pythonPath -m streamlit run (Join-Path $PSScriptRoot "app.py")
