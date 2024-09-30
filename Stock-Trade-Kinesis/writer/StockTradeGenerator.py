import random
from model.StockTrade import TradeType
from model.StockTrade import StockTrade



class StockPrice:
    def __init__(self, ticker_symbol: str, price: float):
        self.ticker_symbol: str = ticker_symbol
        self.price: float = price
        
    def __repr__(self):
        return f"StockPrice(ticker_symbol='{self.ticker_symbol}', price={self.price})"
    
    
""" 
Generates random stock trades by picking randomly from a collection of stocks, assigning a
random price based on the mean, and picking a random quantity for the shares.
"""


class StockTradeGenerator:
    
    """ The ratio of the deviation from the mean price """
    MAX_DEVIATION: float = 0.2 ## ie 20%
    
    """ The number of shares is picked randomly between 1 and the MAX_QUANTITY """
    MAX_QUANTITY: int = 10000 
    
    """ Probability of trade being a sell """
    PROBABILITY_SELL: float = 0.4 ## ie 40%
    STOCK_PRICES: list = []
    
    
    def __init__(self) -> None:
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("AAPL", 119.72))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("XOM", 91.56))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("GOOG", 527.83))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("BRK.A", 223999.88))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("MSFT", 42.36))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("WFC", 54.21))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("JNJ", 99.78))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("WMT", 85.91))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("CHL", 66.96))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("GE", 24.64))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("NVS", 102.46))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("PG", 85.05))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("JPM", 57.82))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("RDS.A", 66.72))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("CVX", 110.43))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("PFE", 33.07))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("FB", 74.44))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("VZ", 49.09))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("PTR", 111.08))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("BUD", 120.39))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("ORCL", 43.40))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("KO", 41.23))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("T", 34.64))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("DIS", 101.73))
        StockTradeGenerator.STOCK_PRICES.append(StockPrice("AMZN", 370.56))
        self.id = 1


    """
    Return a random stock trade with a unique id every time.
    """
    def getRandomTrade(self) -> StockTrade:
        
        # pick a random stock
        stockPrice: StockPrice = random.choice(StockTradeGenerator.STOCK_PRICES)
        # pick a random deviation between -MAX_DEVIATION and +MAX_DEVIATION
        deviation: float = (random.uniform(0.0, 1.0) - 0.5) * 2.0 * StockTradeGenerator.MAX_DEVIATION
        # set the price using the deviation and mean price
        price: float = stockPrice.price * (1 + deviation)
        # round price to 2 decimal places
        price = round(price * 100.0) / 100.0
        
        # set the trade type to buy or sell depending on the probability of sell
        tradeType: TradeType = TradeType.BUY
        if random.uniform(0.0, 1.0) < StockTradeGenerator.PROBABILITY_SELL:
            tradeType: TradeType = TradeType.SELL
            
        # randomly pick a quantity of shares
        quantity: int = random.randint(1, StockTradeGenerator.MAX_QUANTITY)
        # add 1 because nextInt() will return between 0 (inclusive)
        # and MAX_QUANTITY (exclusive). we want at least 1 share.
        
        tradeId = self.id
        self.id += 1
        
        return StockTrade(stockPrice.ticker_symbol, tradeType, price, quantity, tradeId)