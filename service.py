"""Entry point of our microservice. API endpoints (routes) are defined here.
 """

#pylint: disable=unused-import
import logging as log
import uuid
import json

from flask import Flask, request, jsonify, Response
from src import handlers, model

import os
import redis

# pylint: disable=invalid-name
app = Flask(__name__)


@app.route('/reservations', methods=['GET'])
def reservations():
    """ Get Reservations Endpoint"""
    flight_id = request.args.get('flight_id', '')
    resp = handlers.get_reservations(flight_id)
    return jsonify(resp)

@app.route('/reservations', methods=['PUT'])
def reserve():
    """Endpoint that reserves a seat for a customer"""
    json_body = request.get_json(force=True)
    resp = handlers.reserve(json_body)
    if resp.get("status") == "success":
        return jsonify(resp)

    return Response(
        json.dumps(resp),
        status=403,
        mimetype='application/json'
    )

@app.route('/reservations/ping', methods=['GET'])
def ping():
    """ Liveness probe """
    resp = {
        "status" : "pass"
    }
    return jsonify(resp)


@app.route('/reservations/health', methods=['GET'])
def health():
    """Readiness probe: verifica que el proceso y Redis estén funcionando"""
    try:
        # Nos conectamos directamente a Redis usando las variables de entorno
        r = redis.Redis(
            host=os.environ.get('REDIS_HOST', 'redis'),
            port=int(os.environ.get('REDIS_PORT', 6379)),
            socket_connect_timeout=2 # Si Redis no responde en 2 segs, falla
        )
        r.ping() # Envía un PING a Redis para verificar que está vivo
        return {"status": "pass", "details": {"redis": "ok"}}, 200
    except Exception as e:
        return {"status": "fail", "error": str(e)}, 503

def init():
    """Init routine for the microservice"""
    uuid.uuid1() # prime the uuid generator at startup

if __name__ == '__main__':
    init()

    app.run(debug=True, host='0.0.0.0')
