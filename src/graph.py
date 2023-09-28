# -*- coding: utf-8 -*-
from pathlib import Path

import networkx as nx
import pydot

from src.enums import DotFileParams, RateCardParams


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

    return G
