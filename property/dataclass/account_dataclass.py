from dataclasses import dataclass


@dataclass
class AccountData:
    number: str = None
    deposit: float = None
    total_buy_money: float = None
    total_profit_loss_money: float = None
    total_profit_loss_rate: float = None

