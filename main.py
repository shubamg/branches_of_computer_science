from graph import Graph

FILE_TO_READ = 'raw_wikipedia_article.yaml'
graph = Graph()
graph.add_nodes_recursively_from_yaml(FILE_TO_READ)

print graph
