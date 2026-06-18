
from q_haderslev_vbo.playwright.faelles_kommunal_login_idp import (
    login_via_faelles_kommunal_idp
)

from q_sapa.selectors import SAPASelectors


async def launch_sapa(
    page,
    session,
    advis: bool = False,
    overblik: bool = False,
):

    # ---------------------------------------------
    # ✅ Valider input
    # ---------------------------------------------
    if advis == overblik:
        raise ValueError(
            "❌ Du skal vælge præcis én: advis=True eller overblik=True"
        )

    # ---------------------------------------------
    # ✅ Vælg URL
    # ---------------------------------------------
    SAPA_URL = "https://sapaadvis.dk/" if advis else "https://sapaoverblik.dk/"

    print(f"🌐 Går til SAPA: {SAPA_URL}")

    await page.goto(SAPA_URL)
    await page.wait_for_load_state("domcontentloaded")

    await session.screenshot(page, "STEP_1_startside")

    # ---------------------------------------------
    # ✅ Check login nødvendigt
    # ---------------------------------------------
    locator = page.locator(SAPASelectors.Login.MUNICIPALITY_SELECT)

    if await locator.count() > 0:
        print("🔐 Ikke logget ind – starter login")

        await locator.select_option(label="Haderslev Kommune")
        await page.locator(SAPASelectors.Login.OK_BUTTON).click()

        await page.wait_for_load_state("networkidle")

        await session.screenshot(page, "STEP_2_kommune")

        await login_via_faelles_kommunal_idp(
            page,
            session=session,
            credential_name="DIRXOPS"
        )

        # ---------------------------------------------
        # ✅ Vent på redirect fra IDP
        # ---------------------------------------------
        print("⏳ Venter på redirect fra IDP...")

        for _ in range(5):
            if "idp" in page.url.lower():
                await page.wait_for_timeout(1500)
            else:
                break

        # ---------------------------------------------
        # ✅ Hvis stadig på IDP → force tilbage
        # ---------------------------------------------
        if "idp" in page.url.lower():
            print("⚠️ Stadig på IDP – tvinger tilbage til SAPA")
            await page.goto(SAPA_URL)

        await page.wait_for_load_state("networkidle")

    else:
        print("✅ Allerede logget ind i SAPA")

    # ---------------------------------------------
    # ✅ Final
    # ---------------------------------------------
    await session.screenshot(page, "STEP_4_klar")

    print("✅ SAPA klar:", page.url)