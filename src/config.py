from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

SOURCE_PDF = RAW_DATA_DIR / "hawkvision_product_spec.pdf"

PARENT_CHUNK_SIZE = 2000
CHILD_CHUNK_SIZE = 500
CHILD_CHUNK_OVERLAP= 100

