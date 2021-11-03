from infrastructure.Modelmanager import ModelManager
from infrastructure.ModelStatistic import ModelStatistic
from domain.machinelearning.Executer import Executer
from domain.machinelearning.Trainer import Trainer
from domain.machinelearning.Misclassification import Misclassification
from domain.machinelearning.Classification import Classification
from domain.machinelearning.Filter import Filter
from domain.loggingdata.LoggingData import LoggingData
from utils.Exceptions import InvalidArgumentsException, InternalServerError, NotFoundException, ConflictException
from service.Modelstorage import ModelStorage

import time
import os


class Manager:

    def __init__(self):
        self.modelManager = ModelManager()

    def reportMisclassification(self, misclassification: Misclassification) -> None:
        now: int = int(round(time.time() * 1000))
        if misclassification.timestamp > now:
            raise InvalidArgumentsException("Error: timestamp has to come from the past.")

        try:
            self.modelManager.reportMiss(misclassification.timestamp)
        except Exception as err:
            raise InternalServerError(str(err))

    def startTraining(self, modelName: str, filterName: str) -> float:
        try:
            unique = self.modelManager.checkUniqueModelName(modelName)
        except Exception as err:
            raise InternalServerError(str(err))

        if not unique:
            raise InvalidArgumentsException("Model with this name already exists")

        trainer = Trainer(modelName, filterName)
        (modelpath, accuracy) = trainer.train()
        try:
            self.modelManager.addModel(modelName, modelpath, filterName)
        except Exception as err:
            raise InternalServerError("Was not able to save model to database")

        return accuracy

    def classify(self, loggingData: LoggingData) -> Classification:
        try:
            currentModelName = self.modelManager.getCurrentClassifier()
        except Exception as err:
            raise InternalServerError(str(err))

        if currentModelName is None:
            raise ConflictException("No model deployed")

        try:
            modelInfo = self.modelManager.getModelInfo(currentModelName)
        except Exception as err:
            raise InternalServerError(str(err))

        executer = Executer(modelInfo.filter, modelInfo.path)

        try:
            self.modelManager.reportClassification(currentModelName)
        except Exception as err:
            raise InvalidArgumentsException(str(err))

        return executer.classify(loggingData)

    def switchModel(self, modelName: str) -> None:
        try:
            unique = self.modelManager.checkUniqueModelName(modelName)
        except Exception as err:
            raise InternalServerError(str(err))

        if unique:
            raise NotFoundException("Model with this name does not exist")

        timestamp = self.__createTimestamp()

        try:
            self.modelManager.startModelUsage(modelName, timestamp)
        except Exception as err:
            raise InternalServerError(str(err))

    def getStatistic(self, modelName: str) -> ModelStatistic:
        try:
            unique = self.modelManager.checkUniqueModelName(modelName)
        except Exception as err:
            raise InternalServerError(str(err))

        if unique:
            raise NotFoundException("Model with this name does not exist")

        try:
            modelstats = self.modelManager.getModelStats(modelName)
        except Exception as err:
            raise InternalServerError(str(err))

        return modelstats

    def deleteModel(self, modelName: str) -> None:
        try:
            unique = self.modelManager.checkUniqueModelName(modelName)
        except Exception as err:
            raise InternalServerError(str(err))

        if unique:
            return

        if self.isModelActive((modelName)):
            raise InvalidArgumentsException("Model is currently active")

        try:
            modelinfo = self.modelManager.getModelInfo(modelName)
            self.modelManager.deleteModel(modelName)
            ModelStorage.deleteModel(modelinfo.path)
        except Exception as err:
            raise InternalServerError(str(err))

    def getAvailableFilters(self) -> list:
        return Filter.getAvailableFilters()

    def getAvailableModels(self) -> list:
        try:
            return self.modelManager.getModels()
        except Exception as err:
            raise InternalServerError(str(err))

    def existsModelName(self, modelName: str) -> bool:
        try:
            return self.modelManager.checkUniqueModelName(modelName)
        except Exception as err:
            raise InternalServerError(str(err))

    def __createTimestamp(self) -> int:
        return int(round(time.time() * 1000))

    def isModelActive(self, modelName: str) -> bool:
        try:
            unique = self.modelManager.checkUniqueModelName(modelName)
        except Exception as err:
            raise InternalServerError(str(err))

        if unique:
            raise NotFoundException("Model with this name does not exist")

        try:
            return self.modelManager.isModelActive(modelName)
        except Exception as err:
            raise InternalServerError(str(err))
