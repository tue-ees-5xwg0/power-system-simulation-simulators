import json
import time
import copy
from typing import Dict
from IPython.display import display
import pprint
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import networkx as nx
import matplotlib.pyplot as plt
from prettytable import PrettyTable 
from power_grid_model import CalculationMethod, CalculationType, PowerGridModel, initialize_array
from power_grid_model.utils import json_deserialize, json_serialize
from power_grid_model.validation import assert_valid_batch_data, assert_valid_input_data
from power_system_simulation.graph_processing import GraphProcessor as gp

#################################################################
# open all input data (input data, active pprof, reactive pprof)#
#################################################################

with open("C:/Users/carme/OneDrive/Desktop/Q4/Power_system_computation_and_simulation/assignment_3/big_network/input/input_network_data.json") as fp:
    input_data = json_deserialize(fp.read())
assert_valid_input_data(input_data=input_data, calculation_type=CalculationType.power_flow)
with open("C:/Users/carme/OneDrive/Desktop/Q4/Power_system_computation_and_simulation/assignment_3/big_network/input/meta_data.json", 'r') as file:
    meta_data = json.load(file)

##################################
# establish input data for graph #
##################################


########### ORIGINAL DATA is extracted for "graph_processing.py" call
vertex_ids = input_data['node']['id']
edge_ids_init = pd.DataFrame(input_data['line']['id']).to_numpy()
edge_vertex_id_pairs_init = list(zip(input_data['line']['from_node'], input_data['line']['to_node']))
edge_enabled_init = (input_data['line']['from_status'] == 1) & (input_data['line']['to_status'] == 1)
source_id = input_data['node'][0][0] # or meta_data

########### MODIFIED DATA FOR TRANSFORMER AS EDGE

# Transformer must be added as edge -> add one more edge_vertex_id_pair: (0,1)
# one more edge enabled (True) and one more edge id (tranformer id). They can all be appended at the end of the list(s)
vertex_ids = vertex_ids
edge_ids = np.append(edge_ids_init, input_data['transformer']['id'])
edge_vertex_id_pairs = (edge_vertex_id_pairs_init) + [(source_id,meta_data['lv_busbar'])]
edge_enabled = np.append(edge_enabled_init,[True])
source_id = source_id

############################
# call GraphProcessing.py  #
############################
G = gp(vertex_ids = vertex_ids, edge_ids= edge_ids, edge_vertex_id_pairs= edge_vertex_id_pairs, edge_enabled= edge_enabled, source_vertex_id= source_id)

pos = nx.spring_layout(G.graph)
nx.draw_planar(G.graph, node_size=5) 