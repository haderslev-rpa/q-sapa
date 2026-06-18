import asyncio

from q_haderslev_vbo.playwright.browser_session import BrowserSession

from q_sapa.functionality import launch_sapa, soeg_advis


async def main():

    # ---------------------------------------------
    # ✅ Start browser
    # ---------------------------------------------
    session = BrowserSession(headless=True, debug=True)
    await session.start()
    page = await session.new_page()

    try:
        # ---------------------------------------------
        # ✅ 1) Launch SAPA (ADVIS)
        # ---------------------------------------------
        await launch_sapa(
            page=page,
            session=session,
            advis=True
        )

        # ---------------------------------------------
        # ✅ 2) Kør søgning
        # ---------------------------------------------
        resultater = await soeg_advis(
            page=page,
            session=session,
            tekst="Arbejdsskadehændelser"
        )

        # ---------------------------------------------
        # ✅ 3) Print resultater
        # ---------------------------------------------
        print("\n📊 RESULTATER:")

        if not resultater:
            print("Ingen resultater fundet")
        else:
            for i, r in enumerate(resultater, start=1):
                print(f"{i}. {r}")

    finally:
        # ---------------------------------------------
        # ✅ Luk browser (robust!)
        # ---------------------------------------------
        await session.close_page(page)


# ---------------------------------------------
# ✅ Kør program
# ---------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())