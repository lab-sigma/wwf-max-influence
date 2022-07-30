import pandas as pd

# import plotly.graph_objects as go

from pyvis.network import Network
import networkx as nx
import matplotlib.pyplot as plt


df = pd.read_excel(open('data.xlsx', 'rb'), sheet_name='Interview data', header=[0,1], dtype=str, keep_default_na=False)  

table = df.iloc[: , :11]

graph = {}

for index, row in table.iterrows():
	i = row[0] 
	if i not in graph:
		graph[i] = set()

	for k in range(1, 11):
		j = row[k]
		# if j == '1501':
		# 	print("<<<", i, j)
		if j != "N/A":
			graph[i].add(j)
			### undirected graph
			if j not in graph:
				graph[j] = set()
			graph[j].add(i)
	# if i == '1501':
	# 	print(">>>", i, graph[i])
# print(graph['1801'])
# print(graph['1501'])

total_nodes = len(graph)
k = 5


print("total nodes: ", total_nodes)
### first degree connectivity
sol = []
connected = set()
for i in range(k):
	candidate = -1
	effect = 0
	for node, child in graph.items():
		new_connected = connected.union(child)
		new_effect = len(new_connected) - len(connected)
		# new_effect = len(child) 
		if new_effect > effect:
			candidate = node
			effect = new_effect
	sol.append(candidate)
	connected = connected.union( graph[candidate] )
	# G.nodes[candidate]['color'] = 'red'
	print( candidate, len(connected) )

print(sol)

G = nx.Graph()
nt = Network(height='100%', width='100%')

for node in graph.keys():
	if node in sol:
		G.add_node(node, color='red', size=20, font='40px arial black')
	elif node in connected:
		G.add_node(node, color='#CE6A85')
	else:
		G.add_node(node)

for n, children in graph.items():
	for c in children:
		if n in sol or c in sol:
			G.add_edge(n, c, color='#CE6A85', width=2, alpha=0.5)
		else:
			G.add_edge(n, c, color='grey', alpha=0.5)

nt.from_nx(G)
# nt.show_buttons(filter_=['physics'])
nt.set_options("""
{
  "physics": {
    "forceAtlas2Based": {
      "springLength": 100
    },
    "minVelocity": 0.75,
    "solver": "forceAtlas2Based"
  }
}
"""
)
nt.show('nx-connectivity.html')


## cascade
print("cascade")

sol = []
connected = set()
secondary = set()
for i in range(k):
	candidate = -1
	effect = 0
	for node, child in graph.items():
		new_effect = 0
		for c in child.difference(connected):
			new_effect += len( graph[c].difference(connected) ) * 0.5

		if new_effect > effect:
			candidate = node
			effect = new_effect
	sol.append(candidate)
	connected = connected.union( graph[candidate] )
	for c in graph[candidate]:
		secondary = secondary.union( graph[c])
	# print( candidate, len(secondary) )

# print(sol)
# print(connected)
# print(secondary)

G = nx.Graph()
nt = Network(height='100%', width='100%')

for node in graph.keys():
	if node in sol:
		G.add_node(node, color='red', size=25, font='40px arial black')
	elif node in connected:
		G.add_node(node, color='#CE6A85', size=15)
	elif node in secondary:
		G.add_node(node, color='#F1CE95')
	else:
		G.add_node(node)

for n, children in graph.items():
	for c in children:
		if n in sol or c in sol:
			G.add_edge(n, c, color='#CE6A85', width=3, alpha=0.5)
		elif n in connected or c in connected:
			G.add_edge(n, c, color='#F1CE95', width=1.5, alpha=0.5)
		else:
			G.add_edge(n, c, color='grey', alpha=0.5)

nt.from_nx(G)
# nt.show_buttons(filter_=['physics'])
nt.set_options("""
{
  "physics": {
    "forceAtlas2Based": {
      "springLength": 100
    },
    "minVelocity": 0.75,
    "solver": "forceAtlas2Based"
  }
}
"""
)
nt.show('nx-cascade.html')


