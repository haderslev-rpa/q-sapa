from q_sapa.selectors import SAPASelectors
from q_sapa.utils import parse_advis_row


async def soeg_advis(page, session, tekst: str, timeout: int = 15000) -> list:

    print("🔎 Navigerer til søgesiden...")

    SOEG_URL = "https://sapaadvis.dk/Soege?clearSessionState=True&restoreResults=True"
    await page.goto(SOEG_URL)
    await page.wait_for_load_state("networkidle")

    # ---------------------------------------------
    # ✅ Select2
    # ---------------------------------------------
    input_felt = page.locator(SAPASelectors.Advis.INPUT).first

    await input_felt.wait_for(state="visible", timeout=timeout)
    await input_felt.click()
    await input_felt.fill(tekst)

    await page.wait_for_timeout(500)

    dropdown_option = page.locator(
        "//li[contains(@class,'select2-result-selectable')]"
    ).first

    await dropdown_option.wait_for(state="visible", timeout=timeout)

    await input_felt.press("ArrowDown")
    await input_felt.press("Enter")

    await session.screenshot(page, "STEP_advis_valgt")

    # ---------------------------------------------
    # ✅ Søg
    # ---------------------------------------------
    soeg_knap = page.locator(SAPASelectors.Advis.BUTTON)
    await soeg_knap.click()

    # ---------------------------------------------
    # ✅ WAIT på SAPA tabel (NY VERSION)
    # ---------------------------------------------
    await page.wait_for_function("""
        () => {
            const table = document.querySelector('#AdvisTable');
            if (!table) return false;

            const spinner = document.querySelector('.dataTables_processing');
            if (spinner) {
                const style = window.getComputedStyle(spinner);
                if (style.display !== 'none') return false;
            }

            const rows = table.querySelectorAll('tbody tr');
            if (rows.length === 0) return false;

            for (const row of rows) {
                if (row.innerText && row.innerText.trim().length > 20) {
                    return true;
                }
            }

            return false;
        }
    """)

    await session.screenshot(page, "STEP_soeg_klikket")

    # ---------------------------------------------
    # ✅ Ingen resultater
    # ---------------------------------------------
    if await page.locator(SAPASelectors.Advis.NO_RESULTS).count() > 0:
        print("✅ Ingen adviser")
        return []

    # ---------------------------------------------
    # ✅ Parse tabel (NY – korrekt selector)
    # ---------------------------------------------
    rows = page.locator(SAPASelectors.Advis.ROWS)
    count = await rows.count()

    print(f"✅ Antal rækker fundet: {count}")

    resultater = []

    for i in range(count):
        row = rows.nth(i)

        data = await parse_advis_row(row)

        if data:
            resultater.append(data)

    print(f"✅ Udtrukket {len(resultater)} resultater")

    return resultater
