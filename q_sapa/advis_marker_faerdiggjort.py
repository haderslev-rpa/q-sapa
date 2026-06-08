from playwright.async_api import Page

# ==================================================
# ✅ XPATH
# ==================================================
FAERDIGGOER_XPATH = "//button[@id='faerdiggoer']"


# ==================================================
# ✅ FUNKTION
# ==================================================
async def advis_marker_faerdiggjort(
    page: Page,
    session,
    url_til_advis: str,
    timeout: int = 15000,
) -> None:

    try:
        print("🔗 Åbner advis...")

        # ---------------------------------------------
        # ✅ 1) Gå til advis
        # ---------------------------------------------
        await page.goto(url_til_advis)
        await page.wait_for_load_state("networkidle")

        await session.recorder.screenshot(page, "STEP_advis_loaded")

        # ---------------------------------------------
        # ✅ 2) Klik “Færdiggør”
        # ---------------------------------------------
        print("🔍 Finder 'Færdiggør'...")

        faerdig_btn = page.locator(f"xpath={FAERDIGGOER_XPATH}")
        await faerdig_btn.wait_for(state="visible", timeout=timeout)

        await faerdig_btn.click()

        # ✅ 🔥 0,5 sekund wait efter klik
        await page.wait_for_timeout(500)

        print("✅ Advis markeret som færdiggjort")

        await session.recorder.screenshot(page, "STEP_faerdiggjort")

    except Exception:
        # ---------------------------------------------
        # ✅ Fejlscreenshot
        # ---------------------------------------------
        await session.recorder.screenshot(page, "FEJL_faerdiggoer")
        raise