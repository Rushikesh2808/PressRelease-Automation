from bs4 import BeautifulSoup

from utils import (
    clean_text,
    remove_footer,
    retry_goto
)


def extract_article(scraper, article_url, article_no, prid):

    # =====================================================
    # OPEN ARTICLE
    # =====================================================

    print(f"\nOpening PRID : {prid}")

    print("1")
    retry_goto(
        scraper,
        article_url
    )

    print("2")
    scraper.page.wait_for_selector(
        "#Titleh2"
    )

    print("3")
    scraper.page.wait_for_timeout(300)

    print("4")
    html = scraper.page.content()

    print("5")
    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # =====================================================
    # HEADER
    # =====================================================

    ministry = ""
    title = ""
    date = ""

    m = soup.find(id="MinistryName")

    if m:

        ministry = clean_text(
            m.get_text(
                " ",
                strip=True
            )
        )

    t = soup.find(id="Titleh2")

    if t:

        title = clean_text(
            t.get_text(
                " ",
                strip=True
            )
        )

    d = soup.find(id="PrDateTime")

    if d:

        date = clean_text(
            d.get_text(
                " ",
                strip=True
            )
        )

    if not title:

        title = "Untitled Press Release"

    if not ministry:

        ministry = "Ministry Not Specified"

    # =====================================================
    # CONTENT
    # =====================================================

    paragraphs = []

    seen = set()

    main_content = soup.find(

        "div",

        class_="innner-page-main-about-us-content-right-part"

    )

    if main_content:

        for p in main_content.find_all("p"):

            txt = clean_text(

                p.get_text(
                    " ",
                    strip=True
                )

            )

            if len(txt) < 10:

                continue

            if txt in seen:

                continue

            seen.add(txt)

            p_copy = BeautifulSoup(

                str(p),

                "html.parser"

            )

            # Preserve bold text

            for tag in p_copy.find_all("strong"):

                tag.name = "b"

            # Remove span tags

            for tag in p_copy.find_all("span"):

                tag.unwrap()

            # Remove unsupported attributes

            for tag in p_copy.find_all():

                tag.attrs = {}

            html_para = "".join(

                str(x)

                for x in p_copy.contents

            )

            paragraphs.append(
                html_para
            )

    # Remove PIB footer

    paragraphs = remove_footer(
        paragraphs
    )

    # =====================================================
    # RETURN
    # =====================================================

    return {

        "article_no": article_no,

        "prid": prid,

        "title": title,

        "ministry": ministry,

        "date": date,

        "paragraphs": paragraphs

    }