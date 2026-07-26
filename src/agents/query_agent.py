import json
import re

from src.config import NON_THINKING_VL_PARAMS
from src.model_client import call_qwen
from src.state import AgentState
from src.utils import build_image_content_blocks

QUERY_SYSTEM_PROMPT = (
    "You are a teaching assistant preparing supplementary research for a lecture. "
    "You are given the lecture's slide images (in order) and the teaching plan "
    "already produced for this lecture.\n\n"
    "Your job: identify knowledge gaps - places where the slides are terse, assume "
    "background knowledge, reference something without explaining it, or would "
    "benefit from an example, definition, or up-to-date fact that a retrieval system "
    "could supply.\n\n"
    "For each gap, write ONE focused search/RAG query that would retrieve the missing "
    "information.\n\n"
    "Respond with ONLY a JSON array of strings, no prose, no markdown fences. "
    'Example: ["definition of gradient descent", "real-world example of overfitting"]'
)


def _parse_queries(raw: str):
    raw = raw.strip()
    raw = re.sub(r"^```(json)?|```$", "", raw, flags=re.MULTILINE).strip()
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return [str(q).strip() for q in parsed if str(q).strip()]
    except json.JSONDecodeError:
        pass
    # Fallback: treat each non-empty line as a query
    return [line.strip("-* ").strip() for line in raw.splitlines() if line.strip()]


def query_agent(state: AgentState) -> AgentState:
    image_paths = state["image_paths"]
    plan = state.get("teaching_plan", "")

    content = [
        {"type": "text", "text": QUERY_SYSTEM_PROMPT},
        {"type": "text", "text": f"Teaching plan:\n{plan}"},
    ]
    content += build_image_content_blocks(image_paths)

    messages = [{"role": "user", "content": content}]
    raw = call_qwen(messages, max_tokens=2048, **NON_THINKING_VL_PARAMS)
    queries = _parse_queries(raw)

    return {**state, "queries": queries}