import websocket
import json
import time
import hmac
import hashlib
import requests
from binance_auth import get_listen_key, keep_alive_listen_key, start_user_data_stream
from kinesis_create import create_kinesis
import boto3



def on_message(ws, msg):
    data = json.loads(msg)
    # print(data["data"])
    new_data = {
        "symbol": data["data"]['s'],
        "event": data["data"]["e"],
        "markPrice": data["data"]["p"],
        "event_time": data["data"]["E"],
        "trade_time": data["data"]["T"]
    }
    print(new_data)

    response = kinesis_client.put_record(
        StreamName = "binance_queue",
        Data = json.dumps(new_data),
        PartitionKey = new_data["symbol"]
    )
    print(f"Kinesis response: {response}")

    # print(data)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"Closed connection: {close_status_code}, {close_msg}")

def on_open(ws):
    params = {
        "method": "ticker.price",
        "params": {
            "symbol": "BTCUSDT"  # You can change the pair here
        },
        "id": "1"
    }
    ws.send(json.dumps(params))

def sign_message(secret, message):
    return hmac.new(secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

    

if __name__ == "__main__":
    response = create_kinesis(stream_name="binance_queue")
    print(response)
    kinesis_client = boto3.client("kinesis")
    # listen_key = get_listen_key()

    # if listen_key:
    #     # Start WebSocket in a separate thread
    #     start_user_data_stream(listen_key)

    #     # Keep the listenKey alive every 30 minutes
    #     while True:
    #         time.sleep(30 * 60)  # 30 minutes
    #         keep_alive_listen_key(listen_key)
    ws = websocket.WebSocketApp(f"wss://fstream.binance.com/stream?streams=bnbusdt@aggTrade/btcusdt@markPrice",
                             on_message=on_message,
                             on_error=on_error,
                             on_close=on_close)
    # ws.on_open = on_open
    ws.run_forever()

