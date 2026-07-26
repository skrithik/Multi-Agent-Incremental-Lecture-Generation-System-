from src.state import AgentState


def rag_agent(state: AgentState) -> AgentState:
    """
    STUB. Later this will take state['queries'], retrieve real supporting
    context from a knowledge base / vector store, and return it as
    state['retrieved_context']. For now it just returns a placeholder so the
    graph can run end-to-end and generator_agent has something to consume.
    """
    queries = state.get("queries", [])
    placeholder = "\n".join(
        f"- {q}: [retrieval not implemented yet]" for q in queries
    )
    return {**state, "retrieved_context": placeholder}