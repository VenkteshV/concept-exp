from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
from main.extract_concepts import extract_concepts, expand_concepts
from main.bloom_verbs import extract_bloom_verbs, get_bloom_taxonomy

REQUEST_API = Blueprint('request_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API

@REQUEST_API.route('/concept/extract', methods=['POST'])
def concept():
    """triggers code to extract concepts
    """
    print("request*****", request.files)

    if not request.files:
        abort(400)
    body = request.files["document"]
    keyphrases = extract_concepts(body.read().decode("utf-8"))
    
    return jsonify({"keywords": keyphrases})

@REQUEST_API.route('/concept/expand', methods=['POST'])
def concept_expand():
    """triggers code to expand concepts
    """
    if not request.files:
        abort(400)
    body = request.files["document"]
    keyphrases = expand_concepts(body.read().decode("utf-8"))
    
    return jsonify({"keywords": keyphrases})



@REQUEST_API.route('/getbloomverbs/<string:skillname>', methods=['POST'])
def fetch_bloom_verbs(skillname):
    """triggers code to expand concepts
    """
    if not request.files:
        abort(400)
    body = request.files["document"]
    text = body.read().decode("utf-8")
    bloom_verbs = extract_bloom_verbs(text,skillname)

    return jsonify({"bloomverbs": bloom_verbs})



@REQUEST_API.route('/getcognitivetaxonomy', methods=['POST'])
def get_cognitive_complexity():
    """triggers code to expand concepts
    """
    if not request.files:
        abort(400)
    body = request.files["document"]
    text = body.read().decode("utf-8")
    bloom_verbs = get_bloom_taxonomy(text)

    return jsonify({"bloomtaxonomy": bloom_verbs})