# -*- coding: utf-8 -*-
import os
from pathlib import Path
from typing import List, Tuple

import networkx as nx
import pytest

from main import DotFileParams, RateCardParams, parse_dot_file

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
