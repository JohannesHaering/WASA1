from domain.machinelearning.Filter import Filter
from domain.machinelearning.Classification import Classification
from service.Modelstorage import ModelStorage
from domain.loggingdata.LoggingData import LoggingData
from domain.loggingdata.LoggingDataStorage import LoggingDataStorage
import config as cfg

import numpy as np
from sklearn import svm


class Trainer:

    def __init__(self, modelName: str, filterName: str) -> (str, float):
        self.modelName = modelName
        self.filterName = filterName
        self.loggingDataStorage = LoggingDataStorage(cfg.trainingsdatapath)

    def train(self) -> float:
        trainingsset = self.loggingDataStorage.getTrainingSet()
        filtered = Filter.filter(self.filterName, trainingsset[0])
        filtered = Filter.filter(self.filterName, trainingsset[0])
        trainingData = np.array(list(
            [Filter.filter(self.filterName, loggingData) for loggingData in self.loggingDataStorage.getTrainingSet()]))

        # model = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma='auto') #best 0.2785
        model = svm.OneClassSVM(nu=0.1, kernel="poly", gamma="auto")  # best 0.9
        model.fit(trainingData)

        modelpath = ModelStorage.saveModel(self.modelName, model)
        accuracy = self.__test(model)
        return modelpath, accuracy

    def __test(self, model: svm.OneClassSVM) -> float:
        testData = np.array(
            list([Filter.filter(self.filterName, loggingData) for loggingData in self.loggingDataStorage.getTestSet()]))
        testLabels = self.loggingDataStorage.getTestLabels()
        classifications = model.predict(testData)
        print(classifications)
        missCounter = 0
        for i in range(len(testLabels)):
            if classifications[i] != testLabels[i]:
                missCounter += 1
        print((len(testLabels) - missCounter) / len(testLabels))
        return (len(testLabels) - missCounter) / len(testLabels)
