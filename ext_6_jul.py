import os
import json

# === CONFIGURE THESE PATHS ===
ARCHIVE_ROOT       = "myarchive"                      # where your use-case folders live
ENRICHED_JSON_PATH = "mitre_enriched_data.json"       # your existing enriched JSON
OUTPUT_JSON_PATH   = "mitre_enriched_with_files.json" # where to write the new JSON

# === UTILS ===
def slurp_file(path):
    """Return the file’s full text, or None if it doesn’t exist or can’t be read."""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except (IOError, OSError):
        return None

# === MAIN ===
def attach_files_to_enriched():
    # 1) load your enriched JSON
    with open(ENRICHED_JSON_PATH, encoding="utf-8") as f:
        enriched = json.load(f)

    # 2) for each use-case in the JSON, read the three files
    for usecase, data in enriched.items():
        folder_path = os.path.join(ARCHIVE_ROOT, usecase)
        files_data = {}
        for fname in ("drilldown.spl", "search.spl", "README.md"):
            full_path = os.path.join(folder_path, fname)
            files_data[fname] = slurp_file(full_path)
        # attach under a new key
        data["files"] = files_data

    # 3) write out the augmented JSON
    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2)

    print(f"Wrote {len(enriched)} use-cases → {OUTPUT_JSON_PATH}")

if __name__ == "__main__":
    attach_files_to_enriched()
