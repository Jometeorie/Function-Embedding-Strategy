from src.utils import *
import networkx as nx

def method_one(begin_node, end_node, topo):
    '''
    This is the method that uses the nearest neighbour algorithm.
    It is a kind of greedy algorithm. It always tries to find the 
    nearest node that can satisfy any functions that haven't been
    satisfied.
    '''
    # Store nodes.
    SFP = []
    # Store functions that already satisfied. 
    F_SFP = []
    # Functions that still not satisfied.
    RE_FUNC = topo.function_need.copy()
    SFP.append(begin_node)
    
    total_distance = 0
    iters = 0
    while sorted(F_SFP) != sorted(topo.function_need):
        iters += 1
        dijkstra_distance = Dijkstra_class()
        dijkstra_distance.make_picture(topo.distance_matrix.tolist(), topo.node_list, 
            another_matrix = topo.bandwidth_matrix.tolist(), another_min_restrict = topo.function_minBD)
        dijkstra_dict = dijkstra_distance.dijkstra(SFP[-1])
        dijkstra_list = sorted(dijkstra_dict.items(), key = lambda x: x[1])
        for i in range(len(dijkstra_list)):
            # If the node can satisfied one function that do not be satisfied.
            # Functions that the node can serve.
            change_node = False
            func_by_node = topo.node_dict[dijkstra_list[i][0]]['function']
            temp_cpu = topo.node_dict[dijkstra_list[i][0]]['CPU']
            if len(set(func_by_node).intersection(set(RE_FUNC))) != 0:
                for j in range(len(func_by_node)):
                    if func_by_node[j] in RE_FUNC and temp_cpu >= topo.function_minCPU_list[func_by_node[j]-1] and func_by_node[j] not in F_SFP:
                        change_node = True
                        temp_cpu -= topo.function_minCPU_list[func_by_node[j]-1]
                        F_SFP.append(func_by_node[j])
                        RE_FUNC.remove(func_by_node[j])
                        if dijkstra_list[i][0] not in SFP:
                            SFP.append(dijkstra_list[i][0])
                            total_distance += dijkstra_dict[dijkstra_list[i][0]]
            if change_node:
                break

        if iters > 1000:
            print(-1)
            sys.exit()

    SFP.append(end_node)
    dijkstra_distance = Dijkstra_class()
    dijkstra_distance.make_picture(topo.distance_matrix.tolist(), topo.node_list, 
        another_matrix = topo.bandwidth_matrix.tolist(), another_min_restrict = topo.function_minBD)
    dijkstra_dict = dijkstra_distance.dijkstra(SFP[-2])
    total_distance += dijkstra_dict[SFP[-1]]

    if total_distance < 10**10:
        for node in SFP:
            for i in range(len(topo.node_list)):
                if node == topo.node_list[i]:
                    # print(str(i) + ' ', end = '')
                    pass
        fat_tree_distance1 = total_distance
    else:
        fat_tree_distance1 = -1

    return fat_tree_distance1

def method_two(begin_node, end_node, candidate_dict, all_functions, topo, N):
    '''
    This is the method that uses physical graph to route.
    '''
    # Generate N random sequences of function lists.
    func_sequences = []
    i = 0
    loop_times = 0
    while(i < N):
        loop_times += 1
        random.shuffle(topo.function_need)
        if topo.function_need not in func_sequences or loop_times > 100:
            func_sequences.append(topo.function_need.copy())
            i += 1

    sum_distance = 0
    temp_min_distance = 10**10
    is_success = True
    for i in range(len(func_sequences)):
        physics_graph = generate_physics_graph(begin_node, end_node, func_sequences[i], candidate_dict, topo)
        dijkstra_distance = Dijkstra_class()
        physics_graph_list = nx.to_numpy_matrix(physics_graph).tolist().copy()
        physics_graph_nodes = list(physics_graph.nodes()._nodes.keys()).copy()
        dijkstra_distance.make_picture(physics_graph_list, physics_graph_nodes)
        temp = dijkstra_distance.dijkstra(begin_node + '_begin')[end_node + '_end']
        if temp >= 10 ** 10:
            is_success = False

        sum_distance += temp
        if temp < temp_min_distance:
            temp_min_distance = temp

    if is_success:
        fat_tree_distance2 = sum_distance / len(func_sequences)
    else:
        fat_tree_distance2 = -1
    normal_tree_distance2 = temp_min_distance

    return fat_tree_distance2

def method_three(begin_node, end_node, candidate_dict, topo):
    # Get the candidate list
    candidate_list = []
    for temp in candidate_dict:
        for ser in candidate_dict[temp]:
            if ser not in candidate_list:
                candidate_list.append(ser)

    complete_graph = generate_complete_graph(begin_node, candidate_list, topo)
    T = generate_T(begin_node, end_node, candidate_list, candidate_dict, topo)
    min_tree = prim(complete_graph, T, topo)

    nx.draw(min_tree, with_labels = False)

    dfs_list = list(nx.dfs_tree(min_tree, source = begin_node))

    dfs_list2 = dfs(nx.dfs_successors(min_tree, source = begin_node), begin_node, topo)

    total_distance = 0
    for i in range(len(dfs_list) - 1):
        total_distance += calculate_min_distance(dfs_list[i], dfs_list[i+1], topo)
    total_distance += calculate_min_distance(dfs_list[-1], end_node, topo)
    if total_distance > 10 ** 10:
        total_distance = -1
    fat_tree_distance3 = total_distance

    return fat_tree_distance3