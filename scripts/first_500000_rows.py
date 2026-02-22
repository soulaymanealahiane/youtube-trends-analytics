"""
keep_first_500k_rows.py
Streams the input CSV and writes only the first 500000 data rows (all columns preserved)
to a new CSV in the same folder. Uses chunked reading to avoid large memory use.
"""
from pathlib import Path
import pandas as pd

# === CONFIG ===

INPUT_PATH = r"C:\Users\pc\OneDrive - Al Akhawayn University in Ifrane\Desktop\BAI_midterm_project\data\original_dataset.csv"
CHUNKSIZE = 100_000  # adjust smaller if you hit memory issues
KEEP_ROWS = 500_000
# =================

def keep_first_n_rows(input_path: str, keep_rows: int = KEEP_ROWS, chunksize: int = CHUNKSIZE):
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    out_name = input_path.stem + f"_first_{keep_rows}_rows" + input_path.suffix
    out_path = input_path.with_name(out_name)

    written = 0
    first_chunk = True

    # Open with safe decoding to avoid UnicodeDecodeError stopping the run
    with open(input_path, "r", encoding="utf-8", errors="replace") as fh:
        for chunk in pd.read_csv(fh, chunksize=chunksize):
            if written >= keep_rows:
                break

            remaining = keep_rows - written
            if len(chunk) <= remaining:
                to_write = chunk
            else:
                to_write = chunk.iloc[:remaining]

            # write header only once
            if first_chunk:
                to_write.to_csv(out_path, index=False, mode="w", header=True)
                first_chunk = False
            else:
                to_write.to_csv(out_path, index=False, mode="a", header=False)

            written += len(to_write)
            print(f"Written {written}/{keep_rows} rows", end="\r")

    print(f"\nDone. Output saved to: {out_path}")
    print(f"Rows written: {written} (requested: {keep_rows})")

if __name__ == "__main__":
    keep_first_n_rows(INPUT_PATH, KEEP_ROWS, CHUNKSIZE)
