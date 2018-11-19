from graph import Graph
from renderer import Renderer

FILE_TO_READ = 'raw_wikipedia_article.yaml'
OUT_FILE_NAME = 'branches_of_CSE.dot'
graph = Graph()
graph.add_nodes_recursively_from_yaml(FILE_TO_READ)
renderer = Renderer(graph, OUT_FILE_NAME)
renderer.render()
