import re
from typing import List

def tokenize_solidity(source: str) -> List[str]:
    tokens = re.findall(r'\b\w+\b|[+\-*/=(){}\[\];.,<>&|!~%^?:]', source)
    return [t.lower() for t in tokens if t.strip()]