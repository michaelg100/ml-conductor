from ninja import NinjaAPI

from feature_service.api import router as FeatureServiceRouter
from feature_logger.api import router as FeatureLoggerRouter

api = NinjaAPI()

# Version 1
api.add_router("/feature-service/", FeatureServiceRouter)
api.add_router("/feature-logger/", FeatureLoggerRouter)