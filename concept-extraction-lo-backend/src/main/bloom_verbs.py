import nltk

import nltk.tokenize as tk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

pathData = os.path.join(dir_path, '../data')

wnl = WordNetLemmatizer()
from sklearn.metrics.pairwise import cosine_similarity

import pickle


def get_wordnet_tag(word_tag_tuple):
    
    if word_tag_tuple[1].startswith('J'):
        return wordnet.ADJ
    elif word_tag_tuple[1].startswith('V'):
        return wordnet.VERB
    elif word_tag_tuple[1].startswith('N'):
        return wordnet.NOUN
    elif word_tag_tuple[1].startswith('R'):
        return wordnet.ADV


def extract_verbs(regex, sentence):
    parser = nltk.RegexpParser(regex)
    verbs =  parser.parse(sentence) 
    results =[]
    for node in verbs.leaves():
       if "VB" in node[1] or "NN" in node[1]:
           print(node[1])
           results.append((node[0], node[1]))

    print(results)
    
    return results


def get_bloom_taxonomy(document):
    print("dicument", document)

    sentences = tk.sent_tokenize(document)
    verbs_from_doc = []
    tokenized_sent = [tk.word_tokenize(sent) for sent  in sentences]
    pos_taggged = [nltk.pos_tag(sent) for sent in tokenized_sent]
    for tagged_sent in pos_taggged:
            verbs_from_doc.append(extract_verbs(r"VP: {<VB.*>$}", tagged_sent))

    verbs_from_doc = [ tokens  for verbs in verbs_from_doc for tokens in verbs]

    print("verbs_from_doc", verbs_from_doc)
    results =[]
    for word_tag_tuple in verbs_from_doc:
        lemmatized_word = wnl.lemmatize(word_tag_tuple[0], get_wordnet_tag(word_tag_tuple))
        results.append(lemmatized_word)


    bloom_dict = open(pathData+"/bloom_taxonomy","rb")
    taxonomy_dict = pickle.loads(bloom_dict.read())

    response = []
    for cognitive_complexity, bloom_verb in taxonomy_dict.items():
        verbs = [ x.lower() for x in bloom_verb.split(",")]
        for verb in results:
            if verb.lower() in verbs:
                response.append(cognitive_complexity)

    return list(set(response))


def extract_bloom_verbs(document, skillname):
    print("dicument", document)

    sentences = tk.sent_tokenize(document)
    verbs_from_doc = []
    tokenized_sent = [tk.word_tokenize(sent) for sent  in sentences]
    pos_taggged = [nltk.pos_tag(sent) for sent in tokenized_sent]
    for tagged_sent in pos_taggged:
            verbs_from_doc.append(extract_verbs(r"VP: {<VB.*>$}", tagged_sent))

    verbs_from_doc = [ tokens  for verbs in verbs_from_doc for tokens in verbs]

    print("verbs_from_doc", verbs_from_doc)
    results =[]
    for word_tag_tuple in verbs_from_doc:
        lemmatized_word = wnl.lemmatize(word_tag_tuple[0], get_wordnet_tag(word_tag_tuple))
        results.append(lemmatized_word)


    bloom_dict = open(pathData+"/bloom_taxonomy","rb")
    taxonomy_dict = pickle.loads(bloom_dict.read())
    verbs_for_skill = taxonomy_dict[skillname].split(",")

    response = []
    for verbs in verbs_for_skill:
        if verbs.lower() in results:
            response.append(verbs.lower())  
    


    return response 
    



