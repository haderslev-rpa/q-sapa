from playwright.async_api import Page
from q_haderslev_vbo.playwright.faelles_kommunal_login_idp import (
    login_via_faelles_kommunal_idp
)
from q_haderslev_vbo.playwright.playwright_debughelper import PlaywrightDebugHelper


async def launch_sapa(
    page: Page,
    advis: bool = False,
    overblik: bool = False,
    debug: bool = False
) -> Page:

    dbg = PlaywrightDebugHelper(debug=debug)

    try:
        # ---------------------------------------------
        # ✅ Valider input (KRAV: præcis én True)
        # ---------------------------------------------
        if advis == overblik:
            raise ValueError(
                "❌ Du skal vælge præcis én: advis=True eller overblik=True"
            )

        # ---------------------------------------------
        # ✅ Vælg URL
        # ---------------------------------------------
        if advis:
            SAPA_URL = "https://sapaadvis.dk/"
        else:
            SAPA_URL = "https://sapaoverblik.dk/"

        print(f"🌐 Starter SAPA: {SAPA_URL}")

        # ---------------------------------------------
        # ✅ 1) Gå til SAPA
        # ---------------------------------------------
        await page.goto(SAPA_URL)
        await page.wait_for_load_state("domcontentloaded")

        if debug:
            await dbg.screenshot(page, "STEP_1_startside")

        # ---------------------------------------------
        # ✅ 2) Vælg kommune hvis nødvendigt
        # ---------------------------------------------
        locator = page.locator("#SelectedAuthenticationUrl")

        if await locator.count() > 0:
            print("🔐 Vælger kommune...")

            await locator.select_option(label="Haderslev Kommune")
            await page.locator("#btnOK").click()
            await page.wait_for_load_state("networkidle")

            if debug:
                await dbg.screenshot(page, "STEP_2_kommune_valgt")

        # ---------------------------------------------
        # ✅ 3) Login (FKI)
        # ---------------------------------------------
        print("🔐 Logger ind via FKI...")

        await login_via_faelles_kommunal_idp(
            page=page,
            credential_name="DIRXOPS",
            debug=debug
        )

        if debug:
            await dbg.screenshot(page, "STEP_3_efter_login")

        # ---------------------------------------------
        # ✅ 4) Reload SAPA efter login
        # ---------------------------------------------
        await page.goto(SAPA_URL)
        await page.wait_for_load_state("networkidle")

        if debug:
            await dbg.screenshot(page, "STEP_4_klar")

        return page

    except Exception as e:
        if debug:
            await dbg.screenshot(page, "FEJL_launch_sapa")
        raise