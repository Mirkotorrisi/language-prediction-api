from models.prediction_output import PredictionOutput
import pickle
from utils.logger import logger

filename = 'assets/language_detection_pipeline.pkl'
loaded_pipeline = pickle.load(open(filename, 'rb'))

def predict_language(text: str) -> PredictionOutput:
    '''
    Get the predicted language for the given text, 
    by using the pre-trained model loaded from a pickle file.
    Args:
        text (str): The input text for language prediction.
    Returns:
        PredictionOutput: The predicted language code.
    '''
    predicted_language = loaded_pipeline.predict([text])

    logger.info(f"Predicted language: {predicted_language[0]}")

    output = PredictionOutput(language_code=predicted_language[0])
    logger.info(f"Output: {output}")

    return output
