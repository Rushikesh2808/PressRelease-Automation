import calendar

# =====================================================
# MONTH / YEAR
# =====================================================

YEAR = "2026"

MONTH_NUM = int(
    input("Enter Month Number : ")
)

MONTHS_EN = {

    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"

}

MONTHS_MR = {

    1: "जानेवारी",
    2: "फेब्रुवारी",
    3: "मार्च",
    4: "एप्रिल",
    5: "मे",
    6: "जून",
    7: "जुलै",
    8: "ऑगस्ट",
    9: "सप्टेंबर",
    10: "ऑक्टोबर",
    11: "नोव्हेंबर",
    12: "डिसेंबर"

}

MONTH_EN = MONTHS_EN[MONTH_NUM]

MONTH_MR = MONTHS_MR[MONTH_NUM]

DAYS_IN_MONTH = calendar.monthrange(

    int(YEAR),

    MONTH_NUM

)[1]

# =====================================================
# PIB URL
# =====================================================

BASE_URL = (

    "https://www.pib.gov.in/"
    "PressReleaseDetail.aspx"
    "?PRID=2210466&reg=1&lang=9"

)

# =====================================================
# FOLDERS
# =====================================================

OUTPUT_FOLDER = "output"

CHECKPOINT_FOLDER = "output/checkpoints"

HTML_FOLDER = "output/html"

PDF_FOLDER = "output/pdf"

LOG_FOLDER = "logs"

FONT_FOLDER = "fonts"

# =====================================================
# OUTPUT FILES
# =====================================================

CHECKPOINT_FILE = (

    f"{CHECKPOINT_FOLDER}/"
    f"{MONTH_EN}_{YEAR}.json"

)

LOG_FILE = (

    f"{LOG_FOLDER}/"
    f"{MONTH_EN}_{YEAR}.txt"

)

OUTPUT_HTML = (

    f"{HTML_FOLDER}/"
    f"PIB_Mumbai_{MONTH_EN}_{YEAR}.html"

)

OUTPUT_PDF = (

    f"{PDF_FOLDER}/"
    f"PIB_Mumbai_{MONTH_EN}_{YEAR}.pdf"

)

# =====================================================
# SCRAPER SETTINGS
# =====================================================

RETRY_COUNT = 3

TIMEOUT = 60000