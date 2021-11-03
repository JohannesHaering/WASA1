import sys

sys.path.insert(0, '../../service')

from domain.loggingdata.LoggingData import LoggingData

import math
import csv
import random


class LoggingDataStorage:
    trainingSetSplit = 0.6

    normaltraffic = 'BENIGN'
    DoSGoldenEye = 'DoS GoldenEye'
    DoSHulk = 'DoS Hulk'
    DoSSlowhttptest = 'DoS Slowhttptest'
    DoSslowloris = 'DoS slowloris'
    WebAttackBruteForce = 'Web Attack � Brute Force'
    WebAttackXSS = 'Web Attack � XSS'

    def __init__(self, dataPath: str):
        self.normalset: list[LoggingData] = []
        self.attackset: list[LoggingData] = []
        self.trainingSet: list[LoggingData] = []
        self.testSet: list[LoggingData] = []
        self.trainingLabels: list[float] = []
        self.testLabels: list[float] = []

        with open(dataPath, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['label'] == self.normaltraffic:
                    row.pop('label')
                    self.normalset.append(LoggingData(self.__checkDicForInvalidValues(row)))
                else:
                    row.pop('label')
                    self.attackset.append((LoggingData(self.__checkDicForInvalidValues(row))))

            self.trainingSet += random.sample(self.normalset, 4000)
            self.trainingLabels += [1] * 4000
            self.testSet += random.sample(self.normalset, 1000)
            self.testLabels += [1] * 1000
            self.testSet += random.sample(self.attackset, 1000)
            self.testLabels += [1] * 1000

    def __checkDicForInvalidValues(self, features: dict) -> dict:
        for key, value in features.items():
            try:
                f = float(value)
                if math.isinf(f) or math.isnan(f):
                    features[key] = '0'
            except ValueError:
                features[key] = '0'
        return features

    def getTrainingSet(self) -> list[LoggingData]:
        return self.trainingSet

    def getTrainingLabels(self) -> list[float]:
        return self.trainingLabels

    def getTestSet(self) -> list[LoggingData]:
        return self.testSet

    def getTestLabels(self) -> list[float]:
        return self.testLabels
