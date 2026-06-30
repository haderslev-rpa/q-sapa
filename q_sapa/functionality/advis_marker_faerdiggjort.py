from q_sapa.selectors import SAPASelectors
from q_haderslev_vbo.playwright.faelles_kommunal_login_idp import (
    login_via_faelles_kommunal_idp
)


async def advis_marker_faerdiggjort(
    page,
    session,
    url_til_advis: str,
    advis: bool = True,
    overblik: bool = False
):
    """
    Logger ind i SAPA og markerer advis som færdiggjort
    """

    # ---------------------------------------------
    # ✅ Valider input
    # ---------------------------------------------
    if advis == overblik:
        raise ValueError("❌ Vælg advis eller overblik")

    # ---------------------------------------------
    # ✅ SAPA start URL
    # ---------------------------------------------
    SAPA_URL = "https://sapaadvis.dk/" if advis else "https://sapaoverblik.dk/"

    print("🌐 Går til SAPA startside")
    await page.goto(SAPA_URL)

    # ---------------------------------------------
    # ✅ Vent på basis load
    # ---------------------------------------------
    await page.wait_for_load_state("networkidle")

    # ---------------------------------------------
    # ✅ Check login
    # ---------------------------------------------
    kommune_dropdown = page.locator(SAPASelectors.Login.MUNICIPALITY_SELECT)

    if await kommune_dropdown.count() > 0:
        print("🔐 Ikke logget ind – logger ind")

        await kommune_dropdown.wait_for(state="visible")

        await kommune_dropdown.select_option(label="Haderslev Kommune")
        await page.locator(SAPASelectors.Login.OK_BUTTON).click()

        await page.wait_for_load_state("networkidle")

        await login_via_faelles_kommunal_idp(
            page,
            session=session,
            credential_name="DIRXOPS"
        )

        # ✅ Vent på redirect fra IDP
        await page.wait_for_url("**sapa**", timeout=20000)
        await page.wait_for_load_state("networkidle")

    else:
        print("✅ Allerede logget ind")

    # --------------------------------------------------
    # ✅ STABIL: Fællessøgninger (din gode løsning)
    # --------------------------------------------------
    
    
    await page.locator(
        SAPASelectors.Frontpage_advis.FAELLESSOEGER_TABLE
    ).wait_for(
        state="visible",
        timeout=15000
    )


    print("✅ SAPA klar")

    # --------------------------------------------------
    # ✅ Gå til advis URL
    # --------------------------------------------------
    print("🌐 Går til advis")

    await page.goto(url_til_advis)

    # ✅ Robust URL wait (pattern)
    await page.wait_for_url("**AdvisDetails**", timeout=15000)

    await page.wait_for_load_state("networkidle")

    # --------------------------------------------------
    # ✅ Vent på FÆRDIGGØR knap
    # --------------------------------------------------
    faerdiggoer_btn = page.locator(
        SAPASelectors.Advis.FAERDIGGOER
    )

    await faerdiggoer_btn.wait_for(
        state="visible",
        timeout=15000
    )

    # --------------------------------------------------
    # ✅ Sikkerhed: korrekt side
    # --------------------------------------------------
    if url_til_advis not in page.url:
        print("⚠️ URL matcher ikke 100%, men fortsætter")

    # buffer mod timing issues
    await page.wait_for_timeout(1000)

    # --------------------------------------------------
    # ✅ Klik færdiggør
    # --------------------------------------------------
    await faerdiggoer_btn.click()

    print("✅ Advis færdiggjort")