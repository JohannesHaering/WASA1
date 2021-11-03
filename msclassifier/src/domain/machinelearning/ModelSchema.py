from sqlalchemy import Column, String, Integer, DateTime, BigInteger
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

import config as cfg

Base = declarative_base()


class ModelSchema(Base):
    __tablename__ = 'model'

    modelName = Column(String, primary_key=True)
    modelPath = Column(String, nullable=False)
    totalClassifications = Column(Integer, default=0)
    misses = Column(Integer, default=0)
    usedFilter = Column(String, nullable=False)


class ModelUsageSchema(Base):
    __tablename__ = 'modelUsage'

    modelName = Column(String, ForeignKey('model.modelName'), primary_key=True)
    startTimestamp = Column(BigInteger, primary_key=True)
    endTimestamp = Column(BigInteger, default=None)


Base.metadata.create_all(
    create_engine("postgresql://{}:{}@{}:{}/{}".format(cfg.postgresql["databaseuser"], cfg.postgresql["password"],
                                                       cfg.postgresql["databaseip"], cfg.postgresql["port"],
                                                       cfg.postgresql["databasename"])))
