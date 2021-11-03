from domain.machinelearning.Filter import Filter
from domain.machinelearning.Classification import Classification
from service.Modelstorage import ModelStorage
from domain.loggingdata.LoggingData import LoggingData

from sklearn import svm


class Executer:

    def __init__(self, filtername: str, modelpath: str):
        self.filterName = filtername
        self.model = ModelStorage.loadModel(modelpath)

    def classify(self, loggingData: LoggingData) -> Classification:
        values = Filter.filter(self.filterName, loggingData)
        classifications = self.model.predict([values])
        if classifications[0] == 1:
            return Classification.ATTACK

        return Classification.HARMLESS
