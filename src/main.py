# -*- coding: utf-8 -*-

import os
import sys
from enum import Enum
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pydot


class DotFileParams(str, Enum):
    LENGTH = "length"
    MATERIAL = "material"
    VERGE = "verge"
    ROAD = "road"
    TYPE = "type"


class RateCardParams(str, Enum):
    CABINET = "Cabinet"
    TRENCH_M_VERGE = "Trench_m_verge"
    TRENCH_M_ROAD = "Trench_m_road"
    CHAMBER = "Chamber"
    POT = "Pot"


def parse_dot_file(file_path: Path) -> nx.Graph:
    G = nx.Graph()

    dot_data = open(file_path, "r").read()
    graph = pydot.graph_from_dot_data(dot_data)[0]

    for node in graph.get_nodes():
        node_name = node.get_name().strip('"')
        node_type = node.get_attributes().get(DotFileParams.TYPE)
        if node_type:
            G.add_node(node_name, type=node_type)

    for edge in graph.get_edges():
        source = edge.get_source().strip('"')
        target = edge.get_destination().strip('"')
        edge_attributes = edge.get_attributes()
        if DotFileParams.LENGTH in edge_attributes:
            edge_attributes[DotFileParams.LENGTH] = int(edge_attributes[DotFileParams.LENGTH])
            G.add_edge(source, target, **edge_attributes)

    # nx.draw(G)
    # plt.show()

    return G


if __name__ == "__main__":
    input_file = os.path.join("src", "reference", "problem.dot")

    try:
        graph = parse_dot_file(input_file)

    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
