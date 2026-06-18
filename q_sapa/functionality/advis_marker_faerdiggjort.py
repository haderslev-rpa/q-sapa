from q_sapa.selectors import SAPASelectors
from q_haderslev_vbo.playwright.faelles_kommunal_login_idp import (
    login_via_faelles_kommunal_idp
)


async def advis_marker_faerdiggjort(page, session, advis: bool = False, overblik: bool = False):

    # ---------------------------------------------
    # ✅ Valider input
    # ---------------------------------------------
    if advis == overblik:
        raise ValueError("❌ Vælg advis eller overblik")

    # ---------------------------------------------
    # ✅ URL
    # ---------------------------------------------
    SAPA_URL = "https://sapaadvis.dk/" if advis else "https://sapaoverblik.dk/"

    await page.goto(SAPA_URL)
    await page.wait_for_load_state("domcontentloaded")

    # ---------------------------------------------
    # ✅ Check login nødvendigt
    # ---------------------------------------------
    kommune_dropdown = page.locator(SAPASelectors.Login.MUNICIPALITY_SELECT)

    if await kommune_dropdown.count() > 0:
        await kommune_dropdown.wait_for(state="visible")

        await kommune_dropdown.select_option(label="Haderslev Kommune")
        await page.locator(SAPASelectors.Login.OK_BUTTON).click()

        # ✅ Vent på navigation efter OK klik
        await page.wait_for_load_state("networkidle")

        # ---------------------------------------------
        # ✅ Login via IDP
        # ---------------------------------------------
        await login_via_faelles_kommunal_idp(
            page,
            session=session,
            credential_name="DIRXOPS"
        )

        # ---------------------------------------------
        # ✅ Vent på redirect tilbage fra IDP
        # ---------------------------------------------
        await page.wait_for_load_state("networkidle")

    # ---------------------------------------------
    # ✅ Klar
    # ---------------------------------------------
    return
