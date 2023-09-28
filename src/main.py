# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import re
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

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


@dataclass
class RateCard:
    Cabinet: int
    Trench_m_verge: int
    Trench_m_road: int
    Chamber: int
    Pot: Optional[int] = None


class Context:
    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def execute_computation(self, graph: nx.Graph) -> int:
        result = self._strategy.calculate_total_cost(graph)
        return result


class Strategy(ABC):
    @staticmethod
    def calculate_edges_cost(graph: nx.Graph, rate_card: RateCard) -> int:
        edge_cost = 0
        for source, target, data in graph.edges(data=True):
            length = data[DotFileParams.LENGTH]
            material = data[DotFileParams.MATERIAL]
            if material == DotFileParams.VERGE:
                trench_cost = getattr(rate_card, RateCardParams.TRENCH_M_VERGE, 0)
            elif material == DotFileParams.ROAD:
                trench_cost = getattr(rate_card, RateCardParams.TRENCH_M_ROAD, 0)
            else:
                trench_cost = 0
            edge_cost += trench_cost * length
        return edge_cost

    @abstractmethod
    def calculate_total_cost(self, graph: nx.Graph) -> int:
        pass


class StrategyCardA(Strategy):
    rate_card = RateCard(Cabinet=1000, Trench_m_verge=50, Trench_m_road=100, Chamber=200, Pot=100)

    def calculate_total_cost(self, graph: nx.Graph) -> int:
        total_cost = Strategy.calculate_edges_cost(graph, StrategyCardA.rate_card)

        for node, data in graph.nodes(data=True):
            item = data.get(DotFileParams.TYPE)
            cost = getattr(StrategyCardA.rate_card, item, 0)
            total_cost += cost

        return total_cost


class StrategyCardB(Strategy):
    rate_card = RateCard(Cabinet=1200, Trench_m_verge=40, Trench_m_road=80, Chamber=200)

    def shortest_path_length_to_nearest_cabinet(self, graph: nx.Graph, source_node: str) -> int:
        shortest_path_length = float("inf")

        for node in graph.nodes():
            if graph.nodes[node][DotFileParams.TYPE] == RateCardParams.CABINET:
                length = nx.shortest_path_length(graph, source=source_node, target=node, weight=DotFileParams.LENGTH)
                if length < shortest_path_length:
                    shortest_path_length = length

        return int(shortest_path_length)

    def calculate_total_cost(self, graph: nx.Graph) -> int:
        total_cost = Strategy.calculate_edges_cost(graph, StrategyCardB.rate_card)

        for node, data in graph.nodes(data=True):
            item = data.get(DotFileParams.TYPE)
            if item == RateCardParams.POT:
                length_to_cabinet = self.shortest_path_length_to_nearest_cabinet(graph, node)
                cost = 20 * length_to_cabinet
            else:
                cost = getattr(StrategyCardB.rate_card, item, 0)
            total_cost += cost

        return total_cost


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


if __name__ == "__main__":
    input_file = Path("src", "reference", "problem.dot")

    try:
        graph = parse_dot_file(input_file)

        context = Context(StrategyCardA())
        print(f"Cost using Rate Card A: £{context.execute_computation(graph)}")

        context.strategy = StrategyCardB()
        print(f"Cost using Rate Card B: £{context.execute_computation(graph)}")
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
