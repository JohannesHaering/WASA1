from api.Manager import Manager
from utils.Exceptions import InvalidArgumentsException, NotFoundException, InternalServerError, ConflictException, \
    InvalidUsage

from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS

apirouter = Blueprint('api', __name__)

class API:

    @apirouter.route('/classify', methods=['POST'])
    def classify():
        req_data = request.get_json()
        try:
            return jsonify(Manager().classify(req_data))
        except InternalServerError as err:
            raise InvalidUsage(str(err), err.errorCode)
        except ConflictException as err:
            raise InvalidUsage(str(err), err.errorCode)
        except InvalidArgumentsException as err:
            raise InvalidUsage(str(err), err.errorCode)

    @apirouter.route('/misclassification', methods=['POST'])
    def reportMisclassification():
        req_data = request.get_json()
        try:
            return Manager().reportMisclassification(req_data)
        except InternalServerError as err:
            raise InvalidUsage(str(err), err.errorCode)
        except InvalidArgumentsException as err:
            raise InvalidUsage(str(err), err.errorCode)

