param([string]$BlenderPath, [switch]$CheckOnly)
$ErrorActionPreference = 'Stop'

function Find-Blender {
    if ($BlenderPath) {
        if (-not (Test-Path -LiteralPath $BlenderPath -PathType Leaf)) { throw 'BlenderPath does not exist.' }
        return (Resolve-Path -LiteralPath $BlenderPath).Path
    }
    $found = Get-Command blender -ErrorAction SilentlyContinue
    if ($found) { return $found.Source }
    $base = Join-Path $env:ProgramFiles 'Blender Foundation'
    if (Test-Path -LiteralPath $base) {
        $found = Get-ChildItem -LiteralPath $base -Directory |
            Where-Object { $_.Name -match '^Blender \d+\.\d+' } |
            Sort-Object { [version]([regex]::Match($_.Name, '\d+\.\d+').Value) } -Descending |
            ForEach-Object { Join-Path $_.FullName 'blender.exe' } |
            Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
        return $found
    }
    return $null
}

function Find-Uv {
    $found = Get-Command uv -ErrorAction SilentlyContinue
    if ($found) { return $found.Source }
    foreach ($candidate in @("$env:USERPROFILE\.local\bin\uv.exe", "$env:LOCALAPPDATA\Microsoft\WinGet\Links\uv.exe")) {
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }
    return $null
}

function Install-Package([string]$Id) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw "Install $Id using its official installer; winget is unavailable." }
    & winget install --id $Id --exact --source winget --accept-package-agreements --accept-source-agreements --silent
    if ($LASTEXITCODE -ne 0) { throw "winget installation failed: $Id (exit $LASTEXITCODE)" }
    $env:PATH = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User') + ';' + $env:PATH
}

$blender = Find-Blender
$uv = Find-Uv
if ($CheckOnly) {
    [pscustomobject]@{ Blender = $blender; Uv = $uv; BlenderRunning = [bool](Get-Process blender -ErrorAction SilentlyContinue) } | ConvertTo-Json
    exit 0
}
if (Get-Process blender -ErrorAction SilentlyContinue) { throw 'Save your work and close Blender, then run this installer again. No processes were stopped.' }
if (-not $blender) { Install-Package 'BlenderFoundation.Blender'; $blender = Find-Blender }
if (-not $uv) { Install-Package 'astral-sh.uv'; $uv = Find-Uv }
if (-not $blender -or -not $uv) { throw 'Executable not found after installation. Restart the terminal or pass -BlenderPath.' }
$uvx = Join-Path (Split-Path -Parent $uv) 'uvx.exe'
if (-not (Test-Path -LiteralPath $uvx)) {
    $command = Get-Command uvx -ErrorAction SilentlyContinue
    if (-not $command) { throw 'uvx was not found. Repair the uv installation.' }
    $uvx = $command.Source
}
$env:DISABLE_TELEMETRY = 'true'
& $uv run --no-project --python 3.11 --with 'blender-mcp==1.9.1' python (Join-Path $PSScriptRoot 'setup_blender.py') --blender $blender --uvx $uvx
if ($LASTEXITCODE -ne 0) { throw "Setup failed (exit $LASTEXITCODE). Existing work was not closed or deleted." }
Write-Host 'Installation finished. Open Blender and restart the Codex session; then verify scene info and a screenshot.'
