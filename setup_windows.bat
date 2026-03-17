@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

echo [1/6] Detecting Python...
set "PY_CMD="
set "PY_EXE="

where py >nul 2>&1
if not errorlevel 1 (
    for /f "delims=" %%I in ('py -3 -c "import sys; print(sys.executable)" 2^>nul') do set "PY_EXE=%%I"
    if defined PY_EXE set "PY_CMD=py -3"
)

if not defined PY_CMD (
    where python >nul 2>&1
    if not errorlevel 1 (
        for /f "delims=" %%I in ('python -c "import sys; print(sys.executable)" 2^>nul') do set "PY_EXE=%%I"
        if defined PY_EXE set "PY_CMD=python"
    )
)

if not defined PY_CMD (
    echo Python was not found. Installing Python 3.12 with winget...
    where winget >nul 2>&1
    if errorlevel 1 (
        echo ERROR: winget is not available. Install Python manually and rerun this script.
        goto :error
    )

    winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    if errorlevel 1 (
        echo ERROR: Python installation failed.
        goto :error
    )

    where py >nul 2>&1
    if not errorlevel 1 (
        for /f "delims=" %%I in ('py -3 -c "import sys; print(sys.executable)" 2^>nul') do set "PY_EXE=%%I"
        if defined PY_EXE set "PY_CMD=py -3"
    )

    if not defined PY_CMD (
        where python >nul 2>&1
        if not errorlevel 1 (
            for /f "delims=" %%I in ('python -c "import sys; print(sys.executable)" 2^>nul') do set "PY_EXE=%%I"
            if defined PY_EXE set "PY_CMD=python"
        )
    )
)

if not defined PY_EXE (
    if exist "%LocalAppData%\Programs\Python\Python312\python.exe" set "PY_EXE=%LocalAppData%\Programs\Python\Python312\python.exe"
)

if not defined PY_EXE (
    if exist "%ProgramFiles%\Python312\python.exe" set "PY_EXE=%ProgramFiles%\Python312\python.exe"
)

if not defined PY_EXE (
    for /f "delims=" %%I in ('dir /b /s "%LocalAppData%\Programs\Python\Python3*\python.exe" 2^>nul') do (
        set "PY_EXE=%%I"
        goto :python_found
    )
)

:python_found
if not defined PY_EXE (
    echo ERROR: Python executable could not be resolved. Open a new terminal and rerun.
    goto :error
)

echo Using Python: %PY_EXE%

echo [2/7] Configuring PATH for Python...
set "PY_DIR="
set "PY_SCRIPTS="
for %%I in ("%PY_EXE%") do set "PY_DIR=%%~dpI"
set "PY_SCRIPTS=%PY_DIR%Scripts\"

if exist "%PY_DIR%python.exe" set "PATH=%PY_DIR%;%PATH%"
if exist "%PY_SCRIPTS%pip.exe" set "PATH=%PY_SCRIPTS%;%PATH%"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$pyDir = '%PY_DIR%'; $pyScripts = '%PY_SCRIPTS%'; $launcher = Join-Path $env:LocalAppData 'Programs\Python\Launcher'; $current = [Environment]::GetEnvironmentVariable('Path','User'); if ([string]::IsNullOrWhiteSpace($current)) { $current = '' }; $parts = @($current -split ';' | Where-Object { $_ -and $_.Trim() -ne '' }); foreach ($p in @($pyDir, $pyScripts, $launcher)) { if (Test-Path $p) { if ($parts -notcontains $p) { $parts += $p; Write-Host ('Added to User PATH: ' + $p) } else { Write-Host ('Already in User PATH: ' + $p) } } }; [Environment]::SetEnvironmentVariable('Path', ($parts -join ';'), 'User')"

where python >nul 2>&1
if errorlevel 1 (
    echo WARNING: python command is not available in current shell yet.
    echo          User PATH has been updated, so it will work in new terminals.
)

echo [3/7] Creating virtual environment (.venv)...
if not exist ".venv\Scripts\python.exe" (
    "%PY_EXE%" -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment with %PY_EXE%.
        "%PY_EXE%" --version
        goto :error
    )
)

echo [4/7] Installing Python packages...
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip.
    goto :error
)

pip install matplotlib tqdm
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies.
    goto :error
)

echo [5/7] Checking Poppler (pdftops)...
where pdftops >nul 2>&1
if errorlevel 1 (
    echo pdftops was not found. Installing Poppler with winget...
    where winget >nul 2>&1
    if errorlevel 1 (
        echo ERROR: winget is not available. Install Poppler manually and rerun.
        goto :error
    )

    winget install -e --id oschwartz10612.Poppler --accept-source-agreements --accept-package-agreements
    if errorlevel 1 (
        echo winget install by ID failed. Trying install by name...
        winget install --name Poppler --accept-source-agreements --accept-package-agreements
        if errorlevel 1 (
            echo ERROR: Poppler installation failed via winget.
            goto :error
        )
    )
)

echo [6/7] Configuring PATH for pdftops...
set "POPPLER_BIN="

for /d %%D in ("%LOCALAPPDATA%\Microsoft\WinGet\Packages\oschwartz10612.Poppler_*") do (
    for /f "delims=" %%I in ('dir /b /s "%%~fD\pdftops.exe" 2^>nul') do (
        set "POPPLER_BIN=%%~dpI"
        goto :poppler_bin_found
    )
)

for /d %%D in ("%LOCALAPPDATA%\Programs\poppler*") do (
    for /f "delims=" %%I in ('dir /b /s "%%~fD\pdftops.exe" 2^>nul') do (
        set "POPPLER_BIN=%%~dpI"
        goto :poppler_bin_found
    )
)

for /d %%D in ("%ProgramFiles%\poppler*") do (
    for /f "delims=" %%I in ('dir /b /s "%%~fD\pdftops.exe" 2^>nul') do (
        set "POPPLER_BIN=%%~dpI"
        goto :poppler_bin_found
    )
)

:poppler_bin_found
if not defined POPPLER_BIN (
    echo ERROR: pdftops.exe was not found after installation.
    echo        Please install Poppler manually and add its bin folder to PATH.
    goto :error
)

set "PATH=%POPPLER_BIN%;%PATH%"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$bin = '%POPPLER_BIN%'; $current = [Environment]::GetEnvironmentVariable('Path','User'); if ([string]::IsNullOrWhiteSpace($current)) { $current = '' }; $parts = @($current -split ';' | Where-Object { $_ -and $_.Trim() -ne '' }); if ($parts -notcontains $bin) { $parts += $bin; [Environment]::SetEnvironmentVariable('Path', ($parts -join ';'), 'User'); Write-Host 'Added Poppler bin to User PATH.' } else { Write-Host 'Poppler bin already exists in User PATH.' }"

if not exist "%POPPLER_BIN%pdftops.exe" (
    echo ERROR: pdftops executable is not available in detected folder.
    goto :error
)

echo [7/7] Launching kifu GUI...
python kifuGUI.py
goto :end

:error
echo.
echo Setup did not complete successfully.
pause
exit /b 1

:end
echo.
echo Setup completed.
pause
endlocal