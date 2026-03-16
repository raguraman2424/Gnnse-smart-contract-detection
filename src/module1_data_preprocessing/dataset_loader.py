from pathlib import Path
from typing import Iterator, Tuple
from tqdm import tqdm

def load_smartbugs_wild(
    root_dir: str | Path,
    max_contracts: int | None = None,
    min_size_kb: int = 1
) -> Iterator[Tuple[Path, str]]:
    root = Path(root_dir).resolve()
    count = 0
    for path in tqdm(root.rglob("*.sol"), desc="Scanning .sol files"):
        if max_contracts is not None and count >= max_contracts:
            break
        if path.stat().st_size < min_size_kb * 1024:
            continue
        yield path, path.stem
        count += 1