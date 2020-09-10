import networkx as nx
import random

'''
This file contains several functions that the three methods may need.
'''

def calculate_min_distance(begin_node, end_node, topo, f = None):
    '''
    This is the method that uses to calculate the shorteset length from the
    begin node to the end node under the restriction of bandwidth_matrix and 
    distance matrix.
    '''
    global node_list
    dijkstra_distance = Dijkstra_class()
    dijkstra_distance.make_picture(topo.distance_matrix.tolist(), topo.node_list, 
        another_matrix = topo.bandwidth_matrix.tolist(), another_min_restrict = topo.function_minBD)
    if not f:
        return dijkstra_distance.dijkstra(begin_node)[end_node]
    else:
        return dijkstra_distance.dijkstra(begin_node, f)

def generate_physics_graph(begin_node, end_node, func_sequence, candidate_dict, topo):
    '''
    This is the method that uses to generate the physics graph with the begin 
    node and the end node under the function_seqence 
    '''
    topo_net = nx.Graph()

    # Add all nodes to the physics graph.
    topo_net.add_node(begin_node + '_begin')
    topo_net.add_node(end_node + '_end')
    for function in func_sequence:
        for satisfied_server in candidate_dict[function]:
            topo_net.add_node('Function' + str(function) + '_' + satisfied_server)

    nodes = topo_net.node()

    # Add all edges to the physics
    for node in nodes:
        if 'Function' + str(func_sequence[0]) == node.split('_')[0]:
            temp_distance = calculate_min_distance(begin_node, node.split('_')[1], topo)
            # Distinguish from the node itself
            if temp_distance == 0:
                temp_distance = 0.000000000001
            topo_net.add_edge(begin_node + '_begin', node, weight = temp_distance)
        if 'Function' + str(func_sequence[-1]) == node.split('_')[0]:
            temp_distance = calculate_min_distance(node.split('_')[1], end_node, topo)
            # Distinguish from the node itself
            if temp_distance == 0:
                temp_distance = 0.000000000001
            topo_net.add_edge(node, end_node + '_end', weight = temp_distance)
        for i in range(0, len(func_sequence) - 1):
            if 'Function' + str(func_sequence[i]) == node.split('_')[0]:
                for node2 in nodes:
                    if 'Function' + str(func_sequence[i+1]) == node2.split('_')[0]:
                        temp_distance = calculate_min_distance(node.split('_')[1], node2.split('_')[1], topo)
                        # Distinguish from the node itself
                        if temp_distance == 0:
                            temp_distance = 0.000000000001
                        topo_net.add_edge(node, node2, weight = temp_distance)

    return topo_net

def generate_complete_graph(begin_node, candidate_list, topo):
    topo_net = nx.Graph()

    # Add all nodes to the physics graph.
    topo_net.add_node(begin_node)
    for node in candidate_list:
        if begin_node != node:
            topo_net.add_node(node)

    nodes = topo_net.node()
    nodes_list = list(nodes._nodes.keys())

    for i in range(len(nodes_list)):
        for j in range(i + 1, len(nodes_list)):
            temp_distance = calculate_min_distance(nodes_list[i], nodes_list[j], topo)
            # Distinguish from the node itself
            if temp_distance == 0:
                temp_distance = 0.000000000001
            topo_net.add_edge(nodes_list[i], nodes_list[j], weight = temp_distance)

    return topo_net

def generate_T(begin_node, end_node, candidate_list, candidate_dict, topo):
    T = [begin_node]
    function_need = list(candidate_dict)
    servers = candidate_list.copy()

    while function_need:
        if T == [begin_node]:
            T.append(get_first_max_impact_factor(begin_node, end_node, servers, candidate_dict, topo))
        else:
            T.append(get_max_impact_factor(T, servers, candidate_dict, topo))
        servers.remove(T[-1])
        candidate_dict_copy = candidate_dict.copy()
        temp_cpu = topo.node_dict[T[-1]]['CPU']
        for func in candidate_dict_copy:
            # Delete the function that already be satisfied:
            if list(set(candidate_dict[func]).intersection(set(T))) and temp_cpu >= topo.function_minCPU_list[func-1]:
                candidate_dict.pop(func)
                function_need.remove(func)
                temp_cpu -= topo.function_minCPU_list[func-1]

        if len(T) > 1:
            _, path = calculate_min_distance(T[-2], T[-1], topo, T[-1])
            if T[-1] in path:
                path.remove(T[-1])
            if T[-2] in path:
                path.remove(T[-2])
            candidate_dict_copy = candidate_dict.copy()
            for func in candidate_dict_copy:
                if list(set(candidate_dict[func]).intersection(set(path))):
                    candidate_dict.pop(func)
                    function_need.remove(func)

    return T

def get_first_max_impact_factor(begin_node, end_node, candidate_list, candidate_dict, topo):
    # Get the max impact factor when initialize.
    impact_factor_dict = dict()
    max_impact_factor = -1
    for ser in candidate_list:
        len_of_SFs = 0
        for func in candidate_dict:
            if ser in candidate_dict[func]:
                len_of_SFs += 1
        # min_distance = 10 ** 10
        min_distance = calculate_min_distance(ser, begin_node, topo) + \
        calculate_min_distance(ser, end_node, topo)
        # Distinguish from the node itself
        if min_distance == 0:
            min_distance = 0.000000000001
        impact_factor = min(len_of_SFs, topo.node_dict[ser]['CPU'] / 15) / min_distance
        if impact_factor > max_impact_factor:
            s = ser
            max_impact_factor = impact_factor
    
    return s

