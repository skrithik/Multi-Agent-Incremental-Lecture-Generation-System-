from src.config import NON_THINKING_VL_PARAMS
from src.model_client import call_qwen
from src.state import AgentState
from src.utils import build_image_content_blocks

PLANNER_SYSTEM_PROMPT = (
    "You are an expert instructional designer. You will be shown, in order, all the "
    "slide images of a single lecture. Study them and produce a clear teaching plan "
    "for the lecture as a whole. The plan should:\n"
    "1. Identify the overall topic and learning objectives.\n"
    "2. Break the lecture into logical sections, mapping each section to the slide "
    "numbers it covers (slides are numbered in the order given, starting at 1).\n"
    "3. For each section, note the key concept(s) to teach and the intended teaching "
    "order/emphasis.\n"
    "Return the plan as clearly structured Markdown."
)


def planner_agent(state: AgentState) -> AgentState:
    image_paths = state["image_paths"]

    content = [{"type": "text", "text": PLANNER_SYSTEM_PROMPT}]
    content += build_image_content_blocks(image_paths)
    content.append(
        {
            "type": "text",
            "text": f"There are {len(image_paths)} slides in total, shown above in order.",
        }
    )

    messages = [{"role": "user", "content": content}]
    plan = call_qwen(messages, max_tokens=4096, **NON_THINKING_VL_PARAMS)

    return {**state, "teaching_plan": plan}