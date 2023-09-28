# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

import networkx as nx

from src.dataclass import RateCard
from src.enums import DotFileParams, RateCardParams


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
