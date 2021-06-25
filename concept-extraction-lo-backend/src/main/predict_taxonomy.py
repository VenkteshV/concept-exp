import joblib
import os
import torch
from transformers import BertForSequenceClassification, AdamW, BertConfig, BertTokenizer
import numpy as np
import sent2vec
import torch.nn.functional as F
from transformers import BertModel, AdamW, BertConfig, BertTokenizer

import torch.nn as nn

dir_path = os.path.dirname(os.path.realpath(__file__))

pathData = os.path.join(dir_path, '../data')
model_path = os.path.join(dir_path, '../data/model_save_reduced')
model_path_recommend = os.path.join(dir_path, '../data/model_euclidean_1')

test_labels = joblib.load(pathData+'/test_labels')
test_labels = np.array(test_labels)

LE = joblib.load(pathData+'/label_encoder_reduced')

labels_with_board = joblib.load(pathData+'/labels_formatted')

model = BertForSequenceClassification.from_pretrained(model_path,   num_labels = 332,   
    output_attentions = False, # Whether the model returns attentions weights.
    output_hidden_states = False)
tokenizer = BertTokenizer.from_pretrained(model_path, do_lower_case=True)
# model.to(device)
class MulticlassClassifier(nn.Module):
    def __init__(self,bert_model_path):
        super(MulticlassClassifier,self).__init__()
        self.bert = BertModel.from_pretrained(bert_model_path,output_hidden_states=False,output_attentions=False)
        self.dropout = nn.Dropout(0.1)
        self.fc1 = nn.Linear(768, 384)
        self.fc2 = nn.Linear(384, 700)

    def forward(self,tokens,masks):
        _, pooled_output = self.bert(tokens, attention_mask=masks)
        x = self.fc1(pooled_output)
        x = self.fc2(x)
        return x

model_recommender = MulticlassClassifier('bert-base-uncased')
model_recommender.load_state_dict(torch.load(model_path_recommend+'/model_weights.zip',map_location=torch.device('cpu')))

recommender_tokenizer = BertTokenizer.from_pretrained(model_path_recommend, do_lower_case=True)

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

# def dist_without_grad( u, v):
#   sqdist = torch.sum((u - v) ** 2, dim=-1)
#   squnorm = torch.sum(u ** 2, dim=-1)
#   sqvnorm = torch.sum(v ** 2, dim=-1)
#   x = 1 + 2 * sqdist / ((1 - squnorm) * (1 - sqvnorm)) + 1e-7
#   z = torch.sqrt(x ** 2 - 1)
#   return torch.log(x + z)
def get_cleaned_taxonomy(taxonomy):
  cleaned_taxonomy = []
  for value in taxonomy:
      value = ' '.join(value.split(">>"))
      cleaned_taxonomy.append( value )
  return cleaned_taxonomy

sent2vec_model = sent2vec.Sent2vecModel()
print("sent2vec",dir_path+'/torontobooks_unigrams.bin')
sent2vec_model.load_model(dir_path+'/embedding/torontobooks_unigrams.bin')
print("here")
def get_taxonomy_embeddings():
    cleaned_taxonomy = get_cleaned_taxonomy(test_labels)
    taxonomy_vectors = []
    for feature in cleaned_taxonomy:
        taxonomy_vectors.append(sent2vec_model.embed_sentences([feature]))
    taxonomy_vectors = np.vstack(taxonomy_vectors)
    test_poincare_tensor = torch.tensor(taxonomy_vectors,dtype=torch.float)
    return test_poincare_tensor
test_poincare_tensor = get_taxonomy_embeddings()
print("test_labels",test_poincare_tensor.shape)


def recommend_taxonomy(text):

    encoded_dict = recommender_tokenizer.encode_plus(
                        text,                      # Sentence to encode.
                        add_special_tokens = True, # Add '[CLS]' and '[SEP]'
                        max_length = 128,           # Pad & truncate all sentences.
                        pad_to_max_length = True,
                        return_attention_mask = True,   # Construct attn. masks.
                        return_tensors = 'pt',     # Return pytorch tensors.
                   )
    
    # Add the encoded sentence to the list.    
    input_ids = encoded_dict['input_ids']
    
    attention_masks = encoded_dict['attention_mask']

    # Tracking variables 
    predictions , true_labels = [], []
    with torch.no_grad():
        outputs = model_recommender(input_ids.reshape(1,-1),attention_masks.reshape(1,-1))
        
    distances = (F.normalize(outputs,p=2,dim=1) - F.normalize(test_poincare_tensor,p=2,dim=1)).pow(2).sum(1)
    distances,indices = torch.topk(distances,3,largest=False)

    top_k_labels = test_labels[indices.cpu().numpy()]
    top_k_labels = list(top_k_labels)
    print("top_k_labels are", test_labels[indices.cpu().numpy()])

    final_list = []
    for label in top_k_labels:
        for formatted_label in labels_with_board:
            if label in formatted_label and len(label.split(">>"))>1:
                final_list.append(formatted_label)

    return final_list

