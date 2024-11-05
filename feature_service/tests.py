from django.test import TestCase
from ninja.errors import HttpError
from ninja.testing import TestClient
from unittest.mock import ANY

from feature_service.api import router
from feature_service.models import Features
from feature_service.controller import FeatureService
from feature_service.test_utils.fixtures import *
from feature_service.types import *


class TestFeatureService(TestCase):
    """ Test the controller for feature service """

    def test_match_datatype(self):
        res = FeatureService._match_datatype(1)
        self.assertEqual("STRING", res)

    def test_update_feature_rows_with_new_feature(self):
        feature_store = "test_store"
        feature_name = "test"
        data = {"don": "don"}
        feature = create_feature(
            feature_store=feature_store,
            data=data,
            entity_id=1
        )
        FeatureService._update_feature_rows_with_new_feature(
            feature_name=feature_name,
            feature_store=feature.feature_store
        )
        res = Features.objects.filter(entity_id=1).values_list("features", flat=True)[0]
        self.assertEqual(res, {**data, feature_name: None})

    def test_feature_creation(self):
        store_name = "test_store"
        feature_name = "test_feature"
        input = FeatureCreation(
            feature_name=feature_name,
            feature_store=store_name,
            feature_description="nada",
            datatype=FeatureTypes.string.value
        )
        # test when store doesnt exist
        self.assertRaises(
            HttpError,
            lambda: FeatureService.feature_creation(input)
        )
        # test when store exists
        feature_store = create_feature_store(store_name)
        FeatureService.feature_creation(input)
        self.assertTrue(
            FeatureMetadata.objects.filter(
                feature_store=feature_store,
                feature_name=feature_name
            ).exists()
        )

    def test_feature_store_creation(self):
        input = FeatureStoreCreation(
            store_name="test_store",
            description="test description"
        )
        res = FeatureService.feature_store_creation(input)
        self.assertEqual(
            res,
            1
        )

    def test_update_feature_value(self):
        store_name = "test_store"
        feature_name = "test_feature"
        input = FeatureCreation(
            feature_name=feature_name,
            feature_store=store_name,
            feature_description="nada",
            datatype=FeatureTypes.string.value
        )
        feature_store = create_feature_store(store_name)
        # Test first time upload for a id that doesnt exist yet
        self.assertIsNone(
            Features.objects.all().first()
        )
        FeatureService.feature_creation(input)
        feature_data_input = {feature_name: "test val"}
        input = FeatureDataUpload(
            feature_store=store_name,
            entity_id=1,
            values=feature_data_input
        )
        FeatureService.upload_feature(input)
        res = Features.objects.filter(feature_store=feature_store, entity_id=1).first()
        self.assertEqual(
            res.features,
            feature_data_input
        )
        # test updating an feature id that already exists
        feature_data_input2 = {feature_name: "test val"}
        input2 = FeatureDataUpload(
            feature_store=store_name,
            entity_id=1,
            values=feature_data_input2
        )
        FeatureService.upload_feature(input2)
        res = Features.objects.filter(feature_store=feature_store, entity_id=1).first()
        self.assertEqual(
            res.features,
            feature_data_input2
        )
        # test when value isnt correct type
        feature_data_input3 = {feature_name: 123}
        input3 = FeatureDataUpload(
            feature_store=store_name,
            entity_id=1,
            values=feature_data_input3
        )
        self.assertRaises(
            HttpError,
            lambda: FeatureService.upload_feature(input3)
        )

    def test_fetch_features(self):
        store_name = "test_store"
        feature_name = "test_feature"
        create_feature(feature_store=store_name, data={feature_name: "test", "two": 1, "three": 3})
        fetch = FetchFeatures(
            fetchables=[FetchFormat(
                feature_store=store_name,
                features=[feature_name, "three"],
                entity_ids=[1]
            )]
        )
        res = FeatureService.fetch(fetch)
        self.assertEqual(
            res.data[0].data,
            [{"entity_id": 1, "test_feature": "test", "three": 3}]
        )


class TestFeatureServiceAPI(TestCase):
    """ Test the APIs for Feature Service"""

    def setUp(self):
        self.client = TestClient(router)

    def test_flow(self):
        # create feature store
        input = FeatureStoreCreation(
            store_name="test_store",
            description="test description"
        )
        response = self.client.post(
            "/store/create",
            json=input
        )
        self.assertEqual(
            response.json()["success"],
            1
        )
        # create feature
        input = FeatureCreation(
            feature_name="test_feature",
            feature_store="test_store",
            datatype=FeatureTypes.string.value,
            feature_description="test description",
            data_source="ads"
        )
        response = self.client.post(
            "/feature/create",
            json=input
        )
        self.assertEqual(
            response.json()["success"],
            1
        )
        # show feature metadata
        response = self.client.get(
            "/feature/feature-metadata"
        )
        self.assertEqual(
            response.json(),
            [
                {
                    "feature_name": "test_feature",
                    "feature_store": {"feature_store_name": "test_store"},
                    "datatype": "STRING",
                    "description": None
                }
            ]
        )
        # show feature store metadata
        response = self.client.get(
            "/feature/feature-store-metadata"
        )
        self.assertEqual(
            response.json(),
            [
                {
                    "feature_store_name": "test_store",
                    "description": "test description",
                    "created": ANY
                }
            ]
        )
        # add feature data
        input = FeatureDataUpload(
            feature_store="test_store",
            entity_id=1,
            values={"test_feature": "testttt"}
        )
        response = self.client.post(
            "/feature/upload",
            json=input
        )
        # fetch feature
        input = FetchFeatures(
            fetchables=[FetchFormat(
                feature_store="test_store",
                features=["test_feature"],
                entity_ids=[1]
            )]
        )
        response = self.client.post(
            "/feature/fetch",
            json=input
        )
        self.assertEqual(
            response.json(),
            {"data": [{"table": "test_store", "data": [{"entity_id": 1, "test_feature": "testttt"}]}]}
        )