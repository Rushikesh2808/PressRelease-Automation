import json
import os
import re
import time
import datetime
from bs4 import BeautifulSoup
from config import RETRY_COUNT, TIMEOUT


# =====================================================
# TEXT HELPERS
# =====================================================

def clean_text(text):

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip()

def remove_footer(paragraphs):

    stop_patterns = [

        "इथे क्लिक करा",
        "सोशल मीडियावर",
        "@PIBMumbai",
        "/PIBMumbai",
        "PIBMumbai",
        "Facebook",
        "Twitter",
        "Instagram",
        "YouTube",
        "WhatsApp Channel",
        "Jaydevi",
        "Pujari",
        "Swami",
        "Tushar",
        "Pawar",
        "Uma",
        "Raikar"

    ]

    cleaned = []

    for para in paragraphs:

        text = BeautifulSoup(
            para,
            "html.parser"
        ).get_text(
            " ",
            strip=True
        )

        stop = False

        for pattern in stop_patterns:

            if pattern.lower() in text.lower():

                stop = True
                break

        if stop:
            break

        cleaned.append(para)

    return cleaned

def extract_prids(html):

    return sorted(
        set(
            re.findall(
                r"Bind_PressReleaseDetails\((\d+)\)",
                html
            )
        ),
        reverse=True
    )


# =====================================================
# CHECKPOINT FUNCTIONS
# =====================================================

def save_checkpoint(
    monthly_data,
    checkpoint_file
):

    os.makedirs(
        os.path.dirname(checkpoint_file),
        exist_ok=True
    )

    with open(
        checkpoint_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            monthly_data,
            f,
            ensure_ascii=False,
            indent=4
        )


def load_checkpoint(checkpoint_file):

    if not os.path.exists(checkpoint_file):
        return []

    try:

        with open(
            checkpoint_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:

        return []


# =====================================================
# LOGGING
# =====================================================

def write_log(
    log_file,
    message
):

    os.makedirs(
        os.path.dirname(log_file),
        exist_ok=True
    )

    timestamp = datetime.datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    with open(
        log_file,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"[{timestamp}] {message}\n"
        )


# =====================================================
# INTERNET RETRY
# =====================================================

# def retry_goto(

#     scraper,

#     url,

#     wait_seconds=10

# ):

#     attempts = 0

#     while attempts < RETRY_COUNT:

#         try:

#             scraper.goto(url)

#             return

#         except Exception as e:

#             attempts += 1

#             print()

#             print("Connection Error")

#             print(e)

#             print()

#             print(
#                 f"Retry {attempts}/{RETRY_COUNT}"
#             )

#             time.sleep(wait_seconds)

#     raise Exception(
#         "Maximum retries exceeded."
#     )
    
def retry_goto(scraper, url, wait_seconds=10):

    attempts = 0

    while attempts < RETRY_COUNT:

        try:

            print(f"Navigating to: {url}")

            scraper.goto(url)

            print("Navigation successful")

            return

        except Exception as e:

            attempts += 1

            print(f"Navigation failed ({attempts}/{RETRY_COUNT})")
            print(e)

            # Reset the page
            try:
                scraper.page.close()
            except:
                pass

            scraper.page = scraper.browser.new_page()
            scraper.page.set_default_timeout(TIMEOUT)

            time.sleep(wait_seconds)

    raise Exception("Maximum retries exceeded.")

    
def wait_for_search_results_update(scraper):

    previous_count = -1

    stable = 0

    while stable < 3:

        html = scraper.page.content()

        count = len(
            extract_prids(html)
        )

        if count == previous_count:

            stable += 1

        else:

            stable = 0

        previous_count = count

        scraper.page.wait_for_timeout(300)

    return previous_count


# =====================================================
# OUTPUT FOLDERS
# =====================================================

def create_folders():

    folders = [

        "output",

        "output/checkpoints",

        "output/html",

        "output/pdf",

        "logs"

    ]

    for folder in folders:

        os.makedirs(
            folder,
            exist_ok=True
        )


# =====================================================
# TIME FORMAT
# =====================================================

def format_runtime(seconds):

    hrs = int(seconds // 3600)

    mins = int(
        (seconds % 3600) // 60
    )

    secs = int(
        seconds % 60
    )

    return (
        f"{hrs}h "
        f"{mins}m "
        f"{secs}s"
    )