from article_worker import extract_article
from scraper import PIBScraper

import datetime
import time

from config import *

from utils import (
    clean_text,
    extract_prids,
    save_checkpoint,
    load_checkpoint,
    retry_goto,
    wait_for_search_results_update,
    write_log,
    create_folders,
    format_runtime
)

# =====================================================
# INITIALIZATION
# =====================================================

create_folders()

start_time = time.time()

print(
    "\nRun Started :",
    datetime.datetime.now()
)

write_log(
    LOG_FILE,
    "Scraping Started"
)

# =====================================================
# LOAD CHECKPOINT
# =====================================================

monthly_data = load_checkpoint(
    CHECKPOINT_FILE
)

completed_days = len(
    monthly_data
)

if completed_days:

    print(
        f"\nCheckpoint Found"
    )

    print(
        f"Completed Days : {completed_days}"
    )

    print(
        f"Resuming From Day : {completed_days + 1}"
    )

    write_log(
        LOG_FILE,
        f"Resuming From Day {completed_days + 1}"
    )

else:

    print(
        "\nNo Checkpoint Found"
    )

    write_log(
        LOG_FILE,
        "Fresh Run Started"
    )

# =====================================================
# OPEN PIB
# =====================================================

scraper = PIBScraper()

retry_goto(
    scraper,
    BASE_URL
)

# =====================================================
# START SCRAPING
# =====================================================

for day in range(

    completed_days + 1,

    DAYS_IN_MONTH + 1

):

    print(
        "\n" + "=" * 60
    )

    print(
        f"DAY : {day}"
    )

    print(
        "=" * 60
    )

    write_log(
        LOG_FILE,
        f"Processing Day {day}"
    )

    # ------------------------------------
    # OPEN SEARCH PAGE
    # ------------------------------------

    retry_goto(
        scraper,
        BASE_URL
    )

    scraper.page.select_option(
        "#ContentPlaceHolder1_ddlday",
        label=str(day)
    )

    wait_for_search_results_update(scraper)

    scraper.page.select_option(
        "#ContentPlaceHolder1_ddlMonth",
        label=MONTH_MR
    )

    wait_for_search_results_update(scraper)

    scraper.page.select_option(
        "#ContentPlaceHolder1_ddlYear",
        label=YEAR
    )

    wait_for_search_results_update(scraper)
    
    attempt = 1

    while True:

        html = scraper.page.content()

        prids = extract_prids(html)

        print(f"Attempt {attempt} : {len(prids)} articles")
        scraper.page.wait_for_timeout(500)

        if len(prids) > 0:
            break

        if attempt == 3:
            break

        print("Reloading search...")

        retry_goto(
            scraper,
            BASE_URL
        )
        
        scraper.page.wait_for_selector(
            "#ContentPlaceHolder1_ddlday"
        )

        scraper.page.select_option(
            "#ContentPlaceHolder1_ddlday",
            label=str(day)
        )

        wait_for_search_results_update(scraper)

        scraper.page.select_option(
            "#ContentPlaceHolder1_ddlMonth",
            label=MONTH_MR
        )

        wait_for_search_results_update(scraper)

        scraper.page.select_option(
            "#ContentPlaceHolder1_ddlYear",
            label=YEAR
        )

        wait_for_search_results_update(scraper)

        attempt += 1


    print(
        f"\nArticles Found : {len(prids)}"
    )

    write_log(
        LOG_FILE,
        f"Articles Found : {len(prids)}"
    )

    day_articles = []
    # =====================================================
    # ARTICLE LOOP
    # =====================================================

    for article_no, prid in enumerate(

        prids,

        start=1

    ):

        print(

            f"\n[{article_no}/{len(prids)}]"

        )

        article_url = (

            "https://www.pib.gov.in/"
            f"PressReleasePage.aspx?PRID={prid}"

        )

        print(article_url)

        try:

            article = extract_article(

                scraper,

                article_url,

                article_no,

                prid

            )

            day_articles.append(article)

            print("✓ Extracted")

            write_log(

                LOG_FILE,

                f"PRID {prid} Extracted"

            )

        except Exception as e:

            print(

                "Error :",

                e

            )

            write_log(

                LOG_FILE,

                f"PRID {prid} Failed : {e}"

            )
        
    # =====================================================
    # SAVE ONE DAY
    # =====================================================
    print(f"Saving Day -> {day}")
    
    monthly_data.append(

        {

            "day": day,

            "articles": day_articles

        }

    )

    save_checkpoint(

        monthly_data,

        CHECKPOINT_FILE

    )

    print(

        f"\nDay {day} Saved."

    )

    print(

        f"Articles : {len(day_articles)}"

    )

    write_log(

        LOG_FILE,

        f"Day {day} Saved ({len(day_articles)} Articles)"

    )
    
    
# =====================================================
# SCRAPING COMPLETED
# =====================================================

scraper.close()

end_time = time.time()

total_time = end_time - start_time

total_articles = sum(

    len(day["articles"])

    for day in monthly_data

)

print(
    "\n" + "=" * 70
)

print(
    "MONTH SCRAPING COMPLETED"
)

print(
    "=" * 70
)

print(
    f"\nMonth : {MONTH_EN} {YEAR}"
)

print(
    f"Days Processed : {len(monthly_data)}"
)

print(
    f"Total Articles : {total_articles}"
)

print(
    f"Checkpoint File :"
)

print(
    CHECKPOINT_FILE
)

print(
    f"\nTotal Runtime : {format_runtime(total_time)}"
)

print(
    "\nScraping Completed Successfully."
)

print(
    "=" * 70
)

# =====================================================
# LOG SUMMARY
# =====================================================

write_log(

    LOG_FILE,

    "=" * 60

)

write_log(

    LOG_FILE,

    "SCRAPING COMPLETED"

)

write_log(

    LOG_FILE,

    f"Month : {MONTH_EN}"

)

write_log(

    LOG_FILE,

    f"Year : {YEAR}"

)

write_log(

    LOG_FILE,

    f"Days : {len(monthly_data)}"

)

write_log(

    LOG_FILE,

    f"Articles : {total_articles}"

)

write_log(

    LOG_FILE,

    f"Runtime : {format_runtime(total_time)}"

)

write_log(

    LOG_FILE,

    "=" * 60

)

print("\n" + "=" * 70)

print("NEXT STEP")

print("=" * 70)

print(
    "\nScraping has completed successfully."
)

print(
    "\nTo generate the PDF, run:"
)

print(
    "\n    python generate_pdf.py"
)

print(
    f"\nThe PDF will be saved to:\n{OUTPUT_PDF}"
)

print(
    "\nThe HTML file will be saved to:"
)

print(
    f"{OUTPUT_HTML}"
)

print(
    "\n" + "=" * 70
)

input(
    "\nPress Enter to Exit..."
)