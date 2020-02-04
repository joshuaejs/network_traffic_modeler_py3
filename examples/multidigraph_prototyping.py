import sys
sys.path.append('../')
import numpy

from pprint import pprint

from pyNTM import Parallel_Link_Model

def normalize_multidigraph_paths(multidigraph_path_info):
    """
    Takes the multidigraph_path_info and normalizes it to create all the
    path combos that only have one link between each node.

    :param multidigraph_path_info: Dict of path information from a source node
    to a destination node.  Keys are 'cost' and 'path'.

    'cost': Cost of shortest path from source (integer)
    'path': List of of interface hops from a source
    node to a destination node.  Each hop in the path
    is a list of all the interfaces from the current node
    to the next node.

    multidigraph_path_info example:
    {'cost': 40,
    'path': [[[Interface(name = 'A-to-D', cost = 40, capacity = 10, node_object = Node('A'),
           remote_node_object = Node('D'), address = '7')]],
          [[Interface(name = 'A-to-B_2', cost = 20, capacity = 150, node_object = Node('A'),
          remote_node_object = Node('B'), address = '2'),
            Interface(name = 'A-to-B', cost = 20, capacity = 125, node_object = Node('A'),
            remote_node_object = Node('B'), address = '1')],
           [Interface(name = 'B-to-D', cost = 20, capacity = 125, node_object = Node('B'),
           remote_node_object = Node('D'), address = '3')]],
          [[Interface(name = 'A-to-B_2', cost = 20, capacity = 150, node_object = Node('A'),
          remote_node_object = Node('B'), address = '2'),
            Interface(name = 'A-to-B', cost = 20, capacity = 125, node_object = Node('A'),
            remote_node_object = Node('B'), address = '1')],
           [Interface(name = 'B-to-G_2', cost = 10, capacity = 100, node_object = Node('B'),
           remote_node_object = Node('G'), address = '18'),
            Interface(name = 'B-to-G_3', cost = 10, capacity = 100, node_object = Node('B'),
            remote_node_object = Node('G'), address = '28'),
            Interface(name = 'B-to-G', cost = 10, capacity = 100, node_object = Node('B'),
            remote_node_object = Node('G'), address = '8')],
           [Interface(name = 'G-to-D', cost = 10, capacity = 100, node_object = Node('G'),
           remote_node_object = Node('D'), address = '9')]]]}

    :return:


    """



    # This will be a list of path info that has
    normalized_paths = []
    for path in multidigraph_path_info['path']:
        # print("************** path {} *************".format(path))
        interfaces_in_each_hop = [len(hop) for hop in path]
        max_sub_paths = numpy.prod(interfaces_in_each_hop)

        # This is a list of all the created sub-paths
        sub_path_list = []
        for sub_path_number in range(max_sub_paths):
            sub_path_list.append([])

        for hop in path:
            for hop_interface in hop:
                hop_interface_index = hop.index(hop_interface)

                for sub_path_num in range(len(sub_path_list)):
                    if (hop_interface_index + sub_path_num) % len(hop) == 0:
                        sub_path_list[sub_path_num].append(hop_interface)

        normalized_paths.append(sub_path_list)

    return {'cost': multidigraph_path_info['cost'], 'normalized_paths': normalized_paths}

model = Parallel_Link_Model.load_model_file_multidigraph('model_test_topology_multidigraph.csv')
model.validate_model()

a_d = model.get_shortest_path('A', 'D')

pprint(a_d)

# test = normalize_multiple_links(a_d)

##################### def prototyping #####################

normalized_paths = normalize_multidigraph_paths(a_d)

for path in normalized_paths['normalized_paths']:
    print(len(path))
    pprint(path)
    print()





