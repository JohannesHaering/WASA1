import unittest

from domain.machinelearning.ModelInfo import ModelInfo
from domain.machinelearning.ModelStats import ModelStats
from infrastructure.Modelmanager import ModelManager
from domain.machinelearning.ModelSchema import ModelSchema, ModelUsageSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestModelManager(unittest.TestCase):

    def setUp(self) -> None:
        self.engine = create_engine("postgresql://postgres:12@localhost:5432/dev_ms_classifier")
        Session = sessionmaker(bind=self.engine)
        session = Session()
        # delete existing
        session.query(ModelUsageSchema).delete()
        session.query(ModelSchema).delete()
        # add new
        model = ModelSchema(modelName='model1', modelPath='test/model1', usedFilter='filter1')
        session.add(model)
        session.flush()
        classifier = ModelUsageSchema(modelName=model.modelName,
                                      startTimestamp=0)
        session.add(classifier)

        session.commit()
        session.close()
        self.manager: ModelManager = ModelManager()

    def testGetModelPath(self) -> None:
        result: str = self.manager.getModelInfo("model1").path
        self.assertEqual("test/model1", result)

    def testGetModelNone(self) -> None:
        result: str = self.manager.getModelInfo('test')
        self.assertIsNone(result)

    def testUniqueNameTester(self) -> None:
        result:  bool = self.manager.checkUniqueModelName('model1')
        self.assertFalse(result)
        result: bool = self.manager.checkUniqueModelName('jumper')
        self.assertTrue(result)

    def testAddModel(self) -> None:
        result: bool = self.manager.addModel('test1', 'test/test1', 'filter2')
        self.assertTrue(result)
        modelName: str = self.manager.getModelInfo('test1').name
        self.assertEqual('test1', modelName)

    def testReportClassification(self) -> None:
        count: int = self.manager.getModelStats('model1').hits
        result: bool = self.manager.reportClassification('model1')
        self.assertTrue(result)
        new: int = self.manager.getModelStats('model1').hits
        self.assertEqual(count + 1, new)

    def testReportMiss(self) -> None:
        result: bool = self.manager.reportMiss(20)
        self.assertTrue(result)
        stats: ModelStats = self.manager.getModelStats('model1')
        self.assertEqual(1, stats.misses)

    def testDeleteModel(self) -> None:
        self.manager.addModel('test', 'test/test', 'filter4')
        model: ModelInfo = self.manager.getModelInfo('test')
        self.assertEqual('test', model.name)
        self.manager.deleteModel('test')
        result: ModelInfo = self.manager.getModelInfo('test')
        self.assertIsNone(result)

    def testGetModels(self) -> None:
        result = self.manager.getModels()
        self.assertEqual(['model1'], result)

    def testGetCurrentClassifier(self) -> None:
        result = self.manager.getCurrentClassifier()
        self.assertEqual('model1', result)

    def testStartModelUsage(self) -> None:
        timestamp: int = 30
        model: ModelInfo = ModelInfo('test', 'test/test', 'filter3')
        self.manager.addModel(model.name, model.path, model.filter)
        active: bool = self.manager.isModelActive(model.name)
        self.assertFalse(active)
        self.manager.startModelUsage(model.name, timestamp)
        active2: bool = self.manager.isModelActive(model.name)
        self.assertTrue(active2)
        current: str = self.manager.getCurrentClassifier()
        self.assertEqual(current, model.name)

        Session = sessionmaker(bind=self.engine)
        session = Session()
        activity: list[ModelUsageSchema] = session.query(ModelUsageSchema)\
            .filter_by(modelName='model1').all()
        dateFound: bool = False
        for entry in activity:
            if entry.endTimestamp == timestamp:
                dateFound = True
        self.assertTrue(dateFound)

    def tearDown(self) -> None:
        Session = sessionmaker(bind=self.engine)
        session = Session()
        session.query(ModelUsageSchema).delete()
        session.query(ModelSchema).delete()
        session.commit()
        self.manager = None


if __name__ == '__main__':
    unittest.main()