def get_max_impact_factor(T, candidate_list, candidate_dict, topo):
    # Get the max impact factor after the first time.
    impact_factor_dict = dict()
    max_impact_factor = -1
    for ser in candidate_list:
        if ser not in T:
            len_of_SFs = 0
            for func in candidate_dict:
                if ser in candidate_dict[func]:
                    len_of_SFs += 1
            min_distance = 10 ** 10
            for ser2 in T:
                temp_distance = calculate_min_distance(ser, ser2, topo)
                # Distinguish from the node itself
                if temp_distance == 0:
                    temp_distance = 0.000000000001
                min_distance = min(min_distance, temp_distance)
            impact_factor = min(len_of_SFs, topo.node_dict[ser]['CPU'] / 15) / min_distance
            if impact_factor > max_impact_factor:
                s = ser
                max_impact_factor = impact_factor

    return s

def prim(complete_graph, T, topo):
    # Use the Prim method to generate the minimum spanning tree.
    min_tree = nx.Graph()
    # Add all nodes to the min_tree.
    for node in T:
        min_tree.add_node(node)

    candidate_nodes = T[1:]
    finished_nodes = [T[0]]
    while sorted(finished_nodes) != sorted(T):
        dijkstra_distance = Dijkstra_class()
        complete_graph_list = nx.to_numpy_matrix(complete_graph).tolist().copy()
        complete_graph_nodes = list(complete_graph.nodes()._nodes.keys()).copy()
        dijkstra_distance.make_picture(complete_graph_list, complete_graph_nodes)

        min_distance = 10 ** 10
        for c in candidate_nodes:
            for f in finished_nodes:
                temp = dijkstra_distance.dijkstra(c)[f]
                if temp <= min_distance:
                    min_distance = temp
                    next_node = c
                    node_in_finished = f

        candidate_nodes.remove(next_node)
        finished_nodes.append(next_node)
        min_tree.add_edge(node_in_finished, next_node, weight = min_distance)

    return min_tree

def dfs(adj, start, topo):
    '''
    Use DFS to traverse the whole graph.
    '''
    visited = set()
    stack = [[start, 0]]
    all_list = [start]
    change_root = False
    while stack:
        (v, next_child_idx) = stack[-1]
        if (v not in adj) or (next_child_idx >= len(adj[v])):
            change_root = True
            last_node = v
            stack.pop()
            continue
        if change_root and len(stack) >= 2:
            min_distance = 10 ** 10
            for i in range(next_child_idx, len(adj[v])):
                temp_distance = calculate_min_distance(last_node, adj[v][i], topo)
                if temp_distance < min_distance:
                    min_distance = temp_distance
                    exchange_node = adj[v][i]
                    adj[v][i] = adj[v][next_child_idx]
                    adj[v][next_child_idx] = exchange_node
                    change_root = False

        next_child = adj[v][next_child_idx]
        stack[-1][1] += 1
        if next_child in visited:
            continue

        all_list.append(next_child)
        visited.add(next_child)
        stack.append([next_child, 0])

    return all_list

class Dijkstra_class(object):
    '''
    The class to find the shortest path by Dijkstra
    '''
    def __init__(self):
        self.storage_matrix = []
        self.node_list = []

    def make_picture(self, matrix, _nodes, min_restrict = -1, max_restrict = 10 ** 10, 
        another_matrix = [], another_min_restrict = -1, another_max_restrict = 10 ** 10):
        '''
        '''
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if another_matrix:
                    if another_matrix[i][j] < another_min_restrict or another_matrix[i][j] > another_max_restrict:
                        matrix[i][j] = 10 ** 10
                if matrix[i][j] == 0 or matrix[i][j] < min_restrict or matrix[i][j] > max_restrict:
                    matrix[i][j] = 10 ** 10
        self.node_list = _nodes
        for m in matrix:
            self.storage_matrix.append(m)
        # print(matrix)

    def dict_min_by_value(self, this_dict):
        '''
        字典里值最小的键
        '''
        min_value = 10 ** 10 + 1
        max_value = -1
        key = ''
        for get_item in this_dict.items():
            if get_item[-1] < min_value:
                min_value = get_item[-1]
                key = get_item[0]
        return key

    def get_node_index(self, node):
        '''
        Find the subscript of min_key in the list node.
        '''
        for i in range(len(self.node_list)):
            if node == self.node_list[i]:
                return i

    def dijkstra(self, start_node, f = None):
        # The node and distance of the shortest path have been found
        over_node = {start_node: 0}  
        # The node of the shortest path to be found and the distance from the starting node
        found_node = dict()  
        path = {}
        path[start_node] = []
        i = self.get_node_index(start_node)
        for j in range(len(self.storage_matrix[i])):
            if j != i:
                found_node[self.node_list[j]] = self.storage_matrix[i][j]
                if found_node[self.node_list[j]] < 10 ** 10:
                    path[self.node_list[j]] = [self.node_list[j]]
                    # path[self.node_list[j]] = []

        while found_node:
            min_key = self.dict_min_by_value(found_node)
            over_node[min_key] = found_node[min_key]
            found_node.pop(min_key)
            i = self.get_node_index(min_key)
            for get_node in found_node.items():
                j = self.get_node_index(get_node[0])
                if get_node[-1] > over_node[min_key] + self.storage_matrix[i][j]:
                    found_node[get_node[0]] = over_node[min_key] + self.storage_matrix[i][j]
                    try:
                        _ = path[get_node[0]]
                    except Exception:
                        path[get_node[0]] = []
                    path[get_node[0]] = path[min_key].copy()
                    path[get_node[0]].append(min_key)

        for min_key in over_node.keys():
            if over_node[min_key] >= 10 ** 10:
                over_node[min_key] = 10 ** 10

        if f:
            return over_node, path[f]

        else:
            return over_node