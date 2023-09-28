# -*- coding: utf-8 -*-
from pathlib import Path

import networkx as nx
import pytest

from src.dataclass import RateCard
from src.enums import DotFileParams, RateCardParams
from src.main import Context, parse_dot_file
from src.strategy import StrategyCardA, StrategyCardB


@pytest.fixture
def sample_graph() -> nx.Graph:
    # Create a sample graph for testing
    G = nx.Graph()
    G.add_node("A", type=RateCardParams.CABINET)
    G.add_node("B", type=RateCardParams.POT)
    G.add_node("F", type=RateCardParams.CHAMBER)
    G.add_edge("A", "F", length=0, material=DotFileParams.VERGE)
    G.add_edge("B", "F", length=10, material=DotFileParams.VERGE)
    return G


@pytest.fixture
def shortened_dot_file_contents() -> str:
    return """strict graph "" {
        A [type=Cabinet];
        B [type=Pot];
        F [type=Chamber];
        A -- F  [length=0, material=verge];
        B -- F  [length=10, material=verge];
    }
    """


@pytest.fixture
def dot_file_contents() -> str:
    return """strict graph "" {
    A [type=Cabinet];
    B [type=Pot];
    C [type=Pot];
    D [type=Pot];
    E [type=Pot];
    F [type=Chamber];
    G [type=Chamber];
    H [type=Chamber];
    I [type=Chamber];
    A -- F  [length=50, material=verge];
    B -- F  [length=20, material=verge];
    C -- G  [length=50, material=road];
    D -- H  [length=100, material=road];
    E -- H  [length=50, material=verge];
    F -- G  [length=100, material=verge];
    G -- I  [length=40, material=road];
    H -- G  [length=100, material=road];
    }
    """


def test_calculate_edges_cost_strategy_A_B(sample_graph: nx.Graph) -> None:
    rate_card = RateCard(Cabinet=1000, Trench_m_verge=50, Trench_m_road=100, Chamber=200, Pot=100)
    strategyA = StrategyCardA()

    edge_costA = strategyA.calculate_edges_cost(sample_graph, rate_card)

    strategyB = StrategyCardB()

    edge_costB = strategyB.calculate_edges_cost(sample_graph, rate_card)

    assert edge_costA == 500
    assert edge_costA == edge_costB


def test_shortest_path_length_to_nearest_cabinet() -> None:
    graph = nx.Graph()
    graph.add_node("A", type=RateCardParams.CABINET)
    graph.add_node("B", type=RateCardParams.POT)
    graph.add_node("C", type=RateCardParams.CABINET)
    graph.add_node("D", type=RateCardParams.POT)
    graph.add_edge("A", "B", LENGTH=3)
    graph.add_edge("B", "C", LENGTH=2)
    graph.add_edge("C", "D", LENGTH=1)

    strategyB = StrategyCardB()

    shortest_path_length = strategyB.shortest_path_length_to_nearest_cabinet(graph, "A")
    assert shortest_path_length == 0

    shortest_path_length = strategyB.shortest_path_length_to_nearest_cabinet(graph, "B")
    assert shortest_path_length == 1

    shortest_path_length = strategyB.shortest_path_length_to_nearest_cabinet(graph, "D")
    assert shortest_path_length == 1


def test_calculate_total_cost_strategy_A(sample_graph: nx.Graph) -> None:
    strategy = StrategyCardA()
    context = Context(strategy)

    total_cost = context.execute_computation(sample_graph)

    assert total_cost == 1800


def test_calculate_total_cost_strategy_B(sample_graph: nx.Graph) -> None:
    strategy = StrategyCardB()
    context = Context(strategy)

    total_cost = context.execute_computation(sample_graph)

    assert total_cost == 2000


def test_calculate_ref_problem_strategy_A(tmp_path: Path, dot_file_contents: str) -> None:
    dot_file = tmp_path / "test_dot_file.dot"
    dot_file.write_text(dot_file_contents)

    G = parse_dot_file(dot_file)

    context = Context(StrategyCardA())
    assert context.execute_computation(G) == 42200


def test_calculate_ref_problem_strategy_B(tmp_path: Path, dot_file_contents: str) -> None:
    dot_file = tmp_path / "test_dot_file.dot"
    dot_file.write_text(dot_file_contents)

    G = parse_dot_file(dot_file)

    context = Context(StrategyCardB())
    assert context.execute_computation(G) == 52400


def test_parse_dot_file_short_example(tmp_path: Path, shortened_dot_file_contents: str) -> None:
    dot_file = tmp_path / "test_dot_file.dot"
    dot_file.write_text(shortened_dot_file_contents)

    G = parse_dot_file(dot_file)

    assert len(G.nodes()) == 3
    assert G.nodes["A"]["type"] == RateCardParams.CABINET
    assert G.nodes["B"]["type"] == RateCardParams.POT
    assert G.nodes["F"]["type"] == RateCardParams.CHAMBER

    assert len(G.edges()) == 2

    assert G.edges[("A", "F")]["length"] == 0
    assert G.edges[("A", "F")]["material"] == DotFileParams.VERGE

    assert G.edges[("B", "F")]["length"] == 10
    assert G.edges[("B", "F")]["material"] == DotFileParams.VERGE


def test_parse_dot_file(tmp_path: Path, dot_file_contents: str) -> None:
    dot_file = tmp_path / "test_dot_file.dot"
    dot_file.write_text(dot_file_contents)

    G = parse_dot_file(dot_file)

    assert len(G.nodes()) == 9
    assert G.nodes["A"]["type"] == RateCardParams.CABINET
    assert G.nodes["B"]["type"] == RateCardParams.POT
    assert G.nodes["C"]["type"] == RateCardParams.POT
    assert G.nodes["D"]["type"] == RateCardParams.POT
    assert G.nodes["E"]["type"] == RateCardParams.POT
    assert G.nodes["F"]["type"] == RateCardParams.CHAMBER
    assert G.nodes["G"]["type"] == RateCardParams.CHAMBER
    assert G.nodes["H"]["type"] == RateCardParams.CHAMBER
    assert G.nodes["I"]["type"] == RateCardParams.CHAMBER

    assert len(G.edges()) == 8

    assert G.edges[("A", "F")]["length"] == 50
    assert G.edges[("A", "F")]["material"] == DotFileParams.VERGE

    assert G.edges[("B", "F")]["length"] == 20
    assert G.edges[("B", "F")]["material"] == DotFileParams.VERGE

    assert G.edges[("C", "G")]["length"] == 50
    assert G.edges[("C", "G")]["material"] == DotFileParams.ROAD

    assert G.edges[("D", "H")]["length"] == 100
    assert G.edges[("D", "H")]["material"] == DotFileParams.ROAD

    assert G.edges[("E", "H")]["length"] == 50
    assert G.edges[("E", "H")]["material"] == DotFileParams.VERGE

    assert G.edges[("F", "G")]["length"] == 100
    assert G.edges[("F", "G")]["material"] == DotFileParams.VERGE

    assert G.edges[("G", "I")]["length"] == 40
    assert G.edges[("G", "I")]["material"] == DotFileParams.ROAD

    assert G.edges[("H", "G")]["length"] == 100
    assert G.edges[("H", "G")]["material"] == DotFileParams.ROAD


if __name__ == "__main__":
    pytest.main()
