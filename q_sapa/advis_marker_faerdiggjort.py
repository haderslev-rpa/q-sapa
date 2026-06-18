from q_sapa.selectors import SAPASelectors
from q_haderslev_vbo.playwright.faelles_kommunal_login_idp import (
    login_via_faelles_kommunal_idp
)


async def launch_sapa(page, session, advis: bool = False, overblik: bool = False):

    if advis == overblik:
        raise ValueError("❌ Vælg advis eller overblik")

    SAPA_URL = "https://sapaadvis.dk/" if advis else "https://sapaoverblik.dk/"

    await page.goto(SAPA_URL)
    await page.wait_for_load_state("domcontentloaded")

    locator = page.locator(SAPASelectors.Login.MUNICIPALITY_SELECT)

    if await locator.count() > 0:
        await locator.select_option(label="Haderslev Kommune")
        await page.locator(SAPASelectors.Login.OK_BUTTON).click()

        await login_via_faelles_kommunal_idp(
            page,
            session=session,
            credential_name="DIRXOPS"
        )

        await page.wait_for_load_state("networkidle")