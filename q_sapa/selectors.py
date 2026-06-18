class SAPASelectors:

    class Advis:

        INPUT = "//div[@id='s2id_advisgrupper-hidden']//input[contains(@class,'select2-input')]"

        VALUE_TEMPLATE = (
            "//div[@id='s2id_advisgrupper-hidden']"
            "//li[contains(@class,'select2-search-choice')]"
            "//div[normalize-space()='{}']"
        )

        BUTTON = "//button[@id='AdvisSoegningSoegKnap']"
        RESULT = "//span[@id='SoegeresultatTotalResults']"
        ROWS = "//table//tbody/tr"

        CPR = ".//td[contains(@class,'Attr_PartPrettyNummer')]//p"
        NAVN = ".//td[contains(@class,'Attr_PartNavn')]//p"
        HAENDELSE = ".//td[contains(@class,'Attr_HaendelsestypeTitel')]//a"
        DATO = ".//td[@data-value]//p"

        OPEN_BUTTON = ".//button[contains(@class,'set-advis-open-button')]"

        NO_RESULTS = "//h4[contains(normalize-space(),'Ingen adviser')]"

        FAERDIGGOER = "//button[@id='faerdiggoer']"
