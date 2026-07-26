import os

MODEL_NAME = os.environ.get("QWEN_MODEL_NAME", "Qwen/Qwen3.5-0.8B")
DEVICE = os.environ.get("QWEN_DEVICE", "cuda:0")  # GPU 0 was idle in your nvidia-smi

# Project paths
PROJECT_ROOT = os.environ.get("AGENTIC_AI_ROOT", "/mnt/storage/sonali/agentic_ai")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "images")
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")

# Sampling params, following Qwen3.5's recommended settings for
# non-thinking mode / VL tasks (see model card "Best Practices")
NON_THINKING_VL_PARAMS = dict(
    temperature=0.7,
    top_p=0.8,
    top_k=20,
)