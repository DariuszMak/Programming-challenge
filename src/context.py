# -*- coding: utf-8 -*-
import networkx as nx

from src.strategy import Strategy


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
