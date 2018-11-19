class Renderer:

    BEGIN_DIGRAPH = 'digraph structs {'
    END_DIGRAPH = '}'
    NODE_CREATION_IN_DOT = '{0}[label=<{1}> style=filled fillcolor="{2}" fontcolor = "{3}"];'
    INVISIBLE_NODE_PREFIX = 'invisible_node'
    INVISIBLE_NODE_CREATION_IN_DOT = '{0}[label=<{0}>, style = invis];'
    EDGE_CREATION_IN_DOT = '{0} -> {1};'
    INVISIBLE_EDGE_CREATION_IN_DOT = '{0} -> {1} [style = invis];'
    BR_TAG = '<BR />'
    available_colors = [('#a6cee3', 'black'), ('#b2df8a', 'black'),
                        ('#1f78b4', 'white'), ('#fdbf6f', 'black'),
                        ('#fb9a99', 'black'), ('#e31a1c', 'white'),
                        ('#cab2d6', 'black'), ('#ff7f00', 'white'),
                        ('#33a02c', 'white'), ('#6a3d9a', 'white'),
                        ('#ffff99', 'black'), ('#b15928', 'white')]

    def get_node_colors(self, node, parent_node):
        node_depth = self.graph.get_depth(node)
        node_id = node.get_id()
        if node_depth == 1:
            color = Renderer.available_colors[
                self.num_level_1_nodes_observed]
            self.num_level_1_nodes_observed += 1
        elif node_depth == 0:
            color = ('white', 'black')
        else:
            color = self.color_of_nodes[parent_node.get_id()]

        self.color_of_nodes[node_id] = color
        return color

    def __init__(self, graph, dot_file_name):
        self.graph = graph
        self.dot_file_name = dot_file_name
        self.parent_id_of_new_invisible_node = self.graph.get_source().get_id()
        self.next_level_1_insertion = self.graph.get_source().get_id()
        self.num_invisible_nodes = 0
        self.slots_filled_at_next_parent_of_level_1_insertion = 0
        self.num_level_1_nodes_observed = 0
        self.color_of_nodes = {}

    def output_list_to_file(self, dot_output):
        file = open(self.dot_file_name, 'w+')
        file.write('\n'.join(dot_output))
        file.close()

    def render(self):
        source = self.graph.get_source()
        dot_output = [self.BEGIN_DIGRAPH]
        dot_output += self.get_dot_code_from_subtree(source, None)
        dot_output += self.END_DIGRAPH
        self.output_list_to_file(dot_output)

    def insert_invisible_node(self):
        dot_list = []
        new_invisible_node_name = self.INVISIBLE_NODE_PREFIX+'_' + \
                                  str(self.num_invisible_nodes)
        dot_list.append(self.INVISIBLE_NODE_CREATION_IN_DOT.format(
            new_invisible_node_name))
        dot_list.append(self.INVISIBLE_EDGE_CREATION_IN_DOT.format(
            self.parent_id_of_new_invisible_node, new_invisible_node_name))
        self.parent_id_of_new_invisible_node = new_invisible_node_name
        self.num_invisible_nodes += 1
        return dot_list

    def insert_invisible_nodes(self, num_invisible_nodes):
        dot_list = []
        for i in xrange(num_invisible_nodes):
            dot_list += self.insert_invisible_node()
        return dot_list

    def is_invincible(self, node_id):
        return self.INVISIBLE_NODE_PREFIX in self.parent_id_of_new_invisible_node

    def position_node(self, node):
        dot_list = []
        if self.graph.get_depth(node) != 1:
            return dot_list

        if self.is_invincible(self.next_level_1_insertion):
            dot_list.append(self.INVISIBLE_EDGE_CREATION_IN_DOT.format(
                self.parent_id_of_new_invisible_node, node.get_id()))

        if self.slots_filled_at_next_parent_of_level_1_insertion == 0:
                dot_list += self.insert_invisible_nodes(2)
        elif self.slots_filled_at_next_parent_of_level_1_insertion == 1:
            self.next_level_1_insertion = self.parent_id_of_new_invisible_node

        self.slots_filled_at_next_parent_of_level_1_insertion = \
            1 - self.slots_filled_at_next_parent_of_level_1_insertion
        return dot_list

    def get_label_from_node(self, node):
        return node.get_label().replace(' ', Renderer.BR_TAG)

    def get_dot_code_from_subtree(self, head_node, parent_of_head):
        node_colors = self.get_node_colors(head_node, parent_of_head)
        dot_list = [self.NODE_CREATION_IN_DOT.format(
            head_node.get_id(), self.get_label_from_node(head_node),
            node_colors[0], node_colors[1])]
        if parent_of_head:
            dot_list += self.position_node(head_node)
            dot_list.append(self.EDGE_CREATION_IN_DOT.format(
                parent_of_head.get_id(), head_node.get_id()))
        for child_node in head_node.get_children():
            dot_list += self.get_dot_code_from_subtree(child_node, head_node)

        return dot_list