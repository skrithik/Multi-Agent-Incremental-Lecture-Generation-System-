import json
import os

from src.config import IMAGES_DIR, OUTPUTS_DIR
from src.graph import build_graph
from src.utils import get_sorted_image_paths


def main():
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    image_paths = get_sorted_image_paths(IMAGES_DIR)
    if not image_paths:
        raise SystemExit(f"No images found in {IMAGES_DIR}")
    print(f"Found {len(image_paths)} slide images.")
    for p in image_paths:
        print("  -", os.path.basename(p))

    app = build_graph()
    final_state = app.invoke({"image_paths": image_paths})

    with open(os.path.join(OUTPUTS_DIR, "teaching_plan.md"), "w") as f:
        f.write(final_state.get("teaching_plan", ""))

    with open(os.path.join(OUTPUTS_DIR, "rag_queries.json"), "w") as f:
        json.dump(final_state.get("queries", []), f, indent=2)

    with open(os.path.join(OUTPUTS_DIR, "retrieved_context.txt"), "w") as f:
        f.write(final_state.get("retrieved_context", ""))

    with open(os.path.join(OUTPUTS_DIR, "narrative.md"), "w") as f:
        f.write(final_state.get("narrative", ""))

    print("\nDone. Outputs written to:", OUTPUTS_DIR)


if __name__ == "__main__":
    main()