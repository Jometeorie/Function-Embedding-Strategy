from src.Fat_tree import Fat_tree
import numpy as np
import random

def init_nodes(node_arr, function_num = 24, num_of_func_each_ser = None): # 3
    '''
    It randomly gives each node a value of CPU and function list.
    It returns a list and a dictionary of the names of the nodes.
    '''
    
    # Generate functions of each servers
    total_func_list = [i + 1 for i in range(function_num)]

    # Report 4
    # function_generate_str = input('Please enter the function list (like \'1, 2, 4\'): ')
    # function_generate_str = '1, 2, 3, 4'
    # total_func_generate_list = function_generate_str.split(', ')
    # total_func_generate_list = list(map(int, total_func_generate_list))
    total_func_generate_list = [i + 1 for i in range(function_num)]

    # function_minCPU_str = input('Please enter the min CPU for each functions: ')
    # function_minCPU_str = '1, 1, 1, 1'
    # function_minCPU_list = function_minCPU_str.split(', ')
    # function_minCPU_list = list(map(float, function_minCPU_list))
    function_minCPU_list = [15 for i in range(function_num)]

    function_minBD_list = [random.random() * 10 + 5 for i in range(function_num)]

    # function_minBD_str = input('Please enter the min bandwidth: ')
    function_minBD_str = '1'
    function_minBD = float(function_minBD_str)

    node_list = list(node_arr._nodes.keys())
    node_dict = {}
    for node in node_list:
        # min_CPU, max_CPU = input("Enter the min and max CPU of " + node + ": ").split(' ')
        # min_CPU = float(min_CPU)
        # max_CPU = float(max_CPU)
        # min_CPU, max_CPU = 1, 3
        # CPU = (max_CPU - min_CPU) * np.random.random() + min_CPU
        CPU_choice = [25, 35, 45, 55]
        CPU = random.choice(CPU_choice)

        node_dict[node] = {'CPU': CPU, 'function': [],}

    servers = []
    for name in node_list:
        if 'ser' in name:
            servers.append(name)
    while True:
        index = 0
        for s in servers:
            if num_of_func_each_ser == None:
                node_dict[s]['function'] = random.sample(total_func_list, random.randint(1, function_num - 1))
            else:
                if num_of_func_each_ser == 1:
                    node_dict[s]['function'] = [total_func_list[index]]
                    index += 1
                else:
                    node_dict[s]['function'] = random.sample(total_func_list, random.randint(num_of_func_each_ser, num_of_func_each_ser))
        # Make sure that all functions can be realized by one of the servers
        has_func_now = []
        for s in servers:
            for f in node_dict[s]['function']:
                if f not in has_func_now:
                    has_func_now.append(f)
        if len(has_func_now) == len(total_func_list):
            break

    func_dict = {}
    for i in range(len(total_func_generate_list)):
        func_dict[total_func_generate_list[i]] = function_minCPU_list[i]

    return node_list, node_dict, total_func_generate_list, function_minCPU_list, function_minBD, func_dict, function_minBD_list

def getNeighbor(node_name, node_list, edge_matrix):
    index = -1
    edge_list = edge_matrix.tolist()

    for i in range(len(node_list)):
        if node_list[i] == node_name:
            index = i
            break
    if index == -1:
        return -1
    else:
        neighbors = []
        for i in range(len(edge_list[index])):
            if edge_list[index][i] != 0:
                neighbors.append(i)
    neighbor_name = []
    for i in neighbors:
        neighbor_name.append(node_list[i])

    return neighbor_name, neighbors

def getNeighborWithEnoughBandwidth(node_name, node_list, bandwidth_matrix, bandwidth_need):
    for i in range(len(node_list)):
        if node_list[i] == node_name:
            node_index = i

    satisfied_list = []
    for i in range(len(bandwidth_matrix.A[node_index])):
        if bandwidth_matrix.A[node_index][i] >= bandwidth_need:
            satisfied_list.append(node_list[i])

    return satisfied_list

def getNeighborWithEnoughComputation(node_name, node_list, node_dict, bandwidth_matrix, CPU_need):
    for i in range(len(node_list)):
        if node_list[i] == node_name:
            node_index = i

    satisfied_list = []
    for i in range(len(bandwidth_matrix.A[node_index])):
        if bandwidth_matrix.A[node_index][i] > 0:
            if node_dict[node_list[i]]['CPU'] >= CPU_need:
                satisfied_list.append(node_list[i])

    return satisfied_list

def getNeighborWithCorrectFunction(node_name, node_list, node_dict, bandwidth_matrix, function_need):
    for i in range(len(node_list)):
        if node_list[i] == node_name:
            node_index = i

    satisfied_list = []
    for i in range(len(bandwidth_matrix.A[node_index])):
        if bandwidth_matrix.A[node_index][i] > 0:
            temp = 1
            for f in function_need:
                if f not in node_dict[node_list[i]]['function']:
                    temp = 0
            if temp == 1:
                satisfied_list.append(node_list[i])

    return satisfied_list

def generate_matrix_by_input(usage, edge_matrix, node_list, min_edge = 5, max_edge = 10, restrict = None):
    '''
    Generate the matrix by input the min and the max of each edge
    usage: choice from 'bandwidth' and 'distance'
    edge_matrix: the matrix of the edges
    node_list: the list which contains the name of each node, and 
    the sequence should be the same as the edge_matrix
    '''
    matrix = edge_matrix.copy()
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] != 0 and i < j:
                # min_edge, max_edge = input("Enter the min and max " + 
                #     usage + " between " + node_list[i] + " and " + 
                #     node_list[j] + ": ").split(' ')
                min_edge = float(min_edge)
                max_edge = float(max_edge)
                edge_value = (max_edge - min_edge) * np.random.random() + min_edge
                if restrict != None:
                    edge_value = random.choice(restrict)
                matrix[i, j] = edge_value
                matrix[j, i] = edge_value

    return matrix