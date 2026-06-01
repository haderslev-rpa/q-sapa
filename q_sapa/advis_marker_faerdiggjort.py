from playwright.async_api import Page
from q_haderslev_vbo.playwright.playwright_debughelper import PlaywrightDebugHelper


# ==================================================
# ✅ XPATH
# ==================================================
FAERDIGGOER_XPATH = "//button[@id='faerdiggoer']"


# ==================================================
# ✅ FUNKTION
# ==================================================
async def advis_marker_faerdiggjort(
    page: Page,
    url_til_advis: str,
    timeout: int = 15000,
    debug: bool = False
) -> None:

    dbg = PlaywrightDebugHelper(debug=debug)

    try:
        print("🔗 Åbner advis...")

        # ---------------------------------------------
        # ✅ 1) Gå til advis
        # ---------------------------------------------
        await page.goto(url_til_advis)
        await page.wait_for_load_state("networkidle")

        if debug:
            await dbg.screenshot(page, "STEP_advis_loaded")

        # ---------------------------------------------
        # ✅ 2) Klik “Færdiggør”
        # ---------------------------------------------
        print("🔍 Finder 'Færdiggør'...")

        faerdig_btn = page.locator(f"xpath={FAERDIGGOER_XPATH}")
        await faerdig_btn.wait_for(state="visible", timeout=timeout)

        await faerdig_btn.click()

        print("✅ Advis markeret som færdiggjort")

        if debug:
            await dbg.screenshot(page, "STEP_faerdiggjort")

    except Exception:
        if debug:
            await dbg.screenshot(page, "FEJL_faerdiggoer")
        raise