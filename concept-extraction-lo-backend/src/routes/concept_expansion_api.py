from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
from main.extract_concepts import extract_concepts, expand_concepts

REQUEST_API = Blueprint('request_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API

@REQUEST_API.route('/concept/extract', methods=['POST'])
def concept():
    """triggers code to tune jvm parameters
    """
    print("request*****", request.files)

    if not request.files:
        abort(400)
    body = request.files["document"]
    keyphrases = extract_concepts(body.read().decode("utf-8"))
    
    return jsonify({"keywords": keyphrases})

@REQUEST_API.route('/concept/expand', methods=['POST'])
def concept_expand():
    """triggers code to tune jvm parameters
    """
    if not request.files:
        abort(400)
    body = request.files["document"]
    keyphrases = expand_concepts(body.read().decode("utf-8"))
    
    return jsonify({"keywords": keyphrases})