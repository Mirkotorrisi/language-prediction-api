from pydantic import BaseModel, Field

class PredictionPayload(BaseModel):
    '''
    Represents the input payload for language prediction.
    '''
    model_config = { "extra": "forbid" }
    text: str = Field(default=None, strip_whitespace=True, min_length=1)