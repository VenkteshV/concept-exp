import pandas as pd
import os
import nltk
import pickle

import nltk.tokenize as tk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from main.bloom_verbs import extract_verbs
from main.bloom_verbs import get_wordnet_tag
dir_path = os.path.dirname(os.path.realpath(__file__))

pathData = os.path.join(dir_path, '../data')
wnl = WordNetLemmatizer()

def extract_bloom_verbs(templates, skillname):
    response = []
    for index, document in templates.iterrows():
        document_text = document["template_text"]
        print("dicument", document_text)

        sentences = tk.sent_tokenize(document_text)
        verbs_from_doc = []
        tokenized_sent = [tk.word_tokenize(sent) for sent  in sentences]
        pos_taggged = [nltk.pos_tag(sent) for sent in tokenized_sent]
        for tagged_sent in pos_taggged:
                verbs_from_doc.append(extract_verbs(r"VP: {<VB.*>$}", tagged_sent))

        verbs_from_doc = [ tokens  for verbs in verbs_from_doc for tokens in verbs]

        results =[]
        for word_tag_tuple in verbs_from_doc:
            lemmatized_word = wnl.lemmatize(word_tag_tuple[0], get_wordnet_tag(word_tag_tuple))
            results.append(lemmatized_word.lower()  )


        bloom_dict = open(pathData+"/bloom_taxonomy","rb")
        taxonomy_dict = pickle.loads(bloom_dict.read())
        verbs_for_skill = taxonomy_dict[skillname].split(",")
        for verbs in verbs_for_skill:
            if verbs.lower() in results:
                response.append(document)
    return response
    


    return response 
class LoTemplate():
        
    def get_templates(self,templates_df):    
        templates = []
        loObject = LoTemplate()
        print(templates_df)
        for row in templates_df:
            loTemplate = dict()
            loTemplate["label"] = row["template_text"]
            loTemplate["value"] = row["template_text"]
            templates.append(loTemplate)
        return templates


def get_lo_templates(skillname):
    pathData = os.path.join(dir_path, '../data')
    templates_df = pd.read_csv(pathData+"/lo-templates.csv")
    loObject = LoTemplate()
    templates = extract_bloom_verbs(templates_df, skillname)
    templates = loObject.get_templates(templates)

    return templates

if __name__=="__main__":
    print(get_lo_templates("Understanding"), len(get_lo_templates("Understanding")))

