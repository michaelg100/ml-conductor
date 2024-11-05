from django.test import TestCase
from ninja.errors import HttpError
from ninja.testing import TestClient
from unittest.mock import ANY

from ml_model_registry.api import router
from ml_model_registry.controller import ModelRegistryService
from ml_model_registry.models import *
from ml_model_registry.types import *


class TestModelRegistryAPI(TestCase):
    """ Test the APIs for Feature Service"""

    def setUp(self):
        self.client = TestClient(router)

    def test_flow(self):
        # upload model expirement
        input = ModelExpirementInsertT(
            model_name="my ml model",
            location="s3://",
            model_description="test description",
            metrics={"cross": 1.3},
            feature_set=["feature a", "feature b"],
            target_field="cost",
            expirement_description="cost with adjusted data"
        )
        response = self.client.post(
            "/model/expirement",
            json=input
        )
        res1 = {
            'model': {
                'model_name': 'my ml model',
                'location': 's3://',
                'description': 'test description',
                'created': ANY
            }, 
            'metrics': {'cross': 1.3},
            'feature_set': ['feature a', 'feature b'],
            'target_field': 'cost',
            'description': 'cost with adjusted data'
        }
        self.assertEqual(
            response.json(),
            res1
        )
        # upload with only partial
        input2 = ModelExpirementInsertT(
            model_name="my ml model 2",
            location="s3://2",
        )
        response2 = self.client.post(
            "/model/expirement",
            json=input2
        )
        res2 = {
            'model': {
                'model_name': 'my ml model 2',
                'location': 's3://2',
                'description': None,
                'created': ANY
            }, 
            'metrics': None,
            'feature_set': None,
            'target_field': None,
            'description': None
        }
        self.assertEqual(
            response2.json(),
            res2
        )
        # should fail when submitting no unique model name or location
        self.assertRaises(
            HttpError,
            lambda: ModelRegistryService.upload_model_expirement(input2)
        )
        # get models
        response = self.client.get("/model/expirements")
        self.assertCountEqual(response.json(), [res1, res2])
