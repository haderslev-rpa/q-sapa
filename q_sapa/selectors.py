class SAPASelectors:

    class Login:
        MUNICIPALITY_SELECT = "#SelectedAuthenticationUrl"
        OK_BUTTON = "#btnOK"

    


    class Frontpage_advis:
        FAELLESSOEGER_TABLE = "#DelteSoegningerTabel"




    class Advis:

        # ---------------------------------------------
        # ✅ Select2 (behold XPath – nødvendig her)
        # ---------------------------------------------
        INPUT = "//div[@id='s2id_advisgrupper-hidden']//input[contains(@class,'select2-input')]"

        VALUE_TEMPLATE = (
            "//div[@id='s2id_advisgrupper-hidden']"
            "//li[contains(@class,'select2-search-choice')]"
            "//div[normalize-space()='{}']"
        )

        # ---------------------------------------------
        # ✅ Søg
        # ---------------------------------------------
        BUTTON = "#AdvisSoegningSoegKnap"
        RESULT = "#SoegeresultatTotalResults"

        # ---------------------------------------------
        # ✅ NY: Stabil tabel selector (KRITISK FIX)
        # ---------------------------------------------
        TABLE = "#AdvisTable"
        ROWS = "#AdvisTable tbody tr"

        # ---------------------------------------------
        # ✅ NY: Kolonne selectors (100% stabile)
        # matcher din HTML
        # ---------------------------------------------
        CPR = "td.Attr_PartPrettyNummer p.part-dialogintegration"
        NAVN = "td.Attr_PartNavn p.part-dialogintegration"
        HAENDELSE = "td.Attr_HaendelsestypeTitel a"
        DATO = "td[data-value] p"

        # ---------------------------------------------
        # ✅ Handlinger
        # ---------------------------------------------
        OPEN_BUTTON = "button.set-advis-open-button"

        # ---------------------------------------------
        # ✅ Ingen resultater
        # ---------------------------------------------
        NO_RESULTS = "//h4[contains(normalize-space(),'Ingen adviser')]"

        # ---------------------------------------------
        # ✅ Færdiggør (behold)
        # ---------------------------------------------
        FAERDIGGOER = "#faerdiggoer"
