# Requires: PowerShell
# Purpose: Install rich-tree to the current user environment and add the user Scripts dir to PATH

param()

$ErrorActionPreference = "Stop"

Write-Host "[1/3] Installing rich-tree to the current user (pip --user) ..." -ForegroundColor Cyan

$installCode = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -m pip install --user . --disable-pip-version-check
    $installCode = $LASTEXITCODE
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python -m pip install --user . --disable-pip-version-check
    $installCode = $LASTEXITCODE
} else {
    Write-Error "Neither 'py' nor 'python' command was found in PATH. Please install Python first."
}

if ($installCode -ne 0) {
    Write-Error ("pip install failed with exit code {0}" -f $installCode)
}

Write-Host "[2/3] Detecting user Scripts directory ..." -ForegroundColor Cyan

# Build candidate Scripts directories (versioned + unversioned)
$pyCmd = if (Get-Command py -ErrorAction SilentlyContinue) { 'py' } elseif (Get-Command python -ErrorAction SilentlyContinue) { 'python' } else { $null }

$userBase = $null
$userSite = $null
if ($pyCmd) {
    $userBase = & $pyCmd -c "import site; print(site.USER_BASE)"
    $userSite = & $pyCmd -c "import site; print(site.getusersitepackages())"
}

$candidates = @()
if ($userBase) { $candidates += (Join-Path $userBase 'Scripts') }
if ($userSite) { $candidates += (Join-Path (Split-Path $userSite -Parent) 'Scripts') }
$candidates += (Join-Path $env:USERPROFILE 'AppData\Roaming\Python\Python310\Scripts')
$candidates += (Join-Path $env:USERPROFILE 'AppData\Roaming\Python\Scripts')

$uniqueCandidates = $candidates | Where-Object { $_ } | Select-Object -Unique
Write-Host "Candidate Scripts directories:" -ForegroundColor Yellow
foreach ($c in $uniqueCandidates) { Write-Host " - $c" -ForegroundColor Yellow }

Write-Host "[3/3] Ensuring user PATH contains the Scripts directory(ies) ..." -ForegroundColor Cyan

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not $userPath) { $userPath = "" }
$pathParts = $userPath.Split(';') | Where-Object { $_ -ne '' }

$added = @()
foreach ($dir in $uniqueCandidates) {
    if (-not (Test-Path $dir)) { continue }
    $inPath = $pathParts | Where-Object { $_.TrimEnd('\\') -ieq $dir.TrimEnd('\\') } | ForEach-Object { $_ }
    if (-not $inPath) {
        $pathParts += $dir
        $added += $dir
    }
}

if ($added.Count -gt 0) {
    $newPath = ($pathParts -join ';')
    & setx Path "$newPath" | Out-Null
    Write-Host "Added to user PATH:" -ForegroundColor Green
    foreach ($a in $added) { Write-Host " - $a" -ForegroundColor Green }
} else {
    Write-Host "User PATH already contains appropriate Scripts directory." -ForegroundColor Green
}

# Show where the rich-tree executable exists
$exePaths = @()
foreach ($dir in $uniqueCandidates) {
    $p = Join-Path $dir 'rich-tree.exe'
    if (Test-Path $p) { $exePaths += $p }
}
if ($exePaths.Count -gt 0) {
    Write-Host "Found rich-tree here:" -ForegroundColor Cyan
    foreach ($p in $exePaths) { Write-Host " - $p" -ForegroundColor Cyan }
}

Write-Host "Done. Please open a NEW terminal, then run: rich-tree" -ForegroundColor Magenta


