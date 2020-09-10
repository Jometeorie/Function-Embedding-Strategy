import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

class Normal_tree:
    '''
    Implement of a normal net
    k: num of nodes
    degree: num of sons each node has
    '''

    def __init__(self, k, degree = None):
        self.node = k
        self.degree = degree
        self.index = 1

        self.topo_net = nx.Graph()
        self.matrix = []

    def generate_graph(self, display_graph = False, edges_func = lambda: 1):
        '''
        Randomly generate the graph of a normal tree
        if display_graph == True, then it will set the graph of the fat net visiable.
        edges_func: The function to generate the value of the edges
        This function will return a class of the graph.
        '''
        topo_net = self.topo_net
        node_size = 50

        # Generate trees by BFS
        topo_net.add_node('ser 1')
        self.generate_son('ser 1', self.degree)

        topo_net.name = 'simple normal net'

        if display_graph == True:
            nx.draw(self.topo_net, with_labels = False, node_size = node_size)
            plt.show()

        # self.topo_net = topo_net

        return topo_net

    def generate_son(self, node_name, degree):
        '''
        Generate trees by BFS
        '''
        topo_net = self.topo_net
        if degree == None:
            pass

        else:
            for i in range(degree):
                topo_net.add_node('ser ' + str(self.index))
                topo_net.add_edge(node_name, 'ser ' + str(self.index))
                self.index += 1
                if self.index > self.node:
                    return
            self.generate_son('ser ' + str(self.index-1), degree)

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