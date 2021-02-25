from dataclasses import dataclass



@dataclass
class RealStockPriceDataclass:
    code: str = None
    time: str = None
    now_price: int = None
    yesterday_diff: int = None
    yesterday_diff_percent: float = None
    medo_1_hoga: int = None
    mesu_1_hoga: int = None
    volume: int = None
    volume_sum: int = None
    high_price: int = None
    low_price: int = None
