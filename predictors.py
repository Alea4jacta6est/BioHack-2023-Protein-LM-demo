from transformers import pipeline


class SSPredictor():
    def __init__(self, model_name="Chandlernnnnnn/esm2_t12_35M_UR50D-finetuned-secondary-structure") -> None:
        self.pipe = pipeline("token-classification", model=model_name)
    
    def predict(self, sequence: str):
        predictions_dict = self.pipe(sequence)
        return predictions_dict