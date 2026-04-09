"""
src/nlp/stage02_validate_sgolla.py - Validate Stage
(EDIT YOUR COPY OF THIS FILE)

Source: Raw HTML string
Sink:   BeautifulSoup object (in memory)

Purpose

  Validates that the expected page structure is present.

Analytical Questions

- What is the top-level structure of the HTML document?
- What elements are present in the document?
- What data types are associated with each field?
- Does the data meet expectations for transformation?

Notes

Following our process, do NOT edit this _case file directly,
keep it as a working example.

In your custom project, copy this _case.py file and
append with _yourname.py instead.

Then edit your copied Python file to:
- inspect the JSON structure for your API,
- validate required keys and types,
- confirm the data is usable for your analysis.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from bs4 import BeautifulSoup

# ============================================================
# Section 2. Define Run Validate Function
# ============================================================


def run_validate(
    html_content: str,
    LOG: logging.Logger,
) -> BeautifulSoup:
    """Inspect and validate HTML structure.

    Args:
        html_content (str): The raw HTML content from the Extract stage.
        LOG (logging.Logger): The logger instance.

    Returns:
        BeautifulSoup: The validated BeautifulSoup object.
    """
    LOG.info("========================")
    LOG.info("STAGE 02: VALIDATE starting...")
    LOG.info("Purpose: Inspect and validate HTML structure")
    LOG.info("========================")

    # ============================================================
    # INSPECT HTML STRUCTURE
    # ============================================================

    LOG.info("HTML STRUCTURE INSPECTION:")
    LOG.info(
        "Checking for required elements (title, authors, abstract, subjects, dateline)..."
    )

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Log the type of the top-level HTML structure.
    LOG.info(f"Top-level type: {type(soup).__name__}")

    # Log the top-level elements in the HTML document
    LOG.info(
        f"Top-level elements: {[element.name for element in soup.find_all(recursive=False)]}"
    )

    # ============================================================
    # VALIDATE EXPECTATIONS
    # ============================================================

    # Check for expected structural elements
    title = soup.find("h1", class_="title")
    authors = soup.find("div", class_="authors")
    abstract = soup.find("blockquote", class_="abstract")
    subjects = soup.find("div", class_="subheader")
    dateline = soup.find("div", class_="dateline")

    LOG.info("VALIDATE: Title found: %s", title is not None)
    if title:
        LOG.info(f"  Title preview: {title.get_text(strip=True)[:80]}...")
    LOG.info("VALIDATE: Authors found: %s", authors is not None)
    if authors:
        author_list = [a.get_text(strip=True) for a in authors.find_all("a")]
        LOG.info(f"  Author count: {len(author_list)}")
    LOG.info("VALIDATE: Abstract found: %s", abstract is not None)
    if abstract:
        abstract_text = abstract.get_text(strip=True)
        LOG.info(f"  Abstract preview: {abstract_text[:80]}...")
        LOG.info(f"  Abstract length: {len(abstract_text)} characters")
    LOG.info("VALIDATE: Subjects found: %s", subjects is not None)
    if subjects:
        LOG.info(f"  Subjects: {subjects.get_text(strip=True)}")
    LOG.info("VALIDATE: Dateline found: %s", dateline is not None)
    if dateline:
        LOG.info(f"  Submission date: {dateline.get_text(strip=True)}")

    missing = []
    if not title:
        missing.append("title")
    if not authors:
        missing.append("authors")
    if not abstract:
        missing.append("abstract")
    if not subjects:
        missing.append("subjects")
    if not dateline:
        missing.append("dateline")

    if missing:
        raise ValueError(
            f"VALIDATE: Required elements missing: {missing}. "
            "Page structure may have changed."
        )

    LOG.info("VALIDATE: HTML structure is valid.")
    LOG.info("Sink: validated BeautifulSoup object")

    # Return the validated BeautifulSoup object for use in the next stage.
    return soup
