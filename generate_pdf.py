from scraper import PIBScraper

import json
import time
import os

from scraper import PIBScraper

import json
import time
import os

from config import (
    CHECKPOINT_FILE,
    OUTPUT_HTML,
    OUTPUT_PDF,
    MONTH_EN,
    YEAR
)

# =====================================================
# LOAD CHECKPOINT
# =====================================================

with open(
    CHECKPOINT_FILE,
    "r",
    encoding="utf-8"
) as f:

    monthly_data = json.load(f)

print(
    f"Loaded {len(monthly_data)} Days"
)

html_output = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<style>

body{{
    font-family:'Noto Serif Devanagari',serif;
    margin:25mm 18mm;
    line-height:1.8;
    font-size:14pt;
}}

.day{{
    font-size:20pt;
    font-weight:bold;
    text-align:center;
    margin-bottom:30px;
}}

.article-number{{
    font-size:18pt;
    font-weight:bold;
    margin-top:25px;
    margin-bottom:10px;
}}

.title{{
    font-size:18pt;
    font-weight:700;
    line-height:1.4;
    margin-bottom:12px;
}}

.ministry{{
    font-size:16pt;
    font-weight:bold;
    text-decoration:underline;
    margin-bottom:8px;
}}

.publish-date{{
    font-size:13pt;
    margin-bottom:20px;
}}

p{{
    font-size:14pt;
    text-align:justify;
    margin-top:0;
    margin-bottom:12px;
    line-height:1.9;
}}

b{{
    font-weight:bold;
}}

.month-title{{
    text-align:center;
    font-size:26pt;
    font-weight:bold;
    margin-bottom:40px;
    border-bottom:2px solid #000;
    padding-bottom:14px;
}}

</style>

</head>

<body>

<div class="month-title">

PIB Mumbai Press Releases

<br>

{MONTH_EN} {YEAR}

</div>
"""

# =====================================================
# BUILD HTML
# =====================================================

for day_index, day_data in enumerate(monthly_data):
    
    if day_index != 0:

        html_output += """
        <div style="page-break-before:always;"></div>
        """
    
    day = day_data["day"]
    articles = day_data["articles"]

    day_heading = (
        f"{day} "
        f"{MONTH_EN} "
        f"{YEAR}"
    )

    html_output += f"""
    <div class="day">
    {day_heading}
    </div>
    """

    article_no = 1

    for article in articles:

        html_output += f"""

        <div class="article-number">

            Article {article_no}

        </div>

        <div class="title">

            {article['title']}

        </div>

        <div class="ministry">

            {article['ministry']}

        </div>

        <div class="publish-date">

            {article['date']}

        </div>

        """

        for para in article["paragraphs"]:

            html_output += para

        html_output += """

        <div style="height:20px;"></div>

        <hr style="
            margin-top:0;
            margin-bottom:25px;
            border:none;
            border-top:1px solid #999;
        ">

        <div style="height:20px;"></div>

        """

        article_no += 1
    
html_output += """

</body>

</html>

"""

# =====================================================
# SAVE HTML
# =====================================================

os.makedirs(
    os.path.dirname(OUTPUT_HTML),
    exist_ok=True
)

with open(
    OUTPUT_HTML,
    "w",
    encoding="utf-8"
) as f:

    f.write(html_output)

print(
    "\nHTML Generated Successfully."
)

# =====================================================
# GENERATE PDF
# =====================================================

print("\nGenerating PDF...")

scraper = PIBScraper()

html_path = (
    "file:///" +
    os.path.abspath(
        OUTPUT_HTML
    ).replace(
        "\\",
        "/"
    )
)

scraper.page.goto(
    html_path,
    wait_until="load"
)

time.sleep(2)

os.makedirs(
    os.path.dirname(OUTPUT_PDF),
    exist_ok=True
)

scraper.page.pdf(

    path=OUTPUT_PDF,

    format="A4",

    print_background=True,

    margin={

        "top": "20mm",

        "bottom": "20mm",

        "left": "18mm",

        "right": "18mm"

    },

    display_header_footer=True,

    header_template="""

    <div></div>

    """,

    footer_template="""

    <div style="
        width:100%;
        font-size:9px;
        color:#666;
        text-align:center;
        padding:0 20px;
    ">

        Page <span class="pageNumber"></span>
        of
        <span class="totalPages"></span>

    </div>

    """

)

scraper.close()

print("\nPDF Generated Successfully.")

print(OUTPUT_PDF)
