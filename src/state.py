from typing import List, TypedDict


class AgentState(TypedDict, total=False):
    image_paths: List[str]      # paths to the slide images, in order
    teaching_plan: str          # output of planner_agent
    queries: List[str]          # output of query_agent
    retrieved_context: str      # output of rag_agent (stubbed for now)
    narrative: str              # output of generator_agent