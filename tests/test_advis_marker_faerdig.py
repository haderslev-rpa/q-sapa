import asyncio
import os

from dotenv import load_dotenv  # bibliotek (pakke → ekstern kode)

from q_haderslev_vbo.playwright.browser_session import BrowserSession
from q_sapa.functionality import launch_sapa, advis_marker_faerdiggjort


async def main():

    # ---------------------------------------------
    # ✅ Load .env (miljøvariabler → konfiguration)
    # ---------------------------------------------
    load_dotenv()

    url_til_advis = os.getenv("SAPA_ADVIS_URL")  # variabel (gemt værdi)

    if not url_til_advis:
        raise ValueError("❌ SAPA_ADVIS_URL mangler i .env")

    # ---------------------------------------------
    # ✅ Start browser
    # ---------------------------------------------
    session = BrowserSession(headless=False, debug=True)
    await session.start()
    page = await session.new_page()

    try:
        # ---------------------------------------------
        # ✅ 1) Launch SAPA (login + klar)
        # ---------------------------------------------
        await launch_sapa(
            page=page,
            session=session,
            advis=True
        )

        # ---------------------------------------------
        # ✅ 2) Gå til advis og færdiggør
        # ---------------------------------------------
        await advis_marker_faerdiggjort(
            page=page,
            session=session,
            url_til_advis=url_til_advis
        )

        print("\n✅ TEST OK - advis færdiggjort")

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
