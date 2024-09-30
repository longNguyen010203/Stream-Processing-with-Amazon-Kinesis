from model.StockTrade import TradeType
from model.StockTrade import StockTrade




class StockStatistic:
    
    countsByTradeType: dict[TradeType, dict[str, int]] = {}
    mostPopularByTradeType: dict[TradeType, str] = {}
    
    
    def __init__(self) -> None:
        StockStatistic.countsByTradeType: dict[TradeType, dict[str, int]] = {
            tradeType: {} for tradeType in TradeType
        }
        
    
    """ 
    Updates the statistics taking into account the new stock trade received.
    """
    
    def addStockTrade(self, trade: StockTrade) -> None:
        # update buy/sell count
        type: TradeType = trade.getTradeType()
        counts: dict[str, int] = StockStatistic.countsByTradeType.get(type)
        count: int = counts.get(trade.getTickerSymbol(), 0)
        counts[trade.getTickerSymbol()] = count + 1
        
        # update most popular stock
        mostPopular: str = StockStatistic.mostPopularByTradeType.get(type)
        if mostPopular is None or StockStatistic.countsByTradeType.get(type).get(mostPopular) < count:
            StockStatistic.mostPopularByTradeType.update({type, trade.getTickerSymbol()})
        
    
    def __str__(self) -> str:
        return "Most popular stock being bought: {}, {} buys.\n" + \
               "Most popular stock being sold: {}, {} sells.".format(
                    self.getMostPopularStock(TradeType.BUY), self.getMostPopularStockCount(TradeType.BUY),
                    self.getMostPopularStock(TradeType.SELL), self.getMostPopularStockCount(TradeType.SELL)
                )
    
    def getMostPopularStock(self, tradeType: TradeType) -> str:
        return StockStatistic.mostPopularByTradeType.get(tradeType)
    
    
    def getMostPopularStockCount(self, tradeType: TradeType) -> int:
        mostPopular = self.getMostPopularStock(tradeType)
        return StockStatistic.countsByTradeType.get(tradeType).get(mostPopular)