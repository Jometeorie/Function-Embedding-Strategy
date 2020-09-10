from src.Process_fat_tree import *
from src.utils import *
import pickle

class Topo_info:
    '''
    It is a class that store some infomation about the topology.
    bandwidth_matrix: bandwidth matrix of the topology.
    distance_matrix: distance matrix of the topology.
    node list: the index of each node.
    node_dict: It is like node_dict[node] = {'CPU': CPU, 'function': [],}, 
               which contains CPU and satisfied function of each node.
    function_need: which functions each demands need to be satisfied.
    function_minCPU_list: The minCPU that each function need.
    function_minBD: The minBD that each function need.
    func_dict: Same as function_minCPU_list.
    function_minBD_list: Same as function_minBD.
    '''
    def __init__(self, graph, function_num, num_of_func_each_ser, is_load = False, filename = None):
        self.node_list, self.node_dict, self.function_need, self.function_minCPU_list, \
        self.function_minBD, self.func_dict, self.function_minBD_list = \
        init_nodes(graph.node(), 24, 3)

    def save(self, filename):
        out_file = open(filename, 'wb')
        s = pickle.dumps(self)
        out_file.write(s)
        out_file.close()