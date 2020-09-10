from src.Normal_net import Normal_net
from src.Process_fat_tree import init_nodes, generate_matrix_by_input
from src.Topology_info import Topo_info
from src.Methods import method_one, method_two, method_three
import sys
import random
import networkx as nx
import pickle

if __name__ == '__main__':
    '''
    You can run this porject by executing
    python 100node-18func.py
    '''
    normal_net = Normal_net(80, 4)
    normal_net_graph = normal_net.generate_graph(edges_func = lambda: 1)

    topo = Topo_info(normal_net_graph, 24, 3)

    topo.normal_net_matrix = normal_net.convert_graph_to_matrix()
    topo.normal_net_table = normal_net.convert_graph_to_table()

    topo.bandwidth_matrix = generate_matrix_by_input('bandwidth', topo.normal_net_matrix, topo.node_list, restrict = [10, 15, 20, 25])
    topo.distance_matrix = generate_matrix_by_input('distance', topo.normal_net_matrix, topo.node_list)
    with open('Topo/100nodes_3_10edge.pkl', 'rb') as f:
        topo = pickle.loads(f.read())

    all_functions = topo.function_need
    for times in range(10000):
        # topo.function_need = random.sample(all_functions, random.randint(10, 20))
        topo.function_need = random.sample(all_functions, 12)
        # begin_node = input('Please enter the begining node (must be cor servers): ')
        begin_node = 'ser ' + str(random.randint(0, 39))
        # end_node = input('Please enter the ending node (must be cor servers): ')
        end_node = 'ser ' + str(random.randint(0, 39))

        # Find all candidate list of all functions that should be satisfied.
        candidate_dict = dict()
        for function in topo.function_need:
            candidate_dict[function] = []
        for func_info in topo.node_dict.items():
            for satisfied_func in func_info[1]['function']:
                if satisfied_func in topo.function_need:
                    candidate_dict[satisfied_func].append(func_info[0])

        # fat_tree_distance1 = method_one(begin_node, end_node, topo)
        # fat_tree_distance2 = method_two(begin_node, end_node, candidate_dict, all_functions, topo, 3)
        fat_tree_distance3 = method_three(begin_node, end_node, candidate_dict, topo)

        # print(str(fat_tree_distance1) + '    ' + str(fat_tree_distance2) + '    ' + str(fat_tree_distance3))
        print(fat_tree_distance3)