from dataclasses import dataclass


@dataclass
class Ticker:
    symbol: str
    high: float
    low: float
    prev_quarter_average: float
