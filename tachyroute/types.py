from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field

class ChoiceQuestion(BaseModel):
    type: str = "choice"
    instructions: str
    criteria: Dict[str, str]

class ScoreQuestion(BaseModel):
    type: str = "score"
    instructions: str
    criteria: List[str]

class BooleanQuestion(BaseModel):
    type: str = "boolean"
    instructions: str

class DecisionResult(BaseModel):
    answer: Any
    confidence: float
    evidence: Optional[List[str]] = Field(default=None, description="Extracted text spans contributing to the decision")
    exit_layer: Optional[int] = Field(default=None, description="The transformer layer where the model exited early")

class RoutingMetadata(BaseModel):
    model: str
    latency_ms: float
    reason: str
