from api.Manager import Manager
from domain.machinelearning.ModelStats import ModelStats
from utils.Exceptions import InvalidArgumentsException, NotFoundException, InternalServerError, ConflictException, \
    InvalidUsage

import json
from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS

bffrouter = Blueprint('bff', __name__)


class BackendForFrontend:

    # API for model overview page

    @bffrouter.route('/models', methods=['GET'])
    def getAvailableModels() -> str:
        try:
            return jsonify(Manager().getAvailableModels())
        except InternalServerError as err:
            raise InvalidUsage(str(err), err.errorCode)

    @bffrouter.route('/models/<modelName>/isActive', methods=['GET'])
    def isModelActive(modelName: str) -> str:
        try:
            return jsonify(Manager().isModelActive(modelName))
        except InternalServerError as err:
            raise InvalidUsage(str(err), 500)
        except NotFoundException as err:
            raise InvalidUsage(str(err), 400)

    @bffrouter.route('/models/<modelName>', methods=['GET'])
    def getModelInformation(modelName: str) -> str:
        try:
            stats = Manager().getStatistic(modelName)
            return json.dumps(stats.__dict__)
        except InternalServerError as err:
            raise InvalidUsage(str(err), err.errorCode)
        except NotFoundException as err:
            raise InvalidUsage(str(err), err.errorCode)

    @bffrouter.route('/models/set/<modelName>', methods=['GET'])
    def changeModel(modelName: str) -> str:
        try:
            return jsonify(Manager().switchModel(modelName))
        except InternalServerError as err:
            raise InvalidUsage(str(err), err.errorCode)
        except NotFoundException as err:
            raise InvalidUsage(str(err), err.errorCode)

    # API for training page

    @bffrouter.route('/models/train', methods=['POST'])
    def trainModel() -> str:
        req_data = request.get_json()
        modelName = req_data['modelName']
        filterName = req_data['filterName']
        try:
            return jsonify(Manager().startTraining(modelName, filterName))
        except InternalServerError as err:
            raise InvalidUsage(str(err), err.errorCode)
        except InvalidArgumentsException as err:
            raise InvalidUsage(str(err), err.errorCode)

    @bffrouter.route('/models/<modelName>', methods=['DELETE'])
    def deleteModel(modelName: str) -> str:
        try:
            return jsonify(Manager().deleteModel(modelName))
        except InternalServerError as err:
            raise InvalidUsage(str(err), err.errorCode)
        except InvalidArgumentsException as err:
            raise InvalidUsage(str(err), err.errorCode)

    @bffrouter.route('/models/availability/<modelName>', methods=['GET'])
    def isModelNameUnique(modelName: str) -> str:
        try:
            return jsonify(Manager().existsModelName(modelName))
        except InternalServerError as err:
            raise InvalidUsage(str(err), err.errorCode)

    @bffrouter.route('/models/filters', methods=['GET'])
    def getAvailableFilters() -> str:
        try:
            return jsonify(Manager().getAvailableFilters())
        except InternalServerError as err:
            raise InvalidUsage(str(err), err.errorCode)

