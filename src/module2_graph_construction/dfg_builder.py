import networkx as nx
from slither.slither import Slither

def build_simple_dfg(slither: Slither) -> nx.DiGraph:
    G = nx.DiGraph()
    for contract in slither.contracts:
        for function in contract.functions_declared:
            for node in function.nodes:
                nid = f"node_{node.node_id}"
                # Use var.canonical_name instead of var.name
                for var in node.variables_read:
                    G.add_edge(f"var_{var.canonical_name}", nid, relation="USE")
                for var in node.variables_written:
                    G.add_edge(nid, f"var_{var.canonical_name}", relation="DEF")
    return G