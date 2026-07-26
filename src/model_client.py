import torch
from transformers import AutoModelForImageTextToText, AutoProcessor

from src.config import DEVICE, MODEL_NAME

print(f"Loading {MODEL_NAME} onto {DEVICE} ...")
_processor = AutoProcessor.from_pretrained(MODEL_NAME)
_model = AutoModelForImageTextToText.from_pretrained(
    MODEL_NAME,
    dtype=torch.float16,
).to(DEVICE)
print("Model loaded.")


def call_qwen(messages, max_tokens: int = 4096, **sampling_kwargs) -> str:
    """Run a chat-completion style request through the local HF model and
    return only the newly generated text."""
    inputs = _processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(_model.device)

    output_ids = _model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        do_sample=True,
        **sampling_kwargs,
    )

    new_tokens = output_ids[0][inputs["input_ids"].shape[-1]:]
    return _processor.decode(new_tokens, skip_special_tokens=True)