import requests, sseclient

SERVER = "http://127.0.0.1:8000/mcp"

data = {"jsonrpc": "2.0", "id": 1, "method": "echo", "params": {"msg": "hello"}}

# 要求伺服器可以回 SSE
resp = requests.post(SERVER, json=data,
                     headers={"Accept": "text/event-stream"},
                     stream=True)

client = sseclient.SSEClient(resp)        # sseclient 與 requests 無縫整合:contentReference[oaicite:7]{index=7}
for event in client.events():
    print(f"[{event.event}] {event.data}")