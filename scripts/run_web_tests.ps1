$ErrorActionPreference = "Stop"

python -m pytest -m smoke --browser chrome @args

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
