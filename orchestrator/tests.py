from django.test import TestCase
from ninja.testing import TestClient
from unittest.mock import ANY

from feature_service.test_utils.fixtures import create_feature
from ml_model_registry.test_utils.fixtures import create_model
from orchestrator.api import router
from orchestrator.online_controller import OnlineOrcaService
from orchestrator.models import *
from orchestrator.types import *


class TestOnlineOrcaService(TestCase):

    def test_retreive(self):
        # create model + features
        feature_1 = "feature_1"
        feature_2 = "feature_2"
        feature_store = "feature_store_1"
        model_name = "tfmodel"
        data = {
            feature_1: 1,
            feature_2: 2.0
        }
        create_feature(feature_store=feature_store, data=data)
        create_model(
            model_name=model_name,
            location="gcs://",
            feature_set={feature_store: [feature_1, feature_2]},
            description="lolll",
            api_url="https://www.example.com/tf/model/tfmodel/predict/"
        )
        # no extra input
        input = RetreivalT(
            ml_model_name=model_name,
            entity_ids={feature_store: [1]}
        )
        res = OnlineOrcaService.retrieve(input)
        self.assertEqual(
            res.response_object.response_object,
            {"result": 1.0}
        )

class TestOnlineOrcaAPI(TestCase):
    """ Test the APIs for Feature Service"""

    def setUp(self):
        self.client = TestClient(router)

    def test_flow(self):
        # create model + features
        feature_1 = "feature_1"
        feature_2 = "feature_2"
        feature_store = "feature_store_1"
        model_name = "tfmodel"
        data = {
            feature_1: 1,
            feature_2: 2.0
        }
        create_feature(feature_store=feature_store, data=data)
        create_model(
            model_name=model_name,
            location="gcs://",
            feature_set={feature_store: [feature_1, feature_2]},
            description="lolll",
            api_url="https://www.example.com/tf/model/tfmodel/predict/"
        )
        # no extra input
        input = RetreivalT(
            ml_model_name=model_name,
            entity_ids={feature_store: [1]}
        )
        response = self.client.post(
            "/orchestration/serve",
            json=input
        )
        self.assertEqual(
            response.json(),
            {
                'ml_model_name': 'tfmodel',
                'response_object': {'response_object': {'result': 1.0}, 'error_object': {}},
                'result_time': ANY
            }
        )
        
