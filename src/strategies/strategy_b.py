# -*- coding: utf-8 -*-
import networkx as nx

from src.dataclass import RateCard
from src.enums import DotFileParams, RateCardParams
from src.strategies.strategy import Strategy


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
