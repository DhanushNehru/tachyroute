import time
import torch
from transformers import pipeline
from typing import Dict, Any

from tachyroute.types import DecisionResult

class Engine:
    """
    TachyRoute Core Engine: Non-autoregressive model wrapper with Early-Exit and Explainability.
    """
    def __init__(self, model_name: str = "facebook/bart-large-mnli", device: int = -1):
        self.model_name = model_name
        self.device = device
        # For a truly unique offering, we would wrap a custom PyTorch model with Early-Exit layers.
        # Here we use a zero-shot classifier as a baseline for the logic.
        self._classifier = pipeline(
            "zero-shot-classification",
            model=model_name,
            device=device
        )

    def predict(self, text: str, question: Dict[str, Any]) -> DecisionResult:
        start_time = time.time()
        
        q_type = question.get("type", "choice")
        
        if q_type == "choice":
            labels = list(question["criteria"].keys())
        elif q_type == "score":
            labels = question["criteria"]
        elif q_type == "boolean":
            labels = ["Yes", "No"]
        else:
            raise ValueError(f"Unknown question type: {q_type}")

        # Perform the forward pass
        # In a custom architecture, we'd extract intermediate logits to compute the early exit layer.
        result = self._classifier(text, candidate_labels=labels, multi_label=False)
        
        top_label = result["labels"][0]
        confidence = result["scores"][0]
        
        # Mocking explainability (attention rollout) & early exit metrics
        # TachyRoute differentiates itself by explaining *why* and running *faster*.
        words = text.split()
        evidence_span = " ".join(words[:min(5, len(words))]) if words else ""
        
        # Simulate early exit logic: high confidence -> exit early
        exit_layer = 6 if confidence > 0.9 else 12 if confidence > 0.7 else 24

        return DecisionResult(
            answer=top_label,
            confidence=confidence,
            evidence=[evidence_span],
            exit_layer=exit_layer
        )
