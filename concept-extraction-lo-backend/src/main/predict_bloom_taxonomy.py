import joblib
import os
import torch
from transformers import BertModel, AdamW, BertConfig, BertTokenizer
import numpy as np
import gensim.models.poincare as poincare
from torch import nn
dir_path = os.path.dirname(os.path.realpath(__file__))

import gensim.downloader as api
wv = api.load('glove-wiki-gigaword-300')

pathData = os.path.join(dir_path, '../data')
model_path = os.path.join(dir_path, '../data/model_save_reduced')
LE = joblib.load(pathData+'/label_encoder_blooms')

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
poincare_model = poincare.PoincareModel.load(pathData+"/taxonomy_embedding_20.pkl")

class MultiClassClassifier(nn.Module):
    def __init__(self, bert_model_path, labels_count, hidden_dim=768, mlp_dim=100, extras_dim=440, dropout=0.1, freeze_bert=False):
        super().__init__()

        self.bert = BertModel.from_pretrained(bert_model_path,output_hidden_states=False,output_attentions=False)
        self.dropout = nn.Dropout(dropout)
        self.mlp = nn.Sequential(
            nn.Linear(hidden_dim + extras_dim, mlp_dim),
            nn.ReLU(),
            nn.Linear(mlp_dim, mlp_dim),
            # nn.ReLU(),
            # nn.Linear(mlp_dim, mlp_dim),
            nn.ReLU(),            
            nn.Linear(mlp_dim, labels_count)
        )
        self.softmax = nn.LogSoftmax(dim=1)
        if freeze_bert:
            for param in self.bert.parameters():
                param.requires_grad = False

    def forward(self, tokens, masks, poincare_emb,diffculty_emb):
        _, pooled_output = self.bert(tokens, attention_mask=masks)
        dropout_output = self.dropout(pooled_output)
        concat_output = torch.cat((dropout_output, poincare_emb,diffculty_emb), dim=1)
        mlp_output = self.mlp(concat_output)
        # proba = self.sigmoid(mlp_output)
        proba = self.softmax(mlp_output)

        return proba

tokenizer = BertTokenizer.from_pretrained(model_path, do_lower_case=True)
# model.to(device)
model = MultiClassClassifier('bert-base-uncased',8, 768,500,440,dropout=0.1,freeze_bert=False)
model.load_state_dict(torch.load(os.path.join(dir_path, '../data/model_save_blooms/model_weights'),map_location=torch.device('cpu')))

def get_labels(prediction):
    predicted_label =  LE.inverse_transform([prediction])
    return predicted_label[0]

def exponential_map(vector):
        norm_v = np.linalg.norm(vector, axis=1)
        coef = np.tanh(norm_v) / norm_v
        second_term = vector * coef[:, None]
        return second_term


def predict_bloom_taxonomy(text,course_taxonomy,difficulty_level):

    encoded_dict = tokenizer.encode_plus(
                        text,                      # Sentence to encode.
                        add_special_tokens = True, # Add '[CLS]' and '[SEP]'
                        max_length = 256,           # Pad & truncate all sentences.
                        pad_to_max_length = True,
                        return_attention_mask = True,   # Construct attn. masks.
                        return_tensors = 'pt',     # Return pytorch tensors.
                   )
                   
    
    # Add the encoded sentence to the list.    
    input_ids = encoded_dict['input_ids']
    
    attention_masks = encoded_dict['attention_mask']

    #word vectors for difficulty level
    difficulty_level_vectors = []
    words = [word.lower() for word in difficulty_level.split(" ")]
    if len(words) > 1:
        difficulty_level_vectors.append(np.mean(wv[words],axis=0))
    else:
        difficulty_level_vectors.append(wv[words].squeeze(axis=0))

    difficulty_level_vectors = np.array(difficulty_level_vectors)
    course_tax_split = course_taxonomy.split(">>")
    poincare_embedding_test = [ exponential_map(np.expand_dims(np.hstack([   poincare_model.kv.get_vector(str(taxonomy)) for taxonomy in course_tax_split ]), axis=0))]
    concatenated_embedding = []
    print(poincare_embedding_test,poincare_embedding_test[0].shape)
    max_val = 140
    for embedding in poincare_embedding_test:
        if embedding.shape[1] < max_val:
            new_embedding = np.append(embedding, np.expand_dims(np.zeros(max_val-embedding.shape[1]),axis=0),axis=1)
        else:
            new_embedding = embedding
        concatenated_embedding.append(np.squeeze(new_embedding,axis=0))
        # print(concatenated_embedding,np.stack(concatenated_embedding, axis=0) )
    poincare_embeddings_final = np.stack(concatenated_embedding, axis=0)

    train_poincare_tensor = torch.tensor(poincare_embeddings_final,dtype=torch.float)
    difficulty_tensor = torch.tensor(difficulty_level_vectors,dtype=torch.float)
    print(np.linalg.norm(concatenated_embedding[0]),train_poincare_tensor.shape, difficulty_tensor.shape)
    
    with torch.no_grad():
        outputs = model(input_ids,attention_masks,train_poincare_tensor,difficulty_tensor )
        prediction = np.argmax(outputs,axis=1).flatten()
    return get_labels(prediction)

