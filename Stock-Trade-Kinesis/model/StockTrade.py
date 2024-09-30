import json
from enum import Enum
from typing import Union, Optional



""" 
Represents the type of the stock trade e.g. buy or sell. 
"""
class TradeType(Enum):
    BUY: str = "BUY"
    SELL: str = "SELL"


""" 
Captures the key elements of a stock trade, such as the ticker symbol, price,
number of shares, the type of the trade (buy or sell), and an id uniquely identifying
the trade.
"""
class StockTrade:
    
    def __init__(self, tickerSymbol: str, tradeType: TradeType, price: float, quantity: int, id: int) -> None:
        self.tickerSymbol: str = tickerSymbol
        self.tradeType: TradeType = tradeType
        self.price: float = price
        self.quantity: int = quantity
        self.id: int = id

    def getTickerSymbol(self) -> str:
        return self.tickerSymbol

    def getTradeType(self) -> TradeType:
        return self.tradeType

    def getPrice(self) -> float:
        return self.price

    def getQuantity(self) -> int:
        return self.quantity

    def getId(self) -> int:
        return self.id
    
    def toJsonAsBytes(self) -> Optional[bytes]:
        try: 
            data = {
                "tickerSymbol": self.tickerSymbol,
                "tradeType": self.tradeType.value,
                "price": self.price,
                "quantity": self.quantity,
                "id": self.id
            }
            
            return json.dumps(data).encode("utf-8")
        except Exception as e:
            print(f"Error encoding to JSON: {e}")
            return None
    
    @staticmethod
    def fromJsonAsBytes(bytesData: Union[bytes, str]):
        try:
            data = json.loads(bytesData)
            return StockTrade(
                tickerSymbol=data["tickerSymbol"],
                tradeType=TradeType(data["tradeType"]),
                price=data["price"],
                quantity=data["quantity"],
                id=data["id"]
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error decoding JSON: {e}")
            return None

    def __str__(self) -> str:
        return "ID {}: {} {} shares of {} for ${:.2f}".format(
            self.id, self.tradeType.value, self.quantity, self.tickerSymbol, self.price
        )