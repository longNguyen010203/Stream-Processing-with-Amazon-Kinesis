import json
import base64
from datetime import datetime


def lambda_handler(event: dict, context) -> dict:
    transformed_messages = []
    
    for record in event["records"]:
        
        # Decode and load the message from Kinesis
        try:
            message: dict = json.loads(base64.b64decode(record["data"]).decode("utf-8"))
            print(f"Message: {message}")
        except (json.JSONDecodeError) as e:
            print(f"Error decoding record: {e}")
            continue  # Skip this record if there's an error
        
        # Rename column
        if "tickerSymbol" in message:
            message["stockId"] = message.pop("tickerSymbol")

        # add transaction time column
        message["tradeTime"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        # change data type
        for field in ["price", "quantity", "id"]:
            if field in message:
                try:
                    message[field] = float(message[field]) if field == "price" else int(message[field])
                except (ValueError, TypeError):
                    message[field] = None
        
        # Encode the transformed message back to base64
        try:
            encoded_data = base64.b64encode(json.dumps(message).encode("utf-8")).decode("utf-8")
        except (TypeError, ValueError) as e:
            print(f"Error encoding message: {e}")
            continue  # Skip this record if there's an encoding error
        
        # Add the transformed record to the output
        transformed_messages.append({
            "recordId": record["recordId"],
            "result": "Ok",
            "data": encoded_data
        })
                    
    return { "records": transformed_messages }