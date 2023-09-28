# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Optional


@dataclass
class RateCard:
    Cabinet: int
    Trench_m_verge: int
    Trench_m_road: int
    Chamber: int
    Pot: Optional[int] = None
