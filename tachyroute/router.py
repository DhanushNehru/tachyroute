import time
from typing import Dict, Any, Union
from tachyroute.engine import Engine
from tachyroute.types import RoutingMetadata

class Router:
    """
    Multimodal & Multilingual Router.
    Automatically detects complexity and language to route to the correct model.
    """
    def __init__(self, preload: bool = False):
        self.engines = {}
        if preload:
            self.load_model("english", "facebook/bart-large-mnli")
            self.load_model("multilingual", "joeddav/xlm-roberta-large-xnli")
            self.load_model("quantized-fast", "cross-encoder/nli-deberta-v3-small")

    def load_model(self, name: str, hf_id: str):
        if name not in self.engines:
            self.engines[name] = Engine(model_name=hf_id)

    def route_request(self, text: str) -> str:
        # A lightweight heuristic to detect non-English or complexity
        # In a real scenario, we use a fast fasttext classifier or regex
        if any(ord(char) > 127 for char in text):
            return "multilingual"
        
        if len(text.split()) < 15:
            # Simple short queries can go to the fast quantized model
            return "quantized-fast"
            
        return "english"

    def predict(self, state: Union[str, Dict[str, str]], questions: Dict[str, Dict[str, Any]], model: str = None) -> Dict[str, Any]:
        t0 = time.time()
        
        # Parse state
        if isinstance(state, dict):
            text = " ".join(str(v) for v in state.values())
        else:
            text = state
            
        # Route
        chosen_model = model or self.route_request(text)
        
        # Lazy load if needed
        if chosen_model not in self.engines:
            if chosen_model == "multilingual":
                self.load_model("multilingual", "joeddav/xlm-roberta-large-xnli")
            elif chosen_model == "quantized-fast":
                self.load_model("quantized-fast", "cross-encoder/nli-deberta-v3-small")
            else:
                self.load_model("english", "facebook/bart-large-mnli")

        engine = self.engines[chosen_model]
        
        # Execute
        answers = {}
        max_exit_layer = 0
        for q_key, q_val in questions.items():
            res = engine.predict(text, q_val)
            answers[q_key] = res.dict()
            if res.exit_layer and res.exit_layer > max_exit_layer:
                max_exit_layer = res.exit_layer
                
        t1 = time.time()
        latency = (t1 - t0) * 1000
        
        routing_info = RoutingMetadata(
            model=chosen_model,
            latency_ms=latency,
            reason=f"Routed based on text characteristics. Max compute depth: {max_exit_layer} layers."
        )

        return {
            "answers": answers,
            "routing": routing_info.dict()
        }
