from pydantic import BaseModel, Field

class PredictionOutput(BaseModel):
    '''Represents the output of a prediction.'''
    language_code: str = Field(..., description="Predicted language code")
    confidence: float = Field(..., description="Confidence score of the prediction")
