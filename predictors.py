from transformers import pipeline
from prottrans import *


class SSPredictor():
    def __init__(self, model_name="Chandlernnnnnn/esm2_t12_35M_UR50D-finetuned-secondary-structure") -> None:
        self.pipe = pipeline("token-classification", model=model_name)
    
    def predict(self, sequence: str):
        predictions_dict = self.pipe(sequence)
        return predictions_dict
    
    def convert_esm2_output(self, esm2_t12_output):
        classif_res = []
        for el in esm2_t12_output:
            classif_res.append(int(el['entity'].split('_')[1]))
        
        return classif_res


class ProtTransSSPredictor():
    def __init__(self) -> None:
        self.model, self.tokenizer = get_T5_model()

    
    def predict(self, sequence: str):
        predictions = get_embeddings( self.model, self.tokenizer, sequence,
                        )
        return predictions
    
    def convert_prottrans_output(self, prottrans_output):
        classif_res = []
        #   class_mapping = {0:"H",1:"E",2:"L"} 
        class_mapping = {0:0,1:1,2:2} 
        classif_res = [''.join( [class_mapping[j] for j in yhat] )
                for seq_id, yhat in prottrans_output.items()]
        return classif_res




