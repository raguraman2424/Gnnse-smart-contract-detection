import torch
import os
import csv
from torch_geometric.data.hetero_data import HeteroData

# 1. Security: Allow the specific HeteroData class for loading
torch.serialization.add_safe_globals([HeteroData])

def summarize_all_graphs(input_folder, output_csv):
    # Ensure the input folder exists
    if not os.path.exists(input_folder):
        print(f"❌ Error: Folder not found: {input_folder}")
        return

    # List to store data for the CSV
    summary_data = []

    print(f"{'Graph File':<30} | {'Nodes':<10} | {'Edges':<10}")
    print("-" * 55)

    # 2. Loop through every file in the folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.pt'):
            file_path = os.path.join(input_folder, filename)
            
            try:
                # Load the graph
                # Note: weights_only=False is required for custom classes like HeteroData
                data = torch.load(file_path, weights_only=False, map_location='cpu')
                
                # Calculate totals across all node and edge types
                total_nodes = sum(data[node_type].num_nodes for node_type in data.node_types)
                total_edges = sum(data[edge_type].num_edges for edge_type in data.edge_types)
                
                # Print to console for immediate feedback
                print(f"{filename:<30} | {total_nodes:<10} | {total_edges:<10}")
                
                # Store for CSV
                summary_data.append([filename, total_nodes, total_edges])
                
            except Exception as e:
                print(f"❌ Error loading {filename}: {e}")

    # 3. Save the results to a CSV file
    try:
        with open(output_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            # Write Header
            writer.writerow(['Graph Filename', 'Total Nodes', 'Total Edges'])
            # Write Data
            writer.writerows(summary_data)
        
        print("-" * 55)
        print(f"✅ Success! Summary saved to: {os.path.abspath(output_csv)}")
    except Exception as e:
        print(f"❌ Failed to save CSV: {e}")

if __name__ == "__main__":
    # CONFIGURATION: Change these paths if your folders are named differently
    GRAPH_FOLDER = 'data/processed/graphs'
    OUTPUT_FILE = 'graph_summary_report.csv'

    summarize_all_graphs(GRAPH_FOLDER, OUTPUT_FILE)