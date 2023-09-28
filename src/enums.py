# -*- coding: utf-8 -*-
from enum import Enum


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
