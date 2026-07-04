# PIB Mumbai Press Release Automation

## Overview

PIB Mumbai Press Release Automation is a Python-based automation project that extracts Marathi press releases published on the Press Information Bureau (PIB) Mumbai website and compiles them into a well-formatted PDF document.

The project automatically navigates the PIB website, extracts every press release for a selected month, stores the extracted data in a checkpoint file, generates an HTML document, and finally converts the HTML into a print-ready PDF.

The application has been designed to handle large volumes of articles while ensuring reliability through automatic retries, checkpoint recovery, and logging.

---

# Features

* Scrapes all PIB Mumbai Marathi press releases for a selected month.
* Automatic extraction of:

  * Ministry Name
  * Press Release Title
  * Publication Date
  * Complete Article Content
* Removes duplicate paragraphs.
* Automatically removes PIB social media/footer information.
* Preserves important bold text from the original article.
* Saves extracted data into JSON checkpoints.
* Resume scraping from the last completed day if interrupted.
* Automatic retry mechanism for temporary network failures.
* Generates clean HTML output.
* Converts HTML into a print-ready PDF using Playwright.
* Generates execution logs.
* Well-structured modular codebase.

---

# Project Structure

```text
PBI_Automation_articles/
│
├── article_worker.py          # Extracts a single article
├── scrape_month.py            # Main scraper
├── generate_pdf.py            # HTML and PDF generation
├── scraper.py                 # Playwright wrapper
├── utils.py                   # Helper functions
├── config.py                  # Configuration
│
├── fonts/
│
├── output/
│   ├── checkpoints/
│   ├── html/
│   └── pdf/
│
├── logs/
│
└── README.md
```

---

# Technologies Used

* Python 3.x
* Playwright
* BeautifulSoup4
* HTML
* CSS
* JSON

---

# Python Libraries

Install the required packages using:

```bash
pip install playwright beautifulsoup4
```

After installing Playwright, install the browser:

```bash
playwright install chromium
```

---

# How It Works

## Step 1 – Select Month

When the program starts, it asks for the month number.

Example:

```text
Enter Month Number : 1
```

---

## Step 2 – Scraping

The scraper:

* Opens the PIB Mumbai Marathi Press Release page.
* Selects the required day, month, and year.
* Collects every PRID available for that date.
* Opens each press release.
* Extracts the required information.
* Saves the day's progress into a checkpoint file.

---

## Step 3 – Checkpoint System

After every day is completed, the scraper stores the extracted data inside:

```text
output/checkpoints/
```

If the program stops unexpectedly, simply run it again.

The scraper resumes automatically from the next incomplete day.

---

## Step 4 – HTML Generation

Once scraping finishes, the program generates a structured HTML document.

The HTML includes:

* Month heading
* Day-wise organization
* Article numbering
* Titles
* Ministry names
* Publication dates
* Paragraph formatting

---

## Step 5 – PDF Generation

The HTML document is rendered using Playwright Chromium.

The PDF includes:

* Proper page margins
* Bold headings
* Justified paragraphs
* Page numbers
* Print-friendly formatting

---

# Output

Generated files are stored inside:

```text
output/
```

Checkpoint:

```text
output/checkpoints/January_2026.json
```

HTML:

```text
output/html/PIB_Mumbai_January_2026.html
```

PDF:

```text
output/pdf/PIB_Mumbai_January_2026.pdf
```

Logs:

```text
logs/January_2026.txt
```

---

# Running the Project

## Step 1

Run the scraper:

```bash
python scrape_month.py
```

After successful completion, a checkpoint JSON file will be created.

---

## Step 2

Generate the PDF:

```bash
python generate_pdf.py
```

This reads the checkpoint file and creates the HTML and PDF.

---

# Reliability Features

The project includes several mechanisms to improve reliability:

* Automatic retry on navigation failures.
* Resume support using checkpoints.
* Duplicate paragraph removal.
* Footer and social media removal.
* Detailed execution logs.
* Structured modular architecture.

---

# Future Improvements

Possible enhancements include:

* Microsoft Word (.docx) export.
* Automatic Table of Contents.
* PDF bookmarks.
* Cover page with official logos.
* Image extraction from press releases.
* Searchable index.
* Command-line arguments for month/year selection.
* Standalone executable using PyInstaller.
* Multi-language support.

---

# Author

**Rushikesh Zanwar**

Bachelor of Technology (B.Tech)

Python Automation Project

---

# License

This project is intended for educational and research purposes.

All press release content belongs to the Press Information Bureau (PIB), Government of India. This project only automates the extraction and compilation of publicly available information and does not claim ownership of the original content.
