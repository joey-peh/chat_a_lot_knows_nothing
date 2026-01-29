from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.chat_models import ChatOllama
from core.config import OLLAMA_MODEL, OLLAMA_BASE_URL

# LLM SETUP
llm = ChatOllama(
    base_url=OLLAMA_BASE_URL,
    model=OLLAMA_MODEL,
    temperature=0.7
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
# graph = workflow.compile(checkpointer=memory)
graph = workflow.compile()  # turn off memory for now.. because accuracy is not good when it is noisy