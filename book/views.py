import json

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest

from book import models


bp = Blueprint('api', 'api', url_prefix='/')


@bp.route('/request', methods=['POST'])
def create_request():
    try:
        data = request.json
        email = data.get('email')
        title = data.get('title')
        id_ = models.add_request(email, title)
        return jsonify(models.get_request(id_)), 201
    except (AttributeError, BadRequest, json.decoder.JSONDecodeError):
        return "Request contained invalid JSON", 400
    except models.InvalidEmailError:
        return "Email address is invalid", 422
    except models.BookNotFoundError:
        return "No books with the specified title found", 404


@bp.route('/request/', methods=['GET'])
@bp.route('/request', methods=['GET'])
@bp.route('/request/<int:id_>', methods=['GET'])
def get_request(id_=None):
    if id_ is None:
        return jsonify(models.get_all_requests())
    else:
        try:
            return jsonify(models.get_request(id_))
        except models.RequestNotFoundError:
            return "No books with the specified title found", 404


@bp.route('/request/<int:id_>', methods=['DELETE'])
def delete_request(id_):
    try:
        models.delete_request(id_)
        return '', 204
    except models.RequestNotFoundError:
        return "No books with the specified title found", 404
