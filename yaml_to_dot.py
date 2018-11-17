import yaml
from subprocess import check_call

CIRCLE_SHAPE = 'circle'
BOX_SHAPE = 'box'
OCTAGON_SHAPE = 'octagon'
HEXAGON_SHAPE = 'hexagon'

BEGIN_DIGRAPH = 'digraph structs {'
END_DIAGRAPH = '}'
GRAPH_PROPERTIES = 'graph [];'
NODE_PROPERTIES = 'node [margin=0 fontcolor=blue shape={0}]'.format(
  OCTAGON_SHAPE)
MAIN_HEADING = 'Computer science'
FILE_TO_WRITE = 'python_produced_DOT.txt'
OUT_FILE_NAME = 'branches_of_CSE'
OUT_EXTENSION = 'png'
BR_TAG = '<BR />'
INVISIBLE_NODE_LABEL = 'invisible node'
INVISIBLE_CLAUSE = 'style = invis'
FILE_TO_READ = 'raw_wikipedia_article.yaml'

color_list = ['chartreuse', 'red', 'cadetblue', 'brown', 'darkolivegreen1',
              'forestgreen', 'gold', 'darksalmon', 'gray', 'yellow', 'darkviolet',
              'cornflowerblue', 'chocolate2']


def get_node_name(branch_raw_heading, name_suffix=''):
  lower_case_name = branch_raw_heading.replace(' ', '_').lower()
  lower_case_name = lower_case_name.replace(',', '')
  return lower_case_name + name_suffix


def get_invisible_node_creation_line(node_name):
  return '{0}[label=<{0}>, {1}];'.format(node_name, INVISIBLE_CLAUSE)


def get_node_creation_line(branch_raw_name, shape='', name_suffix='',
                           color='white'):
  node_heading = get_node_name(branch_raw_name, name_suffix)
  branch_raw_name = branch_raw_name.replace(' ', BR_TAG)
  if shape:
    node_line = '{0}[label=<{1}> shape={2} style=filled fillcolor="{3}"];'.format(node_heading,
                                                     branch_raw_name, shape,
                                                               color)
  else:
    node_line = '{0}[label=<{1}> style=filled fillcolor="{2}"];'.format(node_heading,
                                                     branch_raw_name, color)
  return node_line


def insert_edge(parent_name, child_name):
  return '{0} -> {1};'.format(parent_name, child_name)


with open(FILE_TO_READ, 'r') as stream:
  loaded_yaml = yaml.load(stream)
# loaded yaml is a list of dict(string -> dict(str -> str))
# print len(loaded_yaml[0].values()[0])
dot_list =[]
dot_list.append(BEGIN_DIGRAPH)
dot_list.append(GRAPH_PROPERTIES)
dot_list.append(NODE_PROPERTIES)
dot_list.append(get_node_creation_line(MAIN_HEADING, 'circle'))
super_node_heading = get_node_name(MAIN_HEADING)
parent_name = super_node_heading
invisible_nodes_cnt = 0
for branch in loaded_yaml:
  branch_raw_name = branch.keys()[0]
  dot_list.append(get_node_creation_line(branch_raw_name, HEXAGON_SHAPE,
                                         color=color_list[invisible_nodes_cnt]))
  child_name = get_node_name(branch_raw_name)
  dot_list.append(insert_edge(super_node_heading, child_name))
  if invisible_nodes_cnt:
    dot_list.append('{0} -> {1} [ {2} ];'.format(parent_name,
                                                 child_name, INVISIBLE_CLAUSE))
  invisible_node = get_node_name(INVISIBLE_NODE_LABEL+str(invisible_nodes_cnt))
  dot_list.append(get_invisible_node_creation_line(invisible_node))
  dot_list.append('{0} -> {1} [ {2} ];'.format(parent_name,
                                               invisible_node, INVISIBLE_CLAUSE))

  parent_name = invisible_node
  invisible_nodes_cnt += 1


for branch in loaded_yaml:
  branch_raw_name = branch.keys()[0]
  parent_name = get_node_name(branch_raw_name)
  for sub_branch_dict in branch.values()[0]:
    print sub_branch_dict
    sub_branch_raw_name = sub_branch_dict.keys()[0]
    child_name_suffix = ''
    child_node_name = get_node_name(sub_branch_raw_name)
    if child_node_name == parent_name:
      child_name_suffix = '0'
      child_node_name += child_name_suffix
    dot_list.append(get_node_creation_line(sub_branch_raw_name,
                                           name_suffix=child_name_suffix))
    child_node_name = get_node_name(sub_branch_raw_name,
                                    name_suffix=child_name_suffix)
    dot_list.append(insert_edge(parent_name, child_node_name))
dot_list.append(END_DIAGRAPH)


file = open(FILE_TO_WRITE, 'w+')
file.write('\n'.join(dot_list))
file.close()
check_call(['dot', '-T{0}'.format(OUT_EXTENSION), FILE_TO_WRITE, '-o', '{0}.{1}'.format(OUT_FILE_NAME, OUT_EXTENSION)])
