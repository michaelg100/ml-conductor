from django.test import TestCase
from ninja.testing import TestClient

from feature_logger.api import router
from feature_logger.controller import FeatureLoggerService
from feature_logger.models import *
from feature_logger.types import *


class TestFeatureLogger(TestCase):
    """ Test the controller for feature service """

    def test_log(self):
        FeatureLoggerService.log(FeatureLogT(data={"test": "test", "score": 1.0}))
        res = FeatureLog.objects.first()
        self.assertEqual(
            res.data,
            {"test": "test", "score": 1.0}
        )


class TestAPI(TestCase):
    """ Test the APIs for Feature Service"""

    def setUp(self):
        self.client = TestClient(router)

    def test_flow(self):
        # create feature store
        input = FeatureLogT(
            data={"test": "test", "score": 1.0}
        )
        response = self.client.post(
            "/upload",
            json=input
        )
        res = FeatureLog.objects.first()
        self.assertEqual(
            res.data,
            {"test": "test", "score": 1.0}
        )