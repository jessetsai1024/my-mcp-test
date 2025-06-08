from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import asyncio, json, uvicorn

app = FastAPI()

def sse(data: dict, event: str = "message") -> str:
    """把 dict 編碼成標準 SSE 格式"""
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"

@app.post("/mcp")
async def handle_post(req: Request):
    payload = await req.json()

    async def stream():
        # 先回應一個「ack」事件，取代原本的 JSONResponse
        yield sse({"status": "accepted"}, event="ack")
        # 示範分段回傳
        yield sse({"partial": True})
        await asyncio.sleep(0.5)
        yield sse({"echo": payload})

    return StreamingResponse(stream(), media_type="text/event-stream")

@app.get("/mcp")
async def handle_get():
    async def heartbeat():
        i = 0
        while True:
            yield sse({"ping": i}, event="ping")
            i += 1
            await asyncio.sleep(5)
    return StreamingResponse(heartbeat(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run("sse_server:app", host="0.0.0.0", port=8000, reload=True)
