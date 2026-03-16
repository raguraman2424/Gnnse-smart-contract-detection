import torch
from torch_geometric.data import HeteroData
from typing import Dict, Optional

def attach_node_embeddings(data: HeteroData, token_embeddings: Optional[Dict] = None) -> HeteroData:
    if not token_embeddings or "embeddings" not in token_embeddings:
        return data

    avg = token_embeddings["embeddings"].get("source_avg")
    if avg is None:
        return data

    try:
        avg_tensor = torch.tensor(avg, dtype=torch.float)
        for node_type in ["statement"]:
            if node_type in data and data[node_type].num_nodes > 0:
                n = data[node_type].num_nodes
                broadcast = avg_tensor.repeat(n, 1)
                if data[node_type].x is None:
                    data[node_type].x = broadcast
                elif data[node_type].x.shape[1] == broadcast.shape[1]:
                    data[node_type].x = torch.cat([data[node_type].x, broadcast], dim=1)
    except Exception:
        pass

    return data