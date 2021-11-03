class Misclassification:

    def __init__(self, timestamp, correctClassification, features):
        self.timestamp = timestamp
        self.correctClassification = correctClassification
        self.features = features
