from dataclasses import dataclass

import pymupdf

@dataclass
class Page:
    page_number : int
    text : str

def load_pdf(pdf_path: str)-> list[Page]:
    document = pymupdf.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")
         
        pages.append(
            Page(
                page_number=page_number,
                text=text.strip(),
            )
        )

    document.close()

    return pages