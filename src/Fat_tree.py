import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class Fat_tree:
    """
    Implement of a fat tree
    k: number of pods
    """

    def __init__(self, k):
        self.num_of_pods = k
        self.servers_per_pod = (k/2) ** 2
        self.num_of_aggregation_switches = int(k/2)
        self.num_of_edge_switches = int(k/2)
        self.services_per_edge_switch = int(k/2)
        self.num_of_core_services = int((k/2) ** 2)

        self.topo_net = nx.Graph()
        self.matrix = []

    def generate_graph(self, display_graph = False, edges_func = lambda: 1):
        '''
        Generate the graph of the fat tree
        if display_graph == True, then it will set the graph of the fat tree visiable.
        edges_func: The function to generate the value of the edges
        However, it is not suggested to set display_graph = True when k > 10.
        This function will return a class of the graph.
        '''
        topo_net = self.topo_net
        node_size = 50
        node_colors = []

        for i in range(self.num_of_core_services):
            # Add core services
            topo_net.add_node('cor ' + str(i))
            node_colors.append(0)

        for i in range(self.num_of_pods):
            for j in range(self.num_of_edge_switches):
                # Add edge switches.
                # i: pod num
                # j: switch num
                topo_net.add_node('edg ' + str(i) + ' ' + str(j))
                node_colors.append(1)
                # Add aggregation switches.
                topo_net.add_node('agg ' + str(i) + ' ' + str(j))
                node_colors.append(2)
                for t in range(self.services_per_edge_switch):
                    # Add services connected to edge switches.
                    topo_net.add_node('ser ' + str(i) + ' ' + str(j) + ' ' + str(t))
                    node_colors.append(3)
                    # Connect services to edge switches.
                    topo_net.add_edge('ser ' + str(i) + ' ' + str(j) + ' ' + str(t), 
                        'edg ' + str(i) + ' ' + str(j), weight = edges_func())

        for i in range(self.num_of_pods):
            for j in range(self.num_of_aggregation_switches):
                for t in range(self.num_of_edge_switches):
                    # Connect aggregation switches to edge switches
                    topo_net.add_edge('agg ' + str(i) + ' ' + str(j), 'edg ' + str(i) + ' ' +str(t), weight = edges_func())

        num_of_edges_in_cor_and_agg = self.num_of_core_services // self.num_of_aggregation_switches
        for i in range(self.num_of_pods):
            for j in range(self.num_of_aggregation_switches):
                for t in range(num_of_edges_in_cor_and_agg):
                    # Connect aggregation switches to core services
                    topo_net.add_edge('agg ' + str(i) + ' ' + str(j), 
                        'cor ' + str(j*num_of_edges_in_cor_and_agg + t), weight = edges_func())

        topo_net.name = 'simple fat tree'

        if display_graph == True:
            nx.draw(self.topo_net, with_labels = False, node_color = node_colors, node_size = node_size)
            plt.show()

        self.topo_net = topo_net
        
        return topo_net

    def convert_graph_to_matrix(self, display_matrix = False):
        '''
        Convert the graph to a matrix.
        If display_matrix == True, it will print the value of the matrix.
        If display_all == True, it will print all the value of the matrix.
        Else, it may print part of it.
        '''
        self.matrix = nx.to_numpy_matrix(self.topo_net)
        if display_matrix == True:
            print(self.matrix)

        return self.matrix

    def generate_matrix(self, edges_func = lambda: np.random.normal(loc = 100, scale = 20), display_matrix = False):
        '''
        Generate matrix such as bandwidth matrix or distance matrix.
        edges_func: function to generate the value of each edges
        '''
        # deep copy the oringin edges matrix in case of changing the original value
        edges_matrix = self.convert_graph_to_matrix(display_matrix = False).copy()
        for i in range(edges_matrix.shape[0]):
            for j in range(edges_matrix.shape[1]):
            	# print(edges_matrix[1][0])
                if edges_matrix[i, j] != 0:
                    edges_matrix[i, j] = edges_func()

        if display_matrix == True:
            print(edges_matrix)

        return edges_matrix

    
    def convert_graph_to_table(self, display_table = False):
        '''
        Convert the graph to a table
        If display_table == True, it will print the value of the table.
        '''
        edge_info = self.topo_net.edges()
        edge_list = list(edge_info)
        tables = {}
        for i in range(len(edge_list)):
            tables[edge_list[i][0]] = []
            tables[edge_list[i][1]] = []
        for i in range(len(edge_list)):
            tables[edge_list[i][0]].append(edge_list[i][1])
            tables[edge_list[i][1]].append(edge_list[i][0])
            
        if display_table == True:
            sorted_tables = sorted(tables.keys())
            for table in sorted_tables:
                print(table + '  ->  ', end = "")
                for i in range(len(tables[table])):
                    if i == len(tables[table]) - 1:
                        print(tables[table][i])
                    else:
                        print(tables[table][i] + '  ->  ', end = "")
        return tables