from torch_geometric.data import InMemoryDataset

class ContractGraphDataset(InMemoryDataset):
    def __init__(self, root: str):
        super().__init__(root)
        # You can load .pt files here later