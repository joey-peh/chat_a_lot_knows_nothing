from typing import Annotated, TypedDict
import os
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.chat_models import ChatOllama
from langchain_core.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

# 1. INITIALIZE CACHE
# This creates a local file 'langchain_cache.db'. 
# Subsequent identical or near-identical calls will bypass Ollama.
set_llm_cache(SQLiteCache(database_path=".langchain_cache.db"))

ollama_base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# 2. LLM SETUP
llm = ChatOllama(
    base_url=ollama_base_url,
    model="llama3.2:3b-instruct-q6_K",
    temperature=0.7,
    # num_ctx=2048,
    # num_thread=8
)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

def agent_node(state: AgentState):
    # Caching happens automatically inside .invoke() thanks to set_llm_cache
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Build the graph
workflow = StateGraph(state_schema=AgentState)
workflow.add_node("agent", agent_node)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# Memory handles conversation "Checkpoints" (the flow), 
# while SQLiteCache handles "LLM generation" (the output).
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)
