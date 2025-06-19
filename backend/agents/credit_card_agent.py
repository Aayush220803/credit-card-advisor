import os
from dotenv import load_dotenv

from backend.logic.recommender import recommend_cards

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory

# Load API key
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

llm = ChatOpenAI(
    temperature=0.3,
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    model="gpt-3.5-turbo"
)

# Tool for recommendation logic
def recommendation_tool_fn(user_input_str):
    import json
    try:
        print("Raw input received by tool:", user_input_str)
        user_input = json.loads(user_input_str)
        print("Parsed input:", user_input)
        results = recommend_cards(user_input)
        print("Recommender output:", results)
        return json.dumps(results)
    except Exception as e:
        print("Tool Error:", e)
        return f"Error in recommendation: {e}"


recommendation_tool = Tool(
    name="CreditCardRecommender",
    func=recommendation_tool_fn,
    description="Use this tool when all user inputs are gathered to recommend top Indian credit cards based on income, spending, and preferences. Takes a JSON string as input."
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent = initialize_agent(
    tools=[recommendation_tool],
    llm=llm,
    agent="chat-conversational-react-description",
    memory=memory,
    verbose=True
)

def run_credit_card_agent(user_message: str) -> str:
    try:
        response = agent.run(user_message)
        return response
    except Exception as e:
        print(f"[Agent Error] {e}")
        return "There was an error in the recommendation process. Please provide more details or try again."


if __name__ == "__main__":
    print("Agent ready. Type your message.")
    while True:
        msg = input("You: ")
        if msg.lower() in ["exit", "quit"]:
            break
        reply = run_credit_card_agent(msg)
        print("Agent:", reply)
