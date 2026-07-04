# PressRelease-Automation

A Python automation project that scrapes Marathi press releases published by the Press Information Bureau (PIB) Mumbai, organizes them month-wise, and generates clean HTML and print-ready PDF archives.

---

## Features

- Scrapes all Marathi press releases for a selected month.
- Automatically extracts:
  - Ministry Name
  - Press Release Title
  - Publication Date
  - Complete Article Content
- Removes duplicate paragraphs.
- Cleans footer, navigation, and social media sections.
- Preserves important formatting such as bold text.
- Stores extracted data as JSON checkpoints.
- Resumes automatically if the process is interrupted.
- Retries failed requests to improve reliability.
- Generates structured HTML output.
- Converts HTML into a print-ready PDF using Playwright (Chromium).
- Maintains execution logs for debugging.

---

## Project Structure

```text
PressRelease-Automation/
│
├── article_worker.py          # Extracts individual articles
├── scrape_month.py            # Monthly scraper
├── generate_pdf.py            # HTML & PDF generator
├── scraper.py                 # Playwright wrapper
├── utils.py                   # Helper utilities
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
├── sample_output/
│   ├── PIB_Mumbai_January_2026.html
│   └── PIB_Mumbai_January_2026.pdf
│
├── requirements.txt
└── README.md
```

---

## Technologies Used

- Python 3.x
- Playwright
- BeautifulSoup4
- HTML
- CSS
- JSON
- ReportLab

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/PressRelease-Automation.git

cd PressRelease-Automation
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Install the Playwright browser:

```bash
playwright install chromium
```

---

## Usage

### Step 1 — Scrape Press Releases

Run:

```bash
python scrape_month.py
```

The program will ask for the month number.

Example:

```text
Enter Month Number: 1
```

The scraper will:

- Navigate the PIB Mumbai Marathi website
- Search each day of the selected month
- Collect available press releases
- Extract article details
- Save progress in checkpoint files

---

### Step 2 — Generate HTML & PDF

Run:

```bash
python generate_pdf.py
```

The script will:

- Read the generated checkpoint file
- Create a formatted HTML document
- Convert the HTML into a PDF using Playwright

---

## Output

Generated files are stored inside the `output/` directory.

```text
output/
│
├── checkpoints/
│   └── January_2026.json
│
├── html/
│   └── PIB_Mumbai_January_2026.html
│
└── pdf/
    └── PIB_Mumbai_January_2026.pdf
```

Execution logs are stored in:

```text
logs/
```

---

## Workflow

```text
Select Month
      │
      ▼
Scrape Daily Articles
      │
      ▼
Extract Article Content
      │
      ▼
Save Checkpoint
      │
      ▼
Generate HTML
      │
      ▼
Generate PDF
```

---

## Reliability Features

- Automatic retry mechanism
- Resume support using checkpoints
- Duplicate content removal
- Footer and unnecessary content cleanup
- Modular architecture
- Execution logging

---

## Sample Output

The repository includes sample generated files in the `output/` directory.

- Sample HTML Output
- Sample PDF Output

---

## Future Improvements

- Microsoft Word (.docx) export
- Automatic table of contents
- PDF bookmarks
- Cover page generation
- Image extraction
- Searchable PDF index
- Command-line arguments
- Standalone executable using PyInstaller
- Multi-language support

---

## Author

**Rushikesh Zanwar**

Bachelor of Technology (B.Tech)

Python Automation Project

---

## Disclaimer

This is an independent educational and automation project developed for learning and research purposes.

It is **not affiliated with, endorsed by, or maintained by the Press Information Bureau (PIB)** or the Government of India.

All press release content remains the intellectual property of the Press Information Bureau (PIB), Government of India. This project only automates the extraction and compilation of publicly available information without claiming ownership of the original content.

---

## License

This project is intended for educational and research purposes.