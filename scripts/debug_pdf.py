from src.config import SOURCE_PDF
from src.ingestion.loader import load_pdf


def main():
    pages = load_pdf(str(SOURCE_PDF))

    print(f"Pages: {len(pages)}")

    for page in pages[:5]:
        print("\n" + "=" * 80)
        print(f"PAGE {page.page_number}")
        print("=" * 80)

        for i, line in enumerate(page.text.splitlines()):
            print(f"{i:03}: {line!r}")


if __name__ == "__main__":
    main()