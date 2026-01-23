from typing import Annotated, TypedDict
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# LLM setup
llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

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