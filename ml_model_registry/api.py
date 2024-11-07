from ninja import Router

from ml_model_registry.controller import ModelRegistryService
from ml_model_registry.models import *
from ml_model_registry.types import *

router = Router()

# Create model and expirement
@router.post("/model/expirement", response=MLModelExpirementSchema)
def create_model_expirement(request, payload: ModelExpirementInsertT):
    res = ModelRegistryService.upload_model_expirement(expirement=payload)
    return res

# fetch model
@router.get("/model/expirements", response=List[MLModelExpirementSchema])
def get_model_expirement(request):
    if hasattr(request, "query_params"):
        model_name = request.query_params.get("model_name")
        return ModelExpirementMetrics.objects.filter(model_name__icontains=model_name)
    return ModelExpirementMetrics.objects.all()

# Add Model Serving API URL
@router.patch("/model/api-serve-url", response=MLModelAPIURL)
def update_serving_api_url(request, payload: MLModelAPIURLUpdate):
    res = ModelRegistryService.add_serving_api_url(model_name=payload.model_name, api_url=payload.api_url)
    return MLModelAPIURL(result=res)