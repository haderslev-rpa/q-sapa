from q_haderslev_vbo.playwright.faelles_kommunal_login_idp import (
    login_via_faelles_kommunal_idp
)

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

        # ---------------------------------------------
        # ✅ 1) Gå til SAPA
        # ---------------------------------------------
        await page.goto(SAPA_URL)
        await page.wait_for_load_state("domcontentloaded")

        await session.recorder.screenshot(page, "STEP_1_startside")

        # ---------------------------------------------
        # ✅ 2) Check login nødvendigt (kommune dropdown)
        # ---------------------------------------------
        locator = page.locator("#SelectedAuthenticationUrl")

        if await locator.count() > 0:
            print("🔐 Ikke logget ind – starter login")

            await locator.select_option(label="Haderslev Kommune")
            await page.locator("#btnOK").click()
            await page.wait_for_load_state("networkidle")

            
            await session.recorder.screenshot(page, "STEP_2_kommune")

            # ---------------------------------------------
            # ✅ 3) Login (FKI)
            # ---------------------------------------------
            await login_via_faelles_kommunal_idp(
                page=page,
                credential_name="DIRXOPS",
                session=session
            )

            # ---------------------------------------------
            # ✅ 4) Vent på redirect fra IDP
            # ---------------------------------------------
            print("⏳ Venter på redirect fra IDP...")

            for _ in range(5):
                if "idp" in page.url.lower():
                    await page.wait_for_timeout(1500)
                else:
                    break

            # ---------------------------------------------
            # ✅ Hvis vi stadig hænger på IDP → force tilbage
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

        await session.recorder.screenshot(page, "STEP_4_klar")

        print("✅ SAPA klar:", page.url)