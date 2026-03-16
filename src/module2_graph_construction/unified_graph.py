import torch
from torch_geometric.data import HeteroData
from slither.slither import Slither
from .cfg_builder import build_cfg
from .embedding import attach_node_embeddings

def create_heterogeneous_graph(slither: Slither, token_embeddings: dict = None) -> HeteroData:
    data = HeteroData()

    cfgs = build_cfg(slither)

    # Collect statement nodes from all CFGs
    stmt_features = []
    stmt_count = 0
    for _, cfg in cfgs.items():
        stmt_count += len(cfg.nodes)
        stmt_features.extend([[0.0] * 32 for _ in range(len(cfg.nodes))])

    data["statement"].num_nodes = stmt_count
    data["statement"].x = torch.tensor(stmt_features, dtype=torch.float)

    # Collect CFG edges (very simplified – no global re-indexing yet)
    edge_list = []
    offset = 0
    for _, cfg in cfgs.items():
        for u, v in cfg.edges:
            edge_list.append([u + offset, v + offset])
        offset += len(cfg.nodes)

    if edge_list:
        data["statement", "cfg_next", "statement"].edge_index = \
            torch.tensor(edge_list, dtype=torch.long).t().contiguous()

    # Attach embeddings (contract-level fallback)
    data = attach_node_embeddings(data, token_embeddings)

    return data