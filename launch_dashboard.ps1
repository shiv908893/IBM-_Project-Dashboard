$ErrorActionPreference = "Stop"

$projectDir = Join-Path $PSScriptRoot "AI_Data_Analyst"
$venvDir = Join-Path $projectDir ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"
$streamlitExe = Join-Path $venvDir "Scripts\streamlit.exe"

if (-not (Test-Path $projectDir)) {
    throw "Project folder not found: $projectDir"
}

if (-not (Test-Path $venvPython)) {
    Write-Host "Creating virtual environment..."
    py -3.14 -m venv $venvDir
}

if (-not (Test-Path $streamlitExe)) {
    Write-Host "Installing project dependencies..."
    & $venvPython -m pip install --upgrade pip
    Set-Location $projectDir
    & $venvPython -m pip install -r requirements.txt
}

$ports = 8501, 8502, 8503, 8504, 8505, 8506, 8507, 8508
$selectedPort = $null
foreach ($port in $ports) {
    $inUse = $false
    try {
        $connections = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
        if ($connections) { $inUse = $true }
    } catch {
        $inUse = $false
    }

    if (-not $inUse) {
        $selectedPort = $port
        break
    }
}

if (-not $selectedPort) {
    throw "No free port found in the default Streamlit range. Please free a port and retry."
}

$env:PYTHONPATH = $projectDir
Set-Location $projectDir

Write-Host "Launching AI Data Analyst dashboard on http://localhost:$selectedPort"
Start-Process "http://localhost:$selectedPort"
& $streamlitExe run app/app.py --server.address 0.0.0.0 --server.port $selectedPort
