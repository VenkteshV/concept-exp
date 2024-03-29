import bert_serving.client as bert_as_a_service_encoders
from sentence_transformers import SentenceTransformer
import spacy
import stanfordnlp
from spacy_stanfordnlp import StanfordNLPLanguage

import main.embedding.embedding as embeddings
import main.extraction.extractor as extractors
import main.keyword_extraction.keyword_extractor as keyword_extractors
import main.rank.rank as ranks

import main.rank.coTagRank as coTagrank


class NLPs:
    SPACY = 'spacy'
    CORENLP = 'corenlp'


def init_nlp(config):
    if config.get('name') == NLPs.SPACY:
        return spacy.load(config.get('model_name'))
    elif config.get('name') == NLPs.CORENLP:
        return StanfordNLPLanguage(stanfordnlp.Pipeline(lang=config.get('model_name')))


def init_encoder(config):
    if hasattr(bert_as_a_service_encoders, config.get('class')):
        return getattr(bert_as_a_service_encoders, config.get('class'))(
            **config.get('kwargs')
        )
    elif config.get('class') == "SentenceTransformer":
        if config.get('kwargs', {}).get("model_name_or_path") in [
            "bert-base-nli-stsb-mean-tokens",
            "bert-large-nli-stsb-mean-tokens",
            "roberta-base-nli-stsb-mean-tokens",
            "roberta-large-nli-stsb-mean-tokens",
            "distilbert-base-nli-stsb-mean-tokens"
        ]:
            return SentenceTransformer(**config.get('kwargs'))
        else:
            raise ValueError(f"Incorrect SentenceTransformer configuration: {config}")
    else:
        raise ValueError(f"Incorrect Encoder configurations: {config}")


def init_keyword_extractor(config):
    nlp_config = config.get('nlp')
    encoder_config = config.get('encoder')
    extractor_config = config.get('extractor')
    embedding_config = config.get('embedding')
    rank_config = config.get('rank')

    nlp = init_nlp(nlp_config)

    if rank_config.get('class') == 'CoTagRank' or encoder_config.get('class') == 'EmbedRank' or encoder_config.get('class') == 'EmbedRankSentenceUSE':
    
        encoder = None #
    else:
        encoder = init_encoder(encoder_config)

    extractor = getattr(extractors, extractor_config.get('class'))(
        **{"nlp": nlp, **extractor_config.get('kwargs')}
    )
    embedding = getattr(embeddings, embedding_config.get('class'))(
        **{"encoder": encoder, **embedding_config.get('kwargs')}
    )
    if rank_config.get('class') == 'CoTagRank':
          rank = getattr(coTagrank, rank_config.get('class'))(
        **rank_config.get('kwargs')
    )
    else:
        rank = getattr(ranks, rank_config.get('class'))(
            **rank_config.get('kwargs')
        )
    keyword_extractor = getattr(keyword_extractors, config.get('class'))(
        phrase_extractor=extractor, embed=embedding, rank=rank
    )

    return keyword_extractor
