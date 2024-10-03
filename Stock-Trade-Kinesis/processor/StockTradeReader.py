import os
import time
import boto3
import logging
from enum import Enum
from typing import Tuple, List
from botocore.exceptions import ClientError

from model.StockTrade import StockTrade
from model.KinesisStream import KinesisStream

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class StockTradesReader(KinesisStream):
    
    def __init__(self, kinesis_client, streamName):
        super().__init__(kinesis_client, streamName)
        
        
    class ShardIteratorType(Enum):
        LATEST = "LATEST"
        TRIM_HORIZON = "TRIM_HORIZON"
        AT_SEQUENCE_NUMBER = "AT_SEQUENCE_NUMBER"
        AFTER_SEQUENCE_NUMBER = "AFTER_SEQUENCE_NUMBER"
        AT_TIMESTAMP = "AT_TIMESTAMP"
        
        
    def get_shard_iterator(self, shard_id: str, 
                           shard_iterator_type: ShardIteratorType = ShardIteratorType.LATEST,
                           sequence_number: int = None, timestamp: int = None):
        
        try:
            if shard_iterator_type == self.ShardIteratorType.AT_SEQUENCE_NUMBER or \
                shard_iterator_type == self.ShardIteratorType.AFTER_SEQUENCE_NUMBER:
                    
                if sequence_number is None:
                    raise ValueError(
                        "sequence_number must be provided for AT_SEQUENCE_NUMBER and AFTER_SEQUENCE_NUMBER types")
                    
                response = self.kinesis_client.get_shard_iterator(
                    StreamName=self.name,
                    ShardId=shard_id,
                    ShardIteratorType=shard_iterator_type.value,
                    StartingSequenceNumber=sequence_number
                )
            elif shard_iterator_type == self.ShardIteratorType.AT_TIMESTAMP:
                if timestamp is None:
                    raise ValueError("timestamp must be provided for AT_TIMESTAMP type")
                response = self.kinesis_client.get_shard_iterator(
                    StreamName=self.name,
                    ShardId=shard_id,
                    ShardIteratorType=shard_iterator_type.value,
                    Timestamp=timestamp
                )
            else:
                response = self.kinesis_client.get_shard_iterator(
                    StreamName=self.name,
                    ShardId=shard_id,
                    ShardIteratorType=shard_iterator_type.value
                )

            return response['ShardIterator']
        
        except ClientError:
            logger.exception("Couldn't get records from stream %s.", self.name)
            raise
        

    def getStockTrade(self, shard_iterator: object, limit: int) -> Tuple[object, List]:
        try:
            response = self.kinesis_client.get_records(
                ShardIterator=shard_iterator,
                Limit=limit
            )
            records = response['Records']
            shard_iterator = response['NextShardIterator']
            logger.info("Got %s records.", len(records))
            return shard_iterator, records
        except ClientError:
            logger.exception("Couldn't get records from stream %s.", self.name)
            raise

        
if __name__ == '__main__':    
    streamName: str = "StockTradeStream"
    kinesis_client = boto3.client(
        "kinesis",
        region_name='ap-southeast-1',
        aws_access_key_id="XXXXXXXXXX",
        aws_secret_access_key="XXXXXXXXXX"
    )
    
    stockStream = StockTradesReader(kinesis_client=kinesis_client, streamName=streamName)
    
    shard_id = 'shardId-000000000000'
    iterator = stockStream.get_shard_iterator(
        shard_id=shard_id,
        shard_iterator_type=stockStream.ShardIteratorType.LATEST,
        sequence_number="49654562623121058677445974153872638346489209601398931458")
    
    try:
        while True:
            iterator, data = stockStream.getStockTrade(iterator, 100)
            for d in data: print(d['Data'])
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user")