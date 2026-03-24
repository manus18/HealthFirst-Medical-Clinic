from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from agents.faq_agent import faq_node, tools
from config.memory import checkpointer, store

workflow = StateGraph(MessagesState)

# Add nodes
workflow.add_node("faq", faq_node)
workflow.add_node("tools", ToolNode(tools))

# Set entry point
workflow.add_edge(START, "faq")

# Add conditional edges
workflow.add_conditional_edges(
    "faq",
    tools_condition,
)

# Add edge from tools back to faq
workflow.add_edge("tools", "faq")

# Compile the graph
faq_graph = workflow.compile(checkpointer=checkpointer, store=store)
