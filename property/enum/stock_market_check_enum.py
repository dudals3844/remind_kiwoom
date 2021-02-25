import enum

class StockMarketEnum(enum.Enum):
    BEFORE_START = '장 시작전'
    START = '장 시작'
    SINGLE_PRICE_AUCTION_CALL = '장 종료: 동시호가로 넘어감'
    END = '3시 30분 장 종료'

