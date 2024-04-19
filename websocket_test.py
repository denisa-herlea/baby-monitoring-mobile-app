import websocket

try:
    ws = websocket.create_connection("wss://echo.websocket.org/")
    print("WebSocket is working")
    ws.close()
except Exception as e:
    print("An error occurred:", e)
