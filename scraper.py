from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from config import TIMEOUT


class PIBScraper:

    def __init__(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(

            headless=False,

            slow_mo=20

        )

        self.page = self.browser.new_page()

        self.page.set_default_timeout(

            TIMEOUT

        )

    # =====================================================
    # NAVIGATION
    # =====================================================

    def open(self, url="https://www.pib.gov.in"):

        self.goto(url)

    def goto(self, url):

        self.page.goto(

            url,

            wait_until="load",

            timeout=TIMEOUT

        )

    # =====================================================
    # HELPERS
    # =====================================================

    def wait_for_title(self):

        self.page.wait_for_selector(

            "#Titleh2"

        )

    def html(self):

        return self.page.content()

    def soup(self):

        return BeautifulSoup(

            self.page.content(),

            "html.parser"

        )

    def title(self):

        return self.page.title()

    # =====================================================
    # FORM HELPERS
    # =====================================================

    def click(self, selector):

        self.page.click(selector)

    def fill(self, selector, value):

        self.page.fill(selector, value)

    def select(self, selector, value):

        self.page.select_option(

            selector,

            label=value

        )

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        try:

            self.browser.close()

        except:

            pass

        try:

            self.playwright.stop()

        except:

            pass