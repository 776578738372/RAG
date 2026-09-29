from src.config import SOURCE_PDF
from src.ingestion.loader import load_pdf

def main():
    pages= load_pdf(str(SOURCE_PDF))

    print(f"Pages extracted: {len(pages)}")

    for page in pages[:3]:
        print("\n" + "=" * 80)
        print(f"PAGE {page.page_number}")
        print("=" * 80)
        print(page.text[:2000])

if __name__ == "__main__":
    main()