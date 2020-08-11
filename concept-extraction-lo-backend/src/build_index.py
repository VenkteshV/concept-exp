from main.embedding.embedding import UseEmbedding
from annoy import AnnoyIndex
import gensim
import gzip
import os
from gensim.utils import simple_preprocess
from gensim import corpora, models 
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
import pickle
from main.fetch_lo import get_tokenized_sent
from sklearn.decomposition import LatentDirichletAllocation

dir_path = os.path.dirname(os.path.realpath(__file__))

from main.extract_concepts import extract_concepts

lo_data = pd.read_csv(dir_path+"/data/lo-class-10-physics.csv", sep="\n",engine="python")
print("number of learnign objectives are", lo_data.shape)

def get_embeddings_for_lo(tokenized_text, lda_model, dictionary):
    # doc = nlp(text)
    # for sentence in doc.sents:
    use_encoder = UseEmbedding(None)
    keywords_for_docs = []
    

    stoplist = stopwords.words('english')
    tf_vectorizer = CountVectorizer(stop_words=stoplist,
                                    vocabulary=dictionary)

    all_docs = tokenized_text['learning_objectives'].values

    # for doc in all_docs:
    #     keywords = extract_concepts(doc)
    #     keywords = [keyword[0] for keyword in keywords]
    #     keyword_text = ' '.join(keywords)
    #     keywords_for_docs.append(keyword_text)

    
    print("keywords_for_docs", all_docs)
    # tf_idf = tf_vectorizer.fit_transform(all_docs)

    # # compute the topic distribution over the document
    # distribution_topic_document = lda_model.transform(tf_idf)

    # # compute the word distributions over topics
    # distributions = lda_model.components_ / lda_model.components_.sum(axis=1)[:,
    #                                     np.newaxis]

    

    embeddings = use_encoder.get_tokenized_sents_embeddings_USE(all_docs)
    

    text_emb = embeddings
    # K = len(distribution_topic_document)
    # distribution_topic_document = distribution_topic_document
    # vectors_lda_USE = np.hstack((distribution_topic_document ,  text_emb))
    # term_embeddings = np.c_[word_vectors ,  phrase_embs]
    vectors_lda_USE = text_emb.squeeze()

    print("text_emb",vectors_lda_USE.shape)
    
    # print("phrase_embs", term_embeddings.shape)
    return vectors_lda_USE


def load_lda_model():
    model = LatentDirichletAllocation()
    with gzip.open(dir_path+'/data'+'/Models/Unsupervised/lda/ExtraMarksExpansion_lda.gz', 'rb') as f:
        (dictionary,
         model.components_,
         model.exp_dirichlet_component_,
         model.doc_topic_prior_) = pickle.load(f)
    return model, dictionary


def get_index(embedding_dim = 512, number_of_trees=100):
    ann = AnnoyIndex(embedding_dim, metric = "angular")
    lda_model, dictionary = load_lda_model()
    embeddings =  get_embeddings_for_lo(lo_data, lda_model, dictionary)
    for index, embed in enumerate(embeddings):
        ann.add_item(index, embed)
    ann.build(number_of_trees)
    ann.save(dir_path+"/data/lo.annoy")


if __name__=="__main__":
    print("enter embedding dimension")

    emb_dim = input()

    print("\n \n")
    print("enter number of trees")
    num_trees = input()

    get_index(int(emb_dim), int(num_trees))
