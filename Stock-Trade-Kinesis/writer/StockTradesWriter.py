import os
import time
import boto3
import logging
from typing import Optional
from botocore.exceptions import ClientError

from model.StockTrade import TradeType
from model.StockTrade import StockTrade
from model.KinesisStream import KinesisStream
from writer.StockTradeGenerator import StockTradeGenerator

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class StockTradesWriter(KinesisStream):
    
    def __init__(self, kinesis_client, streamName):
        super().__init__(kinesis_client, streamName)
    
    def sendStockTrade(self, trade: StockTrade) -> None:
        bytess: Optional[bytes] = trade.toJsonAsBytes()
        if bytess is None: 
            logger.info("Could not get JSON bytes for stock trade")
            return
        
        logger.info(f"Putting trade: {trade.__str__()}")
        
        try:
            response = self.kinesis_client.put_record(
                StreamName=self.name, 
                Data=bytearray(bytess), 
                PartitionKey=trade.getTickerSymbol()
            )
            # logger.info("Put record in stream %s.", self.name)
            
        except ClientError as e:
            logger.exception("Couldn't put record in stream %s.", self.name)
            logger.exception(f"Couldn't put record in stream {self.name}." + 
                             f"Error: {e.response['Error']['Message']}")
            raise
        else:
            return response



if __name__ == "__main__":
    streamName: str = "StockTradeStream"
    kinesis_client = boto3.client(
        "kinesis",
        region_name='ap-southeast-1',
        aws_access_key_id="XXXXXXXXXX",
        aws_secret_access_key="XXXXXXXXXX"
    )

    stockStream = StockTradesWriter(kinesis_client, streamName)
    stockTradeGenerator = StockTradeGenerator()
    logger.info("Put record in stream %s.", stockStream.name)

    try:
        while True:
            trade: StockTrade = stockTradeGenerator.getRandomTrade()
            stockStream.sendStockTrade(trade=trade)
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopped put record in stream %s.", stockStream.name)
        print("Stopped by user")
        