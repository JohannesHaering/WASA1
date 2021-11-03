from sklearn import svm
import pickle
import os

import config as cfg

class ModelStorage:
    
    @staticmethod
    def loadModel(modelpath: str) -> svm.OneClassSVM:
        svm = pickle.load(open(modelpath, 'rb'))
        return svm

    @staticmethod
    def saveModel(modelName: str, model: svm.OneClassSVM) -> str:
        modelDirectory = cfg.modelspath
        if not os.path.exists(modelDirectory):
            os.makedirs(modelDirectory)
        modelPath = os.path.join(modelDirectory, modelName,)
        pickle.dump(model, open(modelPath, 'wb'))
        return modelPath

    @staticmethod
    def deleteModel(modelpath: str) -> None:
        if not os.path.exists(modelpath):
            return
        os.remove(modelpath)