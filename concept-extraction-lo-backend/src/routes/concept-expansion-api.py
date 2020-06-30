from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint

from main.bayes_opt_flag_tuning import Bayesopt
from main.mlrose_simulated_annealing import SimulatedAnnealing
from main.read_important_flags import read_tunable_flags

REQUEST_API = Blueprint('request_api', __name__)

bayesopt = Bayesopt()
annealing = SimulatedAnnealing()
def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API

@REQUEST_API.route('/concept/extract', methods=['POST'])
def extract_keyphrases():
    """triggers code to tune jvm parameters
    """
    if not request.files:
        abort(400)
    body = request.files["document"]
    best_params, best_values = bayesopt.run_trials(body,_workload, _metric, benchmark)
    
    return jsonify({"best_params":(best_params), "best_values": best_values})

@REQUEST_API.route('/tunejvm/annealing/<string:_workload>/<string:_metric>/<string:benchmark>', methods=['POST'])
def tune_params_mlrose(_workload, _metric, benchmark):
    """triggers code to tune jvm parameters
    """
    if not request.get_json():
        abort(400)
    body = request.get_json(force = True)
    best_params, best_values = annealing.run_trials(body,_workload, _metric, benchmark)
    
    return jsonify({"best_params":','.join(str(x) for x in best_params),"best_values": best_values})