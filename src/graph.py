from langgraph.graph import END, START, StateGraph

from src.agents.generator_agent import generator_agent
from src.agents.planner_agent import planner_agent
from src.agents.query_agent import query_agent
from src.agents.rag_agent import rag_agent
from src.state import AgentState


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_agent)
    graph.add_node("query", query_agent)
    # graph.add_node("rag", rag_agent)
    graph.add_node("generator", generator_agent)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "query")
    # graph.add_edge("query", "rag")
    graph.add_edge("query", "generator")
    graph.add_edge("generator", END)

    return graph.compile()