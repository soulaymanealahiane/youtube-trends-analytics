"""
drop_columns_stream.py
Reads a large CSV in chunks, drops irrelevant columns, and writes a new CSV
in the same folder as the original file.

This version drops: kind, title, video_tags, channel_id, thumbnail_url, description, snapshot_date
"""
from pathlib import Path
import pandas as pd

# === CONFIG ===
INPUT_PATH = r"C:\Users\pc\OneDrive - Al Akhawayn University in Ifrane\Desktop\BAI_midterm_project\data\original_dataset.csv"
CHUNKSIZE = 100_000  # adjust if needed
# Columns to drop
TO_DROP = {"kind", "title", "video_tags", "channel_id", "thumbnail_url", "description", "snapshot_date"}
# =================

def drop_columns_stream(input_path: str, chunksize: int = 100_000):
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    out_name = input_path.stem + "_reduced_columns" + input_path.suffix
    out_path = input_path.with_name(out_name)

    first_chunk = True
    total_read = 0
    total_written = 0

    with open(input_path, "r", encoding="utf-8", errors="replace") as fh:
        for chunk in pd.read_csv(fh, chunksize=chunksize):
            total_read += len(chunk)

            # On the first chunk, show which columns exist and what will be dropped/kept
            if first_chunk:
                present_drop = [c for c in TO_DROP if c in chunk.columns]
                found_columns = list(chunk.columns)
                kept_columns = [c for c in found_columns if c not in TO_DROP]
                print("Columns found in input file:")
                print(found_columns)
                print("\nColumns that will be dropped (if present):")
                print(present_drop)
                print("\nColumns that will be kept in output:")
                print(kept_columns)
                # continue processing as usual after printing

            # drop only columns that actually exist in this chunk
            drop_here = [c for c in TO_DROP if c in chunk.columns]
            if drop_here:
                chunk = chunk.drop(columns=drop_here)

            # write to output CSV (header only on first write)
            if first_chunk:
                chunk.to_csv(out_path, index=False, mode="w", header=True)
                first_chunk = False
            else:
                chunk.to_csv(out_path, index=False, mode="a", header=False)

            total_written += len(chunk)
            print(f"Processed: {total_read} rows; Written: {total_written} rows", end="\r")

    print(f"\nDone. Output saved to: {out_path}")
    print(f"Total rows processed: {total_read}, total rows written: {total_written}")

if __name__ == "__main__":
    drop_columns_stream(INPUT_PATH, CHUNKSIZE)
