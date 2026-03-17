feat = {
    'normalized_source': 'contract Test { uint public x = 42; }',
    'source_tokens': ['contract', 'test', '{', 'uint', 'public', 'x', '=', '42', ';', '}'],
    'bytecode': '6080604052348015610010...',
    'opcodes': ['PUSH1', '0x80', 'PUSH1', '0x40', 'MSTORE', ...],
    'embeddings': {},  # or {'source_avg': [0.12, -0.34, ...]}
    'contract_name': 'test',
    'file_path': 'D:\\...\\data\\raw\\contracts\\test.sol'
}