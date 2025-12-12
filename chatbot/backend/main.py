import json
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv('./.env')

from ai_agent.graph import build_graph


app = FastAPI(title="Legal AI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


legal_graph = build_graph()


def format_sse(content: str) -> str:
    """Helper para formatar Server-Sent Events"""
    return f"data: {json.dumps({'content': content})}\n\n"


async def run_legal_agent_streaming(last_message: str):
    inputs = {"question": last_message, "loop_count": 0}
    
    async for event in legal_graph.astream_events(inputs, version="v2"):
        kind = event["event"]
        metadata = event.get("metadata", {})
        if kind == "on_chat_model_stream":
            node_name = metadata.get("langgraph_node")
            if node_name in ["generate", "general_conversation"]:
                content = event["data"]["chunk"].content
                
                if content:
                    yield format_sse(content)

    yield "data: [DONE]\n\n"


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    if not request.messages:
        return {"error": "No messages"}
    
    last_user_msg = request.messages[-1].content
    
    return StreamingResponse(
        run_legal_agent_streaming(last_user_msg),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
