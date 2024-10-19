import requests
import hmac
import hashlib
import time
import websocket
import json
import os
from dotenv import load_dotenv


load_dotenv()

# API credentials
api_key = os.getenv("BINANCE_KEY")
api_secret = os.getenv("BINANCE_SECRET")

# Step 1: Obtain the listenKey
def get_listen_key():
    url = 'https://fapi.binance.com/fapi/v1/listenKey'
    headers = {'X-MBX-APIKEY': api_key}
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        listen_key = response.json()['listenKey']
        print(f"ListenKey: {listen_key}")
        return listen_key
    else:
        print(f"Error fetching listenKey: {response.json()}")
        return None

# Step 2: Define WebSocket handlers
def on_message(ws, message):
    print(f"Received message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### WebSocket closed ###")

def on_open(ws):
    print("### WebSocket connection opened ###")

# Step 3: Connect to WebSocket using the listenKey
def start_user_data_stream(listen_key):
    ws_url = f"wss://fstream.binance.com/ws/{listen_key}"
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

# Step 4: Refresh listenKey every 30 minutes
def keep_alive_listen_key(listen_key):
    url = 'https://fapi.binance.com/fapi/v1/listenKey'
    headers = {'X-MBX-APIKEY': api_key}
    
    response = requests.put(url, headers=headers)
    
    if response.status_code == 200:
        print(f"ListenKey refreshed: {listen_key}")
    else:
        print(f"Error refreshing listenKey: {response.json()}")

