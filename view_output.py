import torch
import os
from torch_geometric.data.hetero_data import HeteroData

# Allow the specific HeteroData class for security
torch.serialization.add_safe_globals([HeteroData])

# Folder where your .pt files are
graph_folder = 'data/processed/graphs'

print(f"{'Graph File':<30} | {'Nodes':<10} | {'Edges':<10}")
print("-" * 55)

# Loop through every file in the folder
if os.path.exists(graph_folder):
    for filename in os.listdir(graph_folder):
        if filename.endswith('.pt'):
            file_path = os.path.join(graph_folder, filename)
            
            try:
                # Load the graph
                data = torch.load(file_path, weights_only=False)
                
                # Calculate totals
                total_nodes = sum(data[node_type].num_nodes for node_type in data.node_types)
                total_edges = sum(data[edge_type].num_edges for edge_type in data.edge_types)
                
                print(f"{filename:<30} | {total_nodes:<10} | {total_edges:<10}")
                
            except Exception as e:
                print(f"Error loading {filename}: {e}")
else:
    print(f"Folder not found: {graph_folder}")