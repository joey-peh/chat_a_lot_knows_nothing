from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from django.contrib.auth import get_user_model

# Example tool: Fetch user data from Django DB (runs in the same process)
@tool
def get_user_info(user_id: int) -> str:
    """Get basic info about a user by ID."""
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        return f"User: {user.username}, Email: {user.email}"
    except User.DoesNotExist:
        return "User not found."

# LLM setup
llm = ChatOpenAI(
    model="gpt-4o-mini"
).bind_tools([get_user_info])

# State with message history
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# Agent node: Calls LLM
def agent_node(state: AgentState):
    return {"messages": [llm.invoke(state["messages"])]}

# Build the graph with memory
workflow = StateGraph(state_schema=AgentState)
workflow.add_node("agent", agent_node)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# Compile with memory (in-memory for simplicity; can use DB checkpointer later)
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)