from src.config import NON_THINKING_VL_PARAMS
from src.model_client import call_qwen
from src.state import AgentState
from src.utils import build_image_content_blocks

GENERATOR_SYSTEM_PROMPT = (
    "You are an engaging lecturer narrating a slide deck to students out loud. "
    "You are given: the full teaching plan for the lecture, supplementary notes "
    "retrieved to fill knowledge gaps, and all the slide images in order.\n\n"
    "Write a natural spoken-style narrative script for the ENTIRE lecture that a "
    "teacher could read aloud while advancing through the slides. Requirements:\n"
    "1. Follow the structure and order given in the teaching plan.\n"
    "2. Clearly mark which slide each part of the narrative corresponds to, e.g. "
    "'--- Slide 3 ---' before the narration for that slide.\n"
    "3. Weave in the supplementary notes where relevant, in your own words.\n"
    "4. Keep the tone clear, engaging, and appropriate for the apparent level of "
    "the material.\n\n"
    "Output the full narrative as Markdown."
)


def generator_agent(state: AgentState) -> AgentState:
    image_paths = state["image_paths"]
    plan = state.get("teaching_plan", "")
    context = state.get("retrieved_context", "")

    content = [
        {"type": "text", "text": GENERATOR_SYSTEM_PROMPT},
        {"type": "text", "text": f"Teaching plan:\n{plan}"},
        {"type": "text", "text": f"Supplementary retrieved notes:\n{context}"},
    ]
    content += build_image_content_blocks(image_paths)

    messages = [{"role": "user", "content": content}]
    narrative = call_qwen(messages, max_tokens=8192, **NON_THINKING_VL_PARAMS)

    return {**state, "narrative": narrative}