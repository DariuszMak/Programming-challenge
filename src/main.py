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
    # Prompt the user for the input filename
    input_filename = input("Enter the input filename: ")

    # Create a Path object using the input filename
    input_file = Path("src", "reference", input_filename)

    if not input_file.exists():
        print("File not found:", input_filename)
        sys.exit(1)

    try:
        graph = parse_dot_file(input_file)

        context = Context(StrategyCardA())
        print(f"Cost using Rate Card A: £{context.execute_computation(graph)}")

        context.strategy = StrategyCardB()
        print(f"Cost using Rate Card B: £{context.execute_computation(graph)}")
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
