import pandas as pd
from pyvis.network import Network
import sys
import argparse


parser = argparse.ArgumentParser(description="A simple script for visualising a network from a TSV file")
parser.add_argument('--file', type=str, help="Path to tsv file", required=True)
parser.add_argument('--out', type=str, help="path for output html file", required=False,default='graph.html')

args = parser.parse_args()


# sys.setdefaultencoding('utf-8')

# Load TSV file
file_path = rf'{args.file}'
df = pd.read_csv(file_path, sep='\t',)
# Create a Pyvis network
net = Network(notebook=True, directed=True, filter_menu=True, select_menu=True)

node_scale = {
    "label": False,
    "min": 1,
    "max": 1,
}
properties ={
    "useImageSize": False,
}

def edge_color(section):
    edges_color = {
            "FULLTEXT": '#f07171',
            "INTRO": '#1f1d1d',
            "RESULTS": '#3a8037',
            "DISCUSS": '#e69f35',
            "TITLEABSTRACT": '#ccc'
    }
    if section in edges_color:
        return edges_color[section]
    else:
        return '#f07171'



# Add nodes and edges
for _, row in df.iterrows():
    source = row['Source']
    target = row['Target']
    edge_value = row['Interaction Type']
    section = row['Section']
    # Add the original nodes
    net.add_node(source, label=source, scaling=node_scale,widthConstraint=100, shape='circle', size=2, shapeProperties= properties)
    net.add_node(target, label=target, scaling=node_scale, widthConstraint=100, shape='circle', size=2, shapeProperties= properties)
    
    # Add edges with labels (title is used as a tooltip initially)
    net.add_edge(source, target, length= 300,title=str(section), label=str(edge_value), color=edge_color(section), width=4)



# Save the network to HTML
output_file = f'{args.out}'
# net.show_buttons(filter_=['physics'])
html_output = net.generate_html()
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_output)

# Function to inject custom JavaScript for edge labels
def customize_node_and_edge_labels(html_file):
    with open(html_file, 'r') as file:
        html_content = file.read()
    
    # Inject JavaScript for fine-tuning labels
    custom_js = """
    <script type="text/javascript">


        // Adjust edge labels to remain visible along the edges
        var edges = network.body.data.edges.get();
        edges.forEach(function(edge) {
            edge.font = {align: 'top', size: 14};  // Position edge labels in the middle
        });
        network.body.data.edges.update(edges);
    </script>
    """
    # Insert the script before the closing body tag
    updated_html = html_content.replace("</body>", custom_js + "</body>")
    
    # Save the updated HTML
    with open(html_file, 'w') as file:
        file.write(updated_html)

# Inject JavaScript into the generated HTML
customize_node_and_edge_labels(output_file)