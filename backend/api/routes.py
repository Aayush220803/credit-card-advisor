from fastapi import APIRouter, Request
from pydantic import BaseModel
from backend.agents.credit_card_agent import run_credit_card_agent

router = APIRouter()

class ChatInput(BaseModel):
    message: str

@router.post("/chat")
async def chat_with_agent(request: ChatInput):
    user_message = request.message
    try:
        agent_reply = run_credit_card_agent(user_message)
        return {"response": agent_reply}
    except Exception as e:
        return {"error": str(e)}
