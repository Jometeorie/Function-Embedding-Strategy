# Function Embedding Strategy
## Introduction
This project includes our function embedding strategy and two comparative algorithms. Algorithm 1 uses the greedy idea to select the nearest server which has unsatisfied functions. Algorithm 2 assumes that the order in which functions are satisfied has been fixed.

We provide fat tree, mesh and tree topologies and allow you to modify the details of the topology.

In most cases, out proposed algorithm can use a shorter distance to complete the demand.

## Examples
The main entrances of fat tree, mesh and tree topologies are in **combine_fat_tree.py, combine_normal_net.py and combine_normal_tree.py** respectively. However, if you want to run these files, you may need to define some hyperparameters. We provide three examples in **run_example.sh**. You can use **bash run_example.sh**.

Below is an explanation of some import hyperparameters.
* --num_of_pod (only in fat tree): The number of pods in fat tree.
* --num_of_nodes (only in mesh and tree): The number of nodes in mesh or tree.
* --degrees (only in mesh and tree): The degree of mesh (min degree) or tree.
*  --times: Number of times to run in this topology.
* --display_graph: True to display the topology by matplotlib.
* --N: Number of function sequences that generated in method 2.
* --load_file: If it is not none, the file will load the topology file rather than randomly generating a topology.
* --save_path: If it is not none, it will save the topology structure in that path.
* --function_need: Number of function needs per demand.

In addition, we provide seven files for you to easily test our proposed method in different topologies.
| File Name | Number of Nodes | Number of functions per demand | Number of functions per server | Total functions | Edges |
| --- | --- | --- | --- | --- | --- |
| 40node-6func.py | 40 | 6 | 3 | 24 | 5-10 |
| 40node-12func.py | 40 | 12 | 3 | 24 | 5-10 |
| 40node-18func.py | 40 | 18 | 3 | 24 | 5-10 |
| 40node-24func.py | 40 | 24 | 3 | 24 | 5-10 |
| 60node-18func.py | 60 | 18 | 3 | 18 | 3-10 |
| 80node-18func.py | 80 | 18 | 3 | 18 | 3-10 |
| 100node-18func.py | 100 | 18 | 3 | 18 | 3-10 |