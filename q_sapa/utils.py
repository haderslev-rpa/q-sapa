async def parse_advis_row(row):
    try:
        cpr = await row.locator("xpath=.//td[contains(@class,'Attr_PartPrettyNummer')]//p").inner_text()
        navn = await row.locator("xpath=.//td[contains(@class,'Attr_PartNavn')]//p").inner_text()
        haendelse = await row.locator("xpath=.//td[contains(@class,'Attr_HaendelsestypeTitel')]//a").inner_text()
        dato = await row.locator("xpath=.//td[@data-value]//p").inner_text()

        onclick = await row.locator(
            "xpath=.//button[contains(@class,'set-advis-open-button')]"
        ).get_attribute("onclick")

        url = None
        if onclick:
            try:
                relative_url = onclick.split("'")[1]
                url = f"https://sapaadvis.dk{relative_url}"
            except Exception:
                pass

        return {
            "cpr": cpr.strip(),
            "navn": navn.strip(),
            "haendelse": haendelse.strip(),
            "dato": dato.strip(),
            "url_til_advis": url
        }

    except Exception:
        return None