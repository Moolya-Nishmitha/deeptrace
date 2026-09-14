from pathlib import Path
from transformers import pipeline

# Loaded once when the server starts — NOT inside the function below.
# This is the slow part (downloading + loading the model into memory),
# so we pay that cost once, not on every single upload.
print("Loading deepfake detection model... (this happens once, at startup)")
detector_pipeline = pipeline(
    "image-classification",
    model="prithivMLmods/Deep-Fake-Detector-v2-Model"
)
print("Model loaded.")


def detect_deepfake(filepath: Path) -> dict:
    """
    Runs the image through the deepfake detector.
    Returns the top predicted label and its confidence score.
    """
    results = detector_pipeline(str(filepath))
    # results looks like: [{'label': 'Deepfake', 'score': 0.97}, {'label': 'Realism', 'score': 0.03}]

    top_result = results[0]

    return {
        "label": top_result["label"],
        "confidence": round(top_result["score"] * 100, 2),
        "all_scores": [
            {"label": r["label"], "confidence": round(r["score"] * 100, 2)}
            for r in results
        ],
    }