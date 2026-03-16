from typing import Dict, Optional
import solcx
from .normalizer import normalize_contract
from .tokenizer import tokenize_solidity

def safe_compile(source: str) -> Dict:
    try:
        solcx.install_solc('0.8.20')
        solcx.set_solc_version('0.8.20')
        compiled = solcx.compile_source(source, output_values=["bin", "asm"])
        iface = next(iter(compiled.values()))
        return {
            "bytecode": iface.get("bin", ""),
            "opcodes": iface.get("asm", "").split()
        }
    except Exception:
        return {"bytecode": "", "opcodes": []}

def extract_multi_modal_features(source_code: str) -> Dict:
    normalized = normalize_contract(source_code)
    source_tokens = tokenize_solidity(normalized)
    compile_result = safe_compile(normalized)

    return {
        "normalized_source": normalized,
        "source_tokens": source_tokens,
        "bytecode": compile_result["bytecode"],
        "opcodes": compile_result["opcodes"],
        "embeddings": {}  # extend later with Word2Vec
    }