# -*- coding: utf-8 -*-
import networkx as nx

from src.dataclass import RateCard
from src.enums import DotFileParams, RateCardParams
from src.strategies.strategy import Strategy


class StrategyCardA(Strategy):
    rate_card = RateCard(Cabinet=1000, Trench_m_verge=50, Trench_m_road=100, Chamber=200, Pot=100)

    def calculate_total_cost(self, graph: nx.Graph) -> int:
        total_cost = Strategy.calculate_edges_cost(graph, StrategyCardA.rate_card)

        for node, data in graph.nodes(data=True):
            item = data.get(DotFileParams.TYPE)
            cost = getattr(StrategyCardA.rate_card, item, 0)
            total_cost += cost

        return total_cost
