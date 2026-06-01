from playwright.async_api import Page
from q_haderslev_vbo.playwright.playwright_debughelper import PlaywrightDebugHelper


# ==================================================
# ✅ NAVIGATION TIL SØGESIDE
# ==================================================
async def go_to_soeg(
    page: Page,
    debug: bool = False
) -> None:

    dbg = PlaywrightDebugHelper(debug=debug)

    SOEG_URL = "https://sapaadvis.dk/Soege?clearSessionState=True&restoreResults=True"

    print("🔎 Navigerer til søgesiden...")

    await page.goto(SOEG_URL)
    await page.wait_for_load_state("networkidle")

    if debug:
        await dbg.screenshot(page, "STEP_soeg_side")

    print("✅ Søgeside klar:", page.url)


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


# ==================================================
# ✅ VÆLG ADVISGRUPPE + SØG
# ==================================================
async def vaelg_advisgruppe(
    page: Page,
    tekst: str,
    timeout: int = 15000,
    debug: bool = False
) -> None:

    dbg = PlaywrightDebugHelper(debug=debug)

    try:
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

        print(f"✅ Valgt korrekt: {tekst}")

        if debug:
            await dbg.screenshot(page, "STEP_advis_valgt")

        print("🔍 Klikker på Søg...")

        soeg_knap = page.locator(f"xpath={BUTTON_XPATH}")
        await soeg_knap.wait_for(state="visible", timeout=timeout)

        await soeg_knap.click()

        if debug:
            await dbg.screenshot(page, "STEP_soeg_klikket")

        print("⏳ Venter på søgeresultater...")

        result = page.locator(f"xpath={RESULT_XPATH}")
        await result.wait_for(state="visible", timeout=timeout)

        antal = await result.inner_text()
        print(f"✅ Søgeresultater loaded: {antal}")

        if debug:
            await dbg.screenshot(page, "STEP_resultater_loaded")

    except Exception:
        if debug:
            await dbg.screenshot(page, "FEJL_soeg_flow")
        raise


# ==================================================
# ✅ HENT SØGERESULTATER (uden print af data)
# ==================================================
async def hent_soegeresultater(
    page: Page,
    timeout: int = 15000,
    debug: bool = False
) -> list:

    dbg = PlaywrightDebugHelper(debug=debug)

    print("📊 Henter søgeresultater...")

    # ✅ 1) UI antal
    result_el = page.locator(f"xpath={RESULT_XPATH}")
    await result_el.wait_for(state="visible", timeout=timeout)

    antal_text = await result_el.inner_text()
    antal = int(antal_text.replace("(", "").replace(")", "").strip())

    print(f"✅ Antal ifølge UI: {antal}")

    if antal == 0:
        print("⚠️ Ingen resultater")
        return []

    # ✅ 2) DOM rækker
    rows = page.locator(f"xpath={ROWS_XPATH}")
    total_rows = await rows.count()

    max_rows = min(antal, total_rows)

    print(f"✅ Behandler rækker: {max_rows}")

    resultater = []

    # ✅ 3) Loop (uden print)
    for i in range(max_rows):
        row = rows.nth(i)

        try:
            cpr = await row.locator(f"xpath={CPR_XPATH}").inner_text()
            navn = await row.locator(f"xpath={NAVN_XPATH}").inner_text()
            haendelse = await row.locator(f"xpath={HAENDELSE_XPATH}").inner_text()
            dato = await row.locator(f"xpath={DATO_XPATH}").inner_text()
        except Exception:
            continue

        data = {
            "cpr": cpr.strip(),
            "navn": navn.strip(),
            "haendelse": haendelse.strip(),
            "dato": dato.strip()
        }

        resultater.append(data)

    if debug:
        await dbg.screenshot(page, "STEP_resultater_udtraekket")

    print("✅ Udtræk færdig")

    return resultater
