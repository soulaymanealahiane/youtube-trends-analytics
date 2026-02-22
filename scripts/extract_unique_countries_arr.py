
"""
dataset_geocoding.py

Run with:
    python dataset_geocoding.py

This script reads the Excel file (read-only), auto-detects the column
that most likely contains 2-letter country codes, and prints a
copy-ready Python list of unique codes (preserving first-seen order).
"""

import pandas as pd
import re
import sys

# === CONFIG: set your Excel path here (already set to what you gave) ===
EXCEL_PATH = r"C:\Users\pc\OneDrive - Al Akhawayn University in Ifrane\Desktop\BAI_midterm_project\midterm_project_data.xlsx"
# ======================================================================

def load_df(path):
    try:
        return pd.read_excel(path, dtype=str)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Could not read Excel file: {e}", file=sys.stderr)
        sys.exit(1)

def find_best_column(df):
    """Return the column name that has the most 2-letter alpha tokens."""
    two_letter_re = re.compile(r'\b([A-Za-z]{2})\b')
    best_col = None
    best_count = -1
    n_rows = len(df)
    for col in df.columns:
        col_count = 0
        # iterate values and count rows having at least one 2-letter token
        for val in df[col].dropna().astype(str):
            if two_letter_re.search(val):
                col_count += 1
        if col_count > best_count:
            best_count = col_count
            best_col = col
    # if nothing found, fall back to first column
    if best_count <= 0:
        return df.columns[0]
    return best_col

def extract_codes_from_cell(cell):
    """Return list of 2-letter tokens found in a cell (uppercased)."""
    if cell is None:
        return []
    s = str(cell).strip()
    # find all standalone 2-letter alphabetic tokens
    tokens = re.findall(r'\b([A-Za-z]{2})\b', s)
    return [t.upper() for t in tokens]

def main():
    df = load_df(EXCEL_PATH)
    if df.empty:
        print("[ERROR] Excel file is empty.", file=sys.stderr)
        sys.exit(1)

    chosen_col = find_best_column(df)
    print(f"[info] Using column: '{chosen_col}'", file=sys.stderr)

    seen = set()
    unique_codes = []

    # iterate rows in original order, pull all 2-letter tokens from each cell
    for cell in df[chosen_col].fillna('').astype(str):
        codes = extract_codes_from_cell(cell)
        for c in codes:
            if c not in seen:
                seen.add(c)
                unique_codes.append(c)

    # Final fallback: if no codes found at all, try the first column but accept any non-empty values
    if not unique_codes:
        print("[warning] No 2-letter codes found in detected column; falling back to extracting non-empty values from first column.", file=sys.stderr)
        first_col = df.columns[0]
        for v in df[first_col].dropna().astype(str).str.strip():
            up = v.upper()
            if up not in seen:
                seen.add(up)
                unique_codes.append(up)

    # Print results: Python list (copy-ready) and CSV line
    print("\n# Python list (copy this):")
    print(repr(unique_codes))

    print("\n# CSV line:")
    print(",".join(unique_codes))

if __name__ == "__main__":
    main()
