import joblib
import os
import torch
from transformers import BertForSequenceClassification, AdamW, BertConfig, BertTokenizer
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))

pathData = os.path.join(dir_path, '../data')
model_path = os.path.join(dir_path, '../data/model_save')
LE = joblib.load(pathData+'/label_encoder')

model = BertForSequenceClassification.from_pretrained(model_path,   num_labels = 1457,   
    output_attentions = False, # Whether the model returns attentions weights.
    output_hidden_states = False)
tokenizer = BertTokenizer.from_pretrained(model_path, do_lower_case=True)
# model.to(device)


def get_labels(prediction):
    predicted_label =  LE.inverse_transform([prediction])
    return predicted_label[0]



def predict_taxonomy(text):

    encoded_dict = tokenizer.encode_plus(
                        text,                      # Sentence to encode.
                        add_special_tokens = True, # Add '[CLS]' and '[SEP]'
                        max_length = 64,           # Pad & truncate all sentences.
                        pad_to_max_length = True,
                        return_attention_mask = True,   # Construct attn. masks.
                        return_tensors = 'pt',     # Return pytorch tensors.
                   )
    
    # Add the encoded sentence to the list.    
    input_ids = encoded_dict['input_ids']
    
    attention_masks = encoded_dict['attention_mask']


    with torch.no_grad():
        outputs = model(input_ids, token_type_ids=None, 
                      attention_mask=attention_masks)
        logits = outputs[0]
        prediction = np.argmax(logits,axis=1).flatten()
    return get_labels(prediction)

