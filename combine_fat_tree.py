import argparse
from src.Fat_tree import Fat_tree
from src.Process_fat_tree import init_nodes, generate_matrix_by_input
from src.Topology_info import Topo_info
from src.Methods import method_one, method_two, method_three
import numpy as np
import sys
import random
import networkx as nx
import pickle

if __name__ == '__main__':
    '''
    You can run this porject by executing
    python -W ignore combine_fat_tree.py \
        --num_of_pod=6 \
        --times=2 \
        --display_all=True \
        --N=3
    or modify the related parameters.
    '''
    parser = argparse.ArgumentParser(description = 'Describe a fat tree.')
    parser.add_argument('--num_of_pod', type = int, help = 'The number of pods (k)', required = True)
    parser.add_argument('--times', type = int, default = 10, help = 'Number of iters run in the same topology')
    parser.add_argument('--display_graph', default = 'False', choices = ['True', 'False'], 
                        help = 'True to display the graph, false not.')
    parser.add_argument('--display_matrix', default = 'False', choices = ['True', 'False'],
                         help = 'True to display the matrix, false not.')
    parser.add_argument('--display_all', default = 'False', choices = ['True', 'False'], 
                        help = 'True to display all value of the matrix, false to display part of it.')
    parser.add_argument('--display_table', default = 'False', choices = ['True', 'False'], 
                        help = 'True to display the table, false not')
    parser.add_argument('--display_bandwidthm', default = 'False', choices = ['True', 'False'])
    parser.add_argument('--display_distance', default = 'False', choices = ['True', 'False'])
    parser.add_argument('--display_CPU', default = 'False', choices = ['True', 'False'])
    parser.add_argument('--N', type = int, required = True, help = 'Number of sequences to generate')
    parser.add_argument('--load_file', type = str, default = 'None', help = 'Topo info to load')
    parser.add_argument('--save_path', default = 'None', help = 'Path to save the topo file, None not save')
    parser.add_argument('--function_need', type = int, default = 24, 
                        help = 'Number of function need')

    # build the graph of a fat tree
    str_to_bool = {'True': True, 'False': False}

    args = parser.parse_args()
    fat_tree = Fat_tree(args.num_of_pod)
    fat_tree_graph = fat_tree.generate_graph(display_graph = str_to_bool[args.display_graph], edges_func = lambda: 1)

    if str_to_bool[args.display_all]:
        np.set_printoptions(threshold = 1000000)
    else:
        np.set_printoptions(threshold = None)

    topo = Topo_info(fat_tree_graph, 24, 3)
    topo.fat_tree_matrix = fat_tree.convert_graph_to_matrix(display_matrix = str_to_bool[args.display_matrix])
    topo.fat_tree_table = fat_tree.convert_graph_to_table(display_table = str_to_bool[args.display_table])

    topo.bandwidth_matrix = generate_matrix_by_input('bandwidth', topo.fat_tree_matrix, topo.node_list, restrict = [10, 15, 20, 25])
    topo.distance_matrix = generate_matrix_by_input('distance', topo.fat_tree_matrix, topo.node_list)
    if args.load_file != 'None':
        with open(args.load_file, 'rb') as f:
            topo = pickle.loads(f.read())

    if args.save_path != 'None':
        topo.save(args.save_path)

    all_functions = topo.function_need
    for times in range(args.times):
        topo.function_need = random.sample(all_functions, args.function_need)
        # begin_node = input('Please enter the begining node (must be cor servers): ')
        begin_node = 'cor 0'
        # end_node = input('Please enter the ending node (must be cor servers): ')
        end_node = 'cor 0'

        # Find all candidate list of all functions that should be satisfied.
        candidate_dict = dict()
        for function in topo.function_need:
            candidate_dict[function] = []
        for func_info in topo.node_dict.items():
            for satisfied_func in func_info[1]['function']:
                if satisfied_func in topo.function_need:
                    candidate_dict[satisfied_func].append(func_info[0])

        fat_tree_distance1 = method_one(begin_node, end_node, topo)
        fat_tree_distance2 = method_two(begin_node, end_node, candidate_dict, all_functions, topo, args.N)
        fat_tree_distance3 = method_three(begin_node, end_node, candidate_dict, topo)

        print(str(fat_tree_distance1) + '    ' + str(fat_tree_distance2) + '    ' + str(fat_tree_distance3))