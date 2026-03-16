# src/main.py
"""
Main pipeline runner for GNNSE-based Smart Contract Vulnerability Detection
Runs Module 1 (preprocessing & feature extraction) → Module 2 (graph construction)
"""

# src/main.py
"""
Main pipeline runner...
"""

# src/main.py
"""
Main pipeline runner for GNNSE-based Smart Contract Vulnerability Detection
"""

import sys
from pathlib import Path

# ────────────────────────────────────────────────
# CRITICAL FIX: Add project root to sys.path
# This makes sure module1_data_preprocessing and module2_graph_construction are found
# Works on Windows, OneDrive, VS Code, etc.
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Debug: print the path to confirm
print(f"Added to sys.path: {project_root}")

# ────────────────────────────────────────────────
# Normal imports now work
import torch
from slither.slither import Slither

# Module 1 imports
from module1_data_preprocessing.dataset_loader import load_smartbugs_wild
from module1_data_preprocessing.multi_modal_extractor import extract_multi_modal_features
from module1_data_preprocessing.utils import save_processed_features

# Module 2 imports
from module2_graph_construction.unified_graph import create_heterogeneous_graph

# ────────────────────────────────────────────────
# Rest of your code (BASE_DIR, FEATURES_DIR, run_pipeline, etc.)
# ... paste your remaining code here ...

# ... rest of your code (BASE_DIR, run_pipeline, etc.) ...
# Project paths (relative to src/ folder)
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw" / "contracts"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
FEATURES_DIR = PROCESSED_DIR / "features"
GRAPHS_DIR = PROCESSED_DIR / "graphs"

# Create output directories if missing
FEATURES_DIR.mkdir(parents=True, exist_ok=True)
GRAPHS_DIR.mkdir(parents=True, exist_ok=True)


def run_pipeline(max_files: int = 10, verbose: bool = True):
    """
    Execute the full pipeline:
    1. Load .sol files → Module 1 (preprocessing)
    2. Process each contract → create JSON features
    3. Use features + Slither → Module 2 (graph construction)
    4. Save graphs as .pt files
    """
    print("=" * 60)
    print("GNNSE Pipeline - Smart Contract Vulnerability Detection")
    print(f"Scanning folder: {RAW_DIR}")
    print(f"Max files to process: {max_files}")
    print("=" * 60 + "\n")

    # ────────────────────────────────────────────────
    # Step 1: Module 1 - Data Acquisition & Preprocessing
    # ────────────────────────────────────────────────
    print("[Module 1] Loading & Preprocessing contracts...")
    features_list = []

    for path, name in load_smartbugs_wild(RAW_DIR, max_contracts=max_files):
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
            features = extract_multi_modal_features(source)
            features["contract_name"] = name
            features["file_path"] = str(path)
            features_list.append(features)

            if verbose:
                print(f"  ✓ Processed: {name}  ({len(source):,} chars)")
        except Exception as e:
            print(f"  ✗ Failed {name}: {str(e)[:100]}...")

    if not features_list:
        print("\nNo valid contracts found. Check data/raw/contracts/ folder.")
        return

    # Save JSON features
    save_processed_features(features_list, str(FEATURES_DIR))
    print(f"\n[Module 1] Success → Saved {len(features_list)} JSON files to:")
    print(f"   {FEATURES_DIR}\n")

    # ────────────────────────────────────────────────
    # Step 2: Module 2 - Graph Construction
    # ────────────────────────────────────────────────
    print("[Module 2] Building heterogeneous graphs...")
    success_count = 0

    for feat in features_list:
        sol_path = Path(feat["file_path"])
        try:
            slither = Slither(str(sol_path))
            graph = create_heterogeneous_graph(slither, feat)
            out_path = GRAPHS_DIR / f"{feat['contract_name']}_graph.pt"
            torch.save(graph, out_path)

            success_count += 1
            if verbose:
                print(f"  ✓ Graph saved: {out_path.name}")
        except Exception as e:
            print(f"  ✗ Graph failed for {feat['contract_name']}: {str(e)[:120]}...")

    print(f"\n[Module 2] Finished → Created {success_count} graph files in:")
    print(f"   {GRAPHS_DIR}\n")

    print("Pipeline execution complete.")
    print(f"Total successful contracts: {success_count}/{len(features_list)}")


if __name__ == "__main__":
    # Change this number to control how many contracts to process
    # Start small (5–20) → increase after testing
    run_pipeline(max_files=10, verbose=True)