import os
import pybtex.database.input.bibtex as bibtex_input
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from datetime import datetime

# Path to the TTF font file
font_path = "NotoSans-Regular.ttf"  # path to the font file


def bold_leo_lahti(name):
    """Bold 'Leo Lahti' in the given name string."""
    return name.replace('Leo Lahti', '<b>Leo Lahti</b>')

def format_author_name(author):
    """Reformat author name to 'First Name Last Name' and bold 'Leo Lahti'."""
    first_names = ' '.join(author.first_names)
    last_names = ' '.join(author.last_names)
    full_name = f"{first_names} {last_names}"
    if 'Leo' in author.first_names and 'Lahti' in author.last_names:
        full_name = f"<b>{full_name}</b>"
    return full_name


def format_entry(entry):
    authors = ', '.join(format_author_name(author) for author in entry.persons['author'])
    title = entry.fields.get('title', 'No title available')
    journal = entry.fields.get('journal', 'No journal available')
    year = entry.fields.get('year', 'No year available')
    pages = entry.fields.get('pages', 'No pages available')
    doi = entry.fields.get('doi', 'No DOI available')

    formatted_entry = f"[{entry.key}] {authors}. \"{title}\". In: {journal} ({year}), pp. {pages}. doi: {doi}."
    return formatted_entry

def main():
    try:
        # Define the path to your .bib file and output PDF
        bib_file = "lahti.bib"  # Replace with the actual path to your .bib file
        pdf_file = "Leo_Lahti.pdf"  # Replace with the desired output PDF path

        # Parse the BibTeX file
        parser = bibtex_input.Parser()
        bib_data = parser.parse_file(bib_file)

        # Register the TTF font
        pdfmetrics.registerFont(TTFont('NotoSans', font_path))

        # PDF Styles with TTF font
        styles = getSampleStyleSheet()
        styles['Title'].fontName = 'NotoSans'
        styles['BodyText'].fontName = 'NotoSans'

        # Create a PDF with the formatted entries
        doc = SimpleDocTemplate(pdf_file, pagesize=letter)
        flowables = [
            Paragraph("List of Publications", styles['Title']),
            Spacer(1, 12),
            Paragraph("Leo Lahti Phd", styles['Title']),
            Paragraph(datetime.now().strftime("%Y-%m-%d"), styles['Title']),
            Spacer(1, 20)
        ]

        for key, entry in bib_data.entries.items():
            formatted_entry = format_entry(entry)
            flowables.append(Paragraph(formatted_entry, styles['BodyText']))
            flowables.append(Spacer(1, 12))

        doc.build(flowables)
        print(f"Successfully generated PDF at: {pdf_file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
