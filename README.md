# E-Commerce QA Automation

A working Selenium and Python automation project for the public [SauceDemo](https://www.saucedemo.com/) e-commerce training application.

The project tests authentication, inventory, cart, and checkout flows using a maintainable Page Object Model. It supports Chrome and Firefox locally or through Docker Selenium Grid, produces HTML and Allure test evidence, captures screenshots on failure, and runs automatically in GitHub Actions.

## Implemented features

- Selenium 4 with Python and pytest
- Page Object Model with reusable browser actions
- Explicit waits without fixed sleeps
- Positive, negative, smoke, regression, and end-to-end scenarios
- Chrome and Firefox cross-browser execution
- Docker Selenium Grid
- Environment-based configuration
- Failure screenshots and Allure attachments
- Self-contained pytest HTML report
- Ruff quality checks
- GitHub Actions browser matrix

## Automated scenarios

| ID | Scenario | Marker |
| --- | --- | --- |
| WEB-LOGIN-001 | Standard user logs in successfully | smoke, regression |
| WEB-LOGIN-002 | Locked user receives the expected error | regression |
| WEB-CART-001 | User adds a backpack to the cart | smoke, regression |
| WEB-CART-002 | User removes a backpack from the cart | regression |
| WEB-CHECKOUT-001 | User completes an order | regression, e2e |

## Project structure

```text
.
├── .github/workflows/web-tests.yml
├── src/ecommerce_qa/
│   ├── config.py
│   ├── driver_factory.py
│   ├── data/users.py
│   └── pages/
├── tests/
├── scripts/
├── docker-compose.yml
└── pyproject.toml
```

## Run on Windows

Prerequisites: Python 3.11 or newer, Git, and Chrome or Firefox.

```powershell
git clone https://github.com/Harigovindbn/ecommerce-qa-automation.git
cd ecommerce-qa-automation
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
python -m pytest -m smoke --browser chrome
```

Open `reports/web-report.html` after the run. Failure screenshots are saved in `screenshots/`, and Allure result files are saved in `allure-results/`.

## Commands

```powershell
# All tests in headless Chrome
python -m pytest --browser chrome

# Visible Chrome smoke test
python -m pytest -m smoke --browser chrome --headed

# Regression tests in Firefox
python -m pytest -m regression --browser firefox

# Code quality
python -m ruff check .

# Allure dashboard, if the Allure CLI is installed
allure serve allure-results
```

## Docker cross-browser execution

```powershell
docker compose up -d
.\scripts\run_grid_tests.ps1
docker compose down
```

The Selenium Grid console is available at `http://localhost:4444`.

## Configuration

Copy `.env.example` to `.env` before changing defaults.

| Variable | Default | Purpose |
| --- | --- | --- |
| `BASE_URL` | `https://www.saucedemo.com/` | Application under test |
| `BROWSER` | `chrome` | `chrome` or `firefox` |
| `HEADLESS` | `true` | Hide or display the browser |
| `SELENIUM_REMOTE_URL` | empty | Selenium Grid endpoint |
| `EXPLICIT_WAIT_SECONDS` | `10` | Explicit-wait timeout |

Command-line options override environment settings.

## CI/CD

Every push and pull request runs:

1. Ruff static analysis and configuration tests
2. Chrome smoke tests in a Selenium Docker container
3. Firefox smoke tests in a Selenium Docker container
4. Upload of HTML reports, screenshots, and Allure results

## Ethical use

This framework targets a public application intended for testing practice. Do not run automated tests against production systems without permission, and never commit real credentials.

## License

MIT
