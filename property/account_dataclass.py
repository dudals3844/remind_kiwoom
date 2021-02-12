from dataclasses import dataclass


@dataclass
class Account:
    number: str
    deposit: float
    total_profit_loss_money: float
    total_profit_loss_rate: float

