from playwright.async_api import Page
from q_sapa.selectors import SAPASelectors


# ---------------------------------------------
# ✅ Parse én række (REN / KY-style)
# ---------------------------------------------
async def parse_advis_row(row):

    try:
        cpr = await row.locator(SAPASelectors.Advis.CPR).first.inner_text()
        navn = await row.locator(SAPASelectors.Advis.NAVN).first.inner_text()
        haendelse = await row.locator(SAPASelectors.Advis.HAENDELSE).first.inner_text()
        dato = await row.locator(SAPASelectors.Advis.DATO).first.inner_text()

        btn = row.locator(SAPASelectors.Advis.OPEN_BUTTON).first
        onclick = await btn.get_attribute("onclick")

        url = None
        if onclick and "AdvisDetails" in onclick:
            try:
                relative = onclick.split("'")[1]
                url = f"https://sapaadvis.dk{relative}"
            except Exception:
                pass

        return {
            "cpr": cpr.strip(),
            "navn": navn.strip(),
            "haendelse": haendelse.strip(),
            "dato": dato.strip(),
            "url_til_advis": url,
        }

    except Exception:
        return None


# ---------------------------------------------
# ✅ Extract tabel (KY-style light version)
# ---------------------------------------------
async def extract_sapa_table(page: Page) -> list[dict]:

    # ✅ Vent på tabel er klar
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