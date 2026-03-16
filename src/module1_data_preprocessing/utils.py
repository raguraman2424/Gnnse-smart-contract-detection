from pathlib import Path
import json

def save_processed_features(features_list: list, output_dir: str):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    for feat in features_list:
        name = feat.get("contract_name", "unknown")
        with open(out / f"{name}.json", "w", encoding="utf-8") as f:
            json.dump(feat, f, indent=2, ensure_ascii=False)