import numpy as np
import pandas as pd
import torch
from pytorch_transformers import *
import gensim
from gensim.utils import simple_preprocess
from gensim import corpora, models
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer

from gensim.parsing.preprocessing import STOPWORDS
from sklearn.decomposition import LatentDirichletAllocation
import gzip
import pickle
from pke.base import LoadFile
from sklearn.metrics.pairwise import cosine_similarity
from main.embedding.embedding import UseEmbedding
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

pathData = os.path.join(dir_path, '../data')

lo_data = pd.read_csv(pathData+"/lo-class-10-physics.csv")

def get_tokenized_sent(doc):  
    document = LoadFile()
    document.load_document(input=doc,
        language='en',
        normalization='stemming')
    texts = []
    text = []

    # loop through sentences
    for sentence in document.sentences:
        # get the tokens (stems) from the sentence if they are not
        # punctuation marks 
        text.extend([sentence.stems[i] for i in range(sentence.length)
                    if sentence.pos[i] != 'PUNCT' and
                    sentence.pos[i].isalpha()])

    # add the document to the texts container
    texts.append(' '.join(text))
    return texts

def run(text, tokenized_text, lda_model, dictionary, single_text = False, only_dist =False):
    # doc = nlp(text)
    # for sentence in doc.sents:
    use_encoder = UseEmbedding(None)

    stoplist = stopwords.words('english')
    tf_vectorizer = CountVectorizer(stop_words=stoplist,
                                    vocabulary=dictionary)
    if single_text:
        all_docs = tokenized_text
    else:
        all_docs = tokenized_text['learning_objectives'].values
    

    tf_idf = tf_vectorizer.fit_transform(all_docs)

    # compute the topic distribution over the document
    distribution_topic_document = lda_model.transform(tf_idf)
    if only_dist:
        return distribution_topic_document

    # compute the word distributions over topics
    distributions = lda_model.components_ / lda_model.components_.sum(axis=1)[:,
                                        np.newaxis]

    

    if single_text==False:
        embeddings = use_encoder.get_tokenized_sents_embeddings_USE(all_docs)
    else:
        embeddings = use_encoder.get_tokenized_sents_embeddings_USE([text])
    importance_lda = 8
    

    text_emb = embeddings
    lemmatizer =  WordNetLemmatizer()
    K = len(distribution_topic_document)
    distribution_topic_document = distribution_topic_document
    vectors_lda_USE = np.hstack((distribution_topic_document ,  text_emb))
    # term_embeddings = np.c_[word_vectors ,  phrase_embs]
    vectors_lda_USE = vectors_lda_USE.squeeze()

    # print("text_emb",vectors_lda_USE.shape)
    
    # print("phrase_embs", term_embeddings.shape)
    return vectors_lda_USE


def load_lda_model():
    model = LatentDirichletAllocation()
    with gzip.open(pathData+'/Models/Unsupervised/lda/ExtraMarksExpansion_lda.gz', 'rb') as f:
        (dictionary,
         model.components_,
         model.exp_dirichlet_component_,
         model.doc_topic_prior_) = pickle.load(f)
    return model, dictionary

def get_top_sentences(text):
    lda_model, dictionary = load_lda_model()
    new_emb = run(text,get_tokenized_sent(text), lda_model, dictionary, single_text=True)
    # new_emb = new_emb.reshape(1,-1)
    article_emb = run(lo_data,lo_data, lda_model, dictionary)
    threshold=0.39
    print("new_emb", new_emb.shape, article_emb.shape)
    text_sims = cosine_similarity(article_emb,[new_emb]).tolist()
    print("text_sims",text_sims)
    results = zip(range(len(text_sims)), text_sims)
    sorted_similarities = sorted(results, key=lambda x: x[1], reverse=True)
    print("text_sims",sorted_similarities)
    top_sentences = []
    for idx, item in sorted_similarities:
        if text_sims[idx][0] >= threshold:
            top_sentences.append(lo_data["learning_objectives"].values[idx])
        else:
            continue
    return top_sentences[:3]

