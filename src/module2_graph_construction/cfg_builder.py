import networkx as nx
from slither.slither import Slither

def build_cfg(slither: Slither) -> dict:
    cfgs = {}
    for contract in slither.contracts:
        for function in contract.functions_declared:
            if not function.is_implemented:
                continue
            G = nx.DiGraph()
            for node in function.nodes:
                nid = node.node_id
                
                # FIX: Access 'lines' as an attribute, not a dictionary key
                line_number = 0
                if node.source_mapping and hasattr(node.source_mapping, 'lines'):
                    line_number = node.source_mapping.lines[0] if node.source_mapping.lines else 0
                
                G.add_node(nid, line=line_number)
                
                for son in node.sons:
                    G.add_edge(nid, son.node_id)
            cfgs[function.full_name] = G
    return cfgs