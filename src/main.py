# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from pathlib import Path

from src.context import Context
from src.graph import parse_dot_file
from src.strategies.strategy import Strategy
from src.strategies.strategy_a import StrategyCardA
from src.strategies.strategy_b import StrategyCardB

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
