$ErrorActionPreference = "Stop"
$env:SELENIUM_REMOTE_URL = "http://localhost:4444"

Write-Host "Running Chrome smoke tests through Selenium Grid..."
python -m pytest -m smoke --browser chrome
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Running Firefox smoke tests through Selenium Grid..."
python -m pytest -m smoke --browser firefox
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
