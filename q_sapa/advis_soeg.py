# ==================================================
# ✅ XPATHS
# ==================================================
INPUT_XPATH = "//div[@id='s2id_advisgrupper-hidden']//input[contains(@class,'select2-input')]"

VALUE_XPATH_TEMPLATE = (
    "//div[@id='s2id_advisgrupper-hidden']"
    "//li[contains(@class,'select2-search-choice')]"
    "//div[normalize-space()='{}']"
)

BUTTON_XPATH = "//button[@id='AdvisSoegningSoegKnap']"
RESULT_XPATH = "//span[@id='SoegeresultatTotalResults']"

ROWS_XPATH = "//table//tbody/tr"

CPR_XPATH = ".//td[contains(@class,'Attr_PartPrettyNummer')]//p[contains(@class,'part-dialogintegration')]"
NAVN_XPATH = ".//td[contains(@class,'Attr_PartNavn')]//p[contains(@class,'part-dialogintegration')]"
HAENDELSE_XPATH = ".//td[contains(@class,'Attr_HaendelsestypeTitel')]//a"
DATO_XPATH = ".//td[@data-value]//p"

ADVIS_BUTTON_XPATH = ".//button[contains(@class,'set-advis-open-button')]"

NO_RESULTS_XPATH = "//h4[contains(normalize-space(),'Ingen adviser')]"


# ==================================================
# ✅ FUNKTION
# ==================================================
async def soeg_advis(page, session, tekst: str, timeout: int = 15000) -> list:

    # ---------------------------------------------
    # ✅ 1) Gå til søgeside
    # ---------------------------------------------
    print("🔎 Navigerer til søgesiden...")

    SOEG_URL = "https://sapaadvis.dk/Soege?clearSessionState=True&restoreResults=True"
    await page.goto(SOEG_URL)

    print(f"🌐 URL efter goto: {page.url}")

    await page.wait_for_load_state("networkidle")

    # ---------------------------------------------
    # ✅ 2) Vælg advisgruppe
    # ---------------------------------------------
    print(f"🔍 Vælger advisgruppe: {tekst}")

    input_felt = page.locator(f"xpath={INPUT_XPATH}").first
    await input_felt.wait_for(state="visible", timeout=timeout)

    await input_felt.click()
    await input_felt.fill(tekst)

    await page.wait_for_timeout(600)

    await input_felt.press("ArrowDown")
    await page.wait_for_timeout(600)
    await input_felt.press("Enter")

    value_xpath = VALUE_XPATH_TEMPLATE.format(tekst)
    valgt = page.locator(f"xpath={value_xpath}").first
    await valgt.wait_for(state="visible", timeout=timeout)

    await session.recorder.screenshot(page, "STEP_advis_valgt")

    # ---------------------------------------------
    # ✅ 3) Klik søg
    # ---------------------------------------------
    print("🔍 Klikker 'Søg'...")

    soeg_knap = page.locator(f"xpath={BUTTON_XPATH}")
    await soeg_knap.wait_for(state="visible", timeout=timeout)
    await soeg_knap.click()

    await page.wait_for_timeout(500)

    # ✅ WAIT på DOM (robust SAPA fix)
    await page.wait_for_function(
        """
        () => {
            const result = document.querySelector('#SoegeresultatTotalResults');
            const hasResults = result && result.innerText.trim() !== '';

            const noResults = Array.from(document.querySelectorAll('h4'))
                .some(el => el.innerText.includes('Ingen adviser'));

            const rows = document.querySelectorAll('table tbody tr').length > 0;

            return hasResults || noResults || rows;
        }
        """
    )

    await page.wait_for_timeout(300)

    await session.recorder.screenshot(page, "STEP_soeg_klikket")

    # ---------------------------------------------
    # ✅ 4) Tjek "Ingen adviser"
    # ---------------------------------------------
    no_results = page.locator(f"xpath={NO_RESULTS_XPATH}")

    if await no_results.count() > 0:
        print("✅ Ingen adviser blev fundet")
        return []

    # ---------------------------------------------
    # ✅ 5) Læs antal resultater
    # ---------------------------------------------
    result_el = page.locator(f"xpath={RESULT_XPATH}")
    await result_el.wait_for(state="visible", timeout=timeout)

    antal_text = (await result_el.inner_text()).strip()

    if not antal_text:
        antal = 0
    else:
        antal = int(antal_text.replace("(", "").replace(")", ""))

    print(f"✅ Søgeresultater: {antal}")

    if antal == 0:
        return []

    # ---------------------------------------------
    # ✅ 6) Læs rækker
    # ---------------------------------------------
    rows = page.locator(f"xpath={ROWS_XPATH}")
    total_rows = await rows.count()

    max_rows = min(antal, total_rows)

    resultater = []

    for i in range(max_rows):
        row = rows.nth(i)

        try:
            cpr = await row.locator(f"xpath={CPR_XPATH}").inner_text()
            navn = await row.locator(f"xpath={NAVN_XPATH}").inner_text()
            haendelse = await row.locator(f"xpath={HAENDELSE_XPATH}").inner_text()
            dato = await row.locator(f"xpath={DATO_XPATH}").inner_text()

            onclick = await row.locator(f"xpath={ADVIS_BUTTON_XPATH}").get_attribute("onclick")

            url = None
            if onclick:
                try:
                    relative_url = onclick.split("'")[1]
                    url = f"https://sapaadvis.dk{relative_url}"
                except Exception:
                    url = None

        except Exception:
            continue

        resultater.append({
            "cpr": cpr.strip(),
            "navn": navn.strip(),
            "haendelse": haendelse.strip(),
            "dato": dato.strip(),
            "url_til_advis": url
        })

    print("✅ Flow færdig")

    return resultater