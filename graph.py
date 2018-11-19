import sys
import yaml
from node import Node


class Graph:

    def __init__(self):
        self.id_to_node = {}
        self.basic_id_to_count = {}
        self.source = None
        self.depths = {}
        self.frequency_of_depth = {}

    @staticmethod
    def convert_raw_text_to_basic_node_id(raw_text):
        lower_case_name = raw_text.replace(' ', '_').lower()
        lower_case_name = lower_case_name.replace(',', '')
        return lower_case_name

    # This is an impure method
    def convert_raw_text_to_node_id(self, raw_text):
        basic_node_name = Graph.convert_raw_text_to_basic_node_id(raw_text)
        if basic_node_name in self.basic_id_to_count:
            node_id = basic_node_name + str(
                self.basic_id_to_count[basic_node_name])
            self.basic_id_to_count[basic_node_name] += 1
        else:
            node_id = basic_node_name
            self.basic_id_to_count[basic_node_name] = 0
        return node_id

    def insert_node(self, raw_name, parent_node):
        node_id = self.convert_raw_text_to_node_id(raw_name)
        node = Node(node_id, raw_name, parent_node)
        if not parent_node:
            self.source = node
            self.depths[node_id] = 0
            self.frequency_of_depth[0] = 1
        else:
            parent_node.append_child(node)
            new_depth = self.depths[parent_node.get_id()]+1
            self.depths[node_id] = new_depth
            if new_depth not in self.frequency_of_depth:
                self.frequency_of_depth[new_depth] = 1
            else:
                self.frequency_of_depth[new_depth] += 1
        self.id_to_node[node_id] = node
        return node

    def get_source(self):
        return self.source

    def get_freq_of_depth(self, depth):
        return self.frequency_of_depth[depth]

    # Assume single key in dict, which is the source node of the graph
    def add_nodes_recursively_from_yaml(self, yaml_file_name):
        with open(yaml_file_name, 'r') as stream:
            loaded_yaml = yaml.load(stream)
        if len(loaded_yaml.keys()) != 1:
            sys.exit('ERROR: Number of sources is not one')
        self.source = self.insert_node(loaded_yaml.keys()[0], None)
        value = loaded_yaml.values()[0]
        self.__insert_dict_val_in_graph(value, self.get_source())

    def __add_nodes_recursively_from_list(self, list_for_graph, parent_node):
        for list_element in list_for_graph:
            if isinstance(list_element, dict):
                self.__add_nodes_recursively_from_dict(list_element, parent_node)
            elif isinstance(list_element, str):
                parent_node.append_description(list_element)
            else:
                sys.exit('ERROR: Found list element {0} of type {1}'.
                         format(list_element, type(list_element)))

    def __insert_dict_val_in_graph(self, value, curr_node):
        if isinstance(value, str):
            curr_node.append_description(value)
        elif isinstance(value, list):
            self.__add_nodes_recursively_from_list(value, curr_node)
        elif value:
            sys.exit('ERROR: Found dict value = "{2}" of type {0} for curr_node {1}'.
                     format(type(value), curr_node, value))

    def __add_nodes_recursively_from_dict(self, dict_for_graph, parent_node):
        key_list = dict_for_graph.keys()
        for key in key_list:
            curr_node = self.insert_node(key, parent_node)
            value = dict_for_graph[key]
            self.__insert_dict_val_in_graph(value, curr_node)

    def get_depth(self, node):
        return self.depths[node.get_id()]

    def __str__(self):
        str_representation = 'List of nodes in graph is:\n\n'
        for node in self.id_to_node.values():
            str_representation += (node.__str__()+'\ndepth: {0}\n\n'.
                                   format(self.get_depth(node)))
        return str_representation
