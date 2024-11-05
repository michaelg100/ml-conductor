from feature_logger.models import *
from feature_logger.types import *


class FeatureLoggerService:

    @classmethod
    def log(cls, feature_log_data: FeatureLogT) -> None:
        FeatureLog.objects.create(data=feature_log_data.data)