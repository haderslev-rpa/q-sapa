from q_sapa.selectors import SAPASelectors
from q_sapa.utils import parse_advis_row


async def soeg_advis(page, session, tekst: str, timeout: int = 15000) -> list:

    print("🔎 Navigerer til søgesiden...")

    SOEG_URL = "https://sapaadvis.dk/Soege?clearSessionState=True&restoreResults=True"
    await page.goto(SOEG_URL)
    await page.wait_for_load_state("networkidle")

    # ✅ vælg advisgruppe
    input_felt = page.locator(f"xpath={SAPASelectors.Advis.INPUT}").first

    await input_felt.wait_for(state="visible", timeout=timeout)
    await input_felt.click()
    await input_felt.fill(tekst)

    await page.wait_for_timeout(600)
    await input_felt.press("ArrowDown")
    await page.wait_for_timeout(600)
    await input_felt.press("Enter")

    value_xpath = SAPASelectors.Advis.VALUE_TEMPLATE.format(tekst)
    await page.locator(f"xpath={value_xpath}").wait_for()

    await session.screenshot(page, "STEP_advis_valgt")

    # ✅ søg
    soeg_knap = page.locator(f"xpath={SAPASelectors.Advis.BUTTON}")
    await soeg_knap.wait_for(state="visible", timeout=timeout)
    await soeg_knap.click()

    await page.wait_for_function("""
        () => {
            const result = document.querySelector('#SoegeresultatTotalResults');
            const hasResults = result && result.innerText.trim() !== '';

            const noResults = Array.from(document.querySelectorAll('h4'))
                .some(el => el.innerText.includes('Ingen adviser'));

            const rows = document.querySelectorAll('table tbody tr').length > 0;

            return hasResults || noResults || rows;
        }
    """)

    await session.screenshot(page, "STEP_soeg_klikket")

    # ✅ ingen resultater
    if await page.locator(f"xpath={SAPASelectors.Advis.NO_RESULTS}").count() > 0:
        print("✅ Ingen adviser")
        return []

    # ✅ parse rækker
    rows = page.locator(f"xpath={SAPASelectors.Advis.ROWS}")
    count = await rows.count()

    resultater = []

    for i in range(count):
        row = rows.nth(i)
        data = await parse_advis_row(row)

        if data:
            resultater.append(data)

    return resultater
