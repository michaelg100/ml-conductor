from ninja import Router
from ninja.responses import Response
from http import HTTPStatus

from feature_service.controller import FeatureService
from feature_service.models import *
from feature_service.types import *

router = Router()

# Feature Store Create
@router.post("/store/create", response=FeatureStoreCreationResponseData)
def create_feature_store(request, payload: FeatureStoreCreation):
    res = FeatureService.feature_store_creation(input=payload)
    return FeatureStoreCreationResponseData(success=res)

# Feature Create
@router.post("/feature/create", response=FeatureCreationResponseData)
def create_feature(request, payload: FeatureCreation):
    res = FeatureService.feature_creation(input=payload)
    return FeatureCreationResponseData(success=res)

# Feature Upload Data
@router.post("/feature/upload")
def upload_feature(request, payload: FeatureDataUpload):
    FeatureService.upload_feature(input=payload)
    return Response(data={'upload': 'successful'}, status=HTTPStatus.OK)

# Fetch Features
@router.post("/feature/fetch", response=FeatureFetchResponse)
def fetch_features(request, payload: FetchFeatures):
    res = FeatureService.fetch(input=payload)
    return res

# View Feature Metadata
@router.get("/feature/feature-metadata", response=List[FeatureMetadataT])
def show_feature_metadata(request):
    return FeatureMetadata.objects.all()

# View Feature Stores
@router.get("/feature/feature-store-metadata", response=List[FeatureStoreT])
def show_feature_metadata(request):
    return FeatureStore.objects.all()