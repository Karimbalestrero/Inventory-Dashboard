from pathlib import Path
from playwright.sync_api import sync_playwright


DASHBOARD_URL = "https://inventory-dashboard-nyy97sztrt6ndzc8nj5dhd.streamlit.app/"

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "dashboard_output"
OUTPUT_FILE = OUTPUT_DIR / "Inventur_Dashboard_Aktuell.png"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


with sync_playwright() as p:

    browser = p.chromium.launch(channel="msedge", headless=True)

    page = browser.new_page(
        viewport={
            "width": 1920,
            "height": 1080,
        }
    )

    page.goto(
        DASHBOARD_URL,
        wait_until="networkidle",
        timeout=120000,
    )
    page.add_style_tag(content="""
        [data-testid="stStatusWidget"],
        [data-testid="stAppDeployButton"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stMainMenu"],
        footer {
            display: none !important;
            visibility: hidden !important;
        }
    """)

    page.mouse.move(10, 10)

    page.screenshot(
        path=str(OUTPUT_FILE),
        full_page=True,
    )

    browser.close()


print(f"Screenshot erstellt: {OUTPUT_FILE}")