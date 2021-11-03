import time

from domain.machinelearning.ModelInfo import ModelInfo
from domain.machinelearning.ModelSchema import ModelSchema, ModelUsageSchema
from domain.machinelearning.ModelStats import ModelStats
import config as cfg

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from sqlalchemy import and_, or_
from utils.Exceptions import InvalidArgumentsException, NotFoundException


class ModelManager:

    def __init__(self):
        engine = create_engine(
            "postgresql://{}:{}@{}:{}/{}".format(cfg.postgresql["databaseuser"], cfg.postgresql["password"],
                                                 cfg.postgresql["databaseip"], cfg.postgresql["port"],
                                                 cfg.postgresql["databasename"]))
        self.Session = sessionmaker(bind=engine)

    """
    increase amount of classifications performed by active model
    """

    def reportClassification(self, modelName: str) -> bool:
        session = self.Session()
        try:
            model = session.query(ModelSchema).filter_by(modelName=modelName).first()
            model.totalClassifications += 1
            session.commit()
            session.close()
            return True

        except SQLAlchemyError as err:
            session.rollback()
            session.close()
            raise err

    """
    Update model statistic that there was a wrong classification
    """

    def reportMiss(self, timestamp: int) -> bool:
        session = self.Session()
        try:
            modelName = self.__determineModel(timestamp)
            if not modelName:
                session.commit()
                session.close()
                return False

            model: ModelSchema = session.query(ModelSchema).filter_by(modelName=modelName).first()
            model.misses += 1
            session.commit()
            session.close()
            return True
        except SQLAlchemyError as err:
            session.rollback()
            session.close()
            raise err

    """
    Create a new machine learning model using given features
    """

    def addModel(self, modelName: str, modelPath: str, filterName: str) -> bool:
        session = self.Session()
        try:
            model: ModelSchema = ModelSchema(modelName=modelName, modelPath=modelPath, usedFilter=filterName)
            session.add(model)
            session.commit()
            session.close()
            return True
        except SQLAlchemyError as err:
            session.rollback()
            session.close()
            raise err

    """
    Delete the model specified with this name
    """

    def deleteModel(self, modelName: str) -> bool:
        session = self.Session()
        try:
            modelusages = session.query(ModelUsageSchema).filter_by(modelName=modelName).all()

            for modelusage in modelusages:
                session.delete(modelusage)

            model = session.query(ModelSchema).filter_by(modelName=modelName).first()
            session.delete(model)
            session.commit()
            session.close()
            return True
        except SQLAlchemyError as err:
            session.rollback()
            session.close()
            raise err

    """
    activate a model
    """

    def startModelUsage(self, modelName: str, timestamp: int) -> bool:
        session = self.Session()
        try:
            current: ModelUsageSchema = session.query(ModelUsageSchema). \
                order_by(desc(ModelUsageSchema.startTimestamp)).first()
            if current:
                current.endTimestamp = timestamp
            new: ModelUsageSchema = ModelUsageSchema(modelName=modelName,
                                                     startTimestamp=timestamp)
            session.add(new)
            session.commit()
            session.close()
            return True
        except SQLAlchemyError as err:
            session.rollback()
            session.close()
            raise err

    """
    Return the stats of a model, returns None if model was not found
    """

    def getModelStats(self, modelName: str) -> ModelStats:
        model: ModelSchema = self.__getModel(modelName)
        if not model:
            return None
        return ModelStats(model.totalClassifications - model.misses, model.misses)

    """
    Return information about model, returns None if model was not found
    """

    def getModelInfo(self, modelName: str) -> ModelInfo:
        model: ModelSchema = self.__getModel(modelName)
        if not model:
            return None
        return ModelInfo(model.modelName, model.modelPath, model.usedFilter)

    """
    Get all information about the model with the given model name, returns None in case
    there is no model with this name
    """

    def __getModel(self, modelName: str) -> ModelSchema:
        session = self.Session()
        result: ModelSchema = session.query(ModelSchema).filter_by(modelName=modelName).first()
        session.close()
        return result

    """
    Check whether name is unique, if not return False
    """

    def checkUniqueModelName(self, modelName: str) -> bool:
        session = self.Session()
        result = session.query(ModelSchema).filter_by(modelName=modelName).all()
        session.close()
        return not result

    """
    Get the names of all existing models
    """

    def getModels(self) -> list[str]:
        session = self.Session()
        try:
            models: list[tuple] = session.query(ModelSchema).all()
            result: list[str] = []
            for entry in models:
                result.append(entry.modelName)
            session.close()
            return result
        except SQLAlchemyError as err:
            session.close()
            raise err

    """
    get the name of the model which is currently classifying 
    """

    def getCurrentClassifier(self) -> str:
        modelName = self.__determineModel(int(round(time.time() * 1000)))
        return modelName

    """
    check whether model is currently active as classifier
    """

    def isModelActive(self, modelName: str) -> bool:
        model: ModelInfo = self.getModelInfo(modelName)
        current: str = self.getCurrentClassifier()
        return model.name == current

    """
    determine name of model that was active at that time
    returns None if no model was active at that time 
    """

    def __determineModel(self, timestamp: int) -> str:
        now: int = int(round(time.time() * 1000))
        if timestamp > now:
            raise InvalidArgumentsException("Error: timestamp has to come from the past.")
        session = self.Session()
        result: ModelUsageSchema = session.query(ModelUsageSchema).filter(and_(
            ModelUsageSchema.startTimestamp <= timestamp,
            (or_(ModelUsageSchema.endTimestamp > timestamp, ModelUsageSchema.endTimestamp == None)))).first()
        session.close()
        if not result:
            return None
        return result.modelName
