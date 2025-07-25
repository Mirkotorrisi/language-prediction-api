from fastapi import APIRouter
from models.prediction_payload import PredictionPayload
from models.prediction_output import PredictionOutput
from typing_extensions import Annotated
from fastapi import Body
from utils.logger import logger


from services.predict_language import predict_language

router = APIRouter()

@router.post("/identify-language")
def identify_language(body: Annotated[PredictionPayload, Body()]) -> PredictionOutput:
    logger.info(f"Received POST on /identify-language endpoint, text: {body.text}")
    try:
        res = predict_language(body.text)
        return res

    except Exception as e:
        logger.error(f"Error occurred while identifying language: {e}") 
        raise Exception("Error occurred while identifying language")
