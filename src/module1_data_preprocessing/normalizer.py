import re

def normalize_contract(source: str) -> str:
    source = re.sub(r'/\*.*?\*/', '', source, flags=re.DOTALL)
    source = re.sub(r'//.*', '', source)
    source = re.sub(r'\s+', ' ', source).strip()
    return source