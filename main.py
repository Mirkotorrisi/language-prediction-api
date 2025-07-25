# This script is part of a FastAPI application for language recognition.
# It defines an API endpoint to identify the language of a given text using a pre-trained model
# To see a well structured version of this code, please refer to this repository:
# https://github.com/Mirkotorrisi/language-prediction-api/tree/main

from fastapi import FastAPI, Body, HTTPException
import os
from pydantic import BaseModel, Field
import pickle
import logging
from typing_extensions import Annotated

# Models 

# Define the data models for the API using Pydantic
# These models will be used to validate the input and output of the API endpoints
class PredictionOutput(BaseModel):
    '''Represents the output of a prediction.'''
    language_code: str = Field(..., description="Predicted language code")
    confidence: float = Field(..., description="Confidence score of the prediction")


class PredictionPayload(BaseModel):
    '''Represents the input payload for language prediction.'''
    model_config = { "extra": "forbid" }
    text: str = Field(default=None, strip_whitespace=True, min_length=1)

    
# Initialize FastAPI app
app = FastAPI(
    debug=os.getenv("DEBUG", "false").lower() == "true", 
    title="Language Identifier model API", 
    description="API for managing language identification", 
    version="1.0.0"
)


# Configure logging
# Set up logging to log to both a file and the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("app")
    

# API endpoint for language identification
@app.post("/identify-language")
def identify_language(body: Annotated[PredictionPayload, Body()]) -> PredictionOutput:
    logger.info(f"Received POST on /identify-language endpoint, text: {body.text}")
    try:
        res = predict_language(body.text)

    except Exception as e:
        logger.error(f"Error occurred while identifying language: {e}") 
        raise HTTPException(status_code=500, detail="Something went wrong while predicting language")

    if(not res.language_code):
        raise HTTPException(status_code=404, detail="Language not found")
    return res
    
# Load the pre-trained model from a pickle file
logger.info("Loading pre-trained language detection pipeline from pickle file...")
filename = 'assets/language_detection_pipeline.pkl'
loaded_pipeline = pickle.load(open(filename, 'rb'))
lang_classes = loaded_pipeline.classes_


# Service function to predict language
def predict_language(text: str) -> PredictionOutput:
    '''
    Get the predicted language for the given text, 
    by using the pre-trained model loaded from a pickle file.
    Args:
        text (str): The input text for language prediction.
    Returns:
        PredictionOutput: The predicted language code.
    '''
    predicted_proba = loaded_pipeline.predict_proba([text])
    confidence = predicted_proba.max(axis=1)
    predicted_language = lang_classes[predicted_proba.argmax(axis=1)]
    output = PredictionOutput(language_code=predicted_language[0], confidence=confidence[0])
    logger.info(f"Output: {output}")

    return output