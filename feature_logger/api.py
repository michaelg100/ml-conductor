from ninja import Router
from ninja.responses import Response
from http import HTTPStatus

from feature_logger.controller import FeatureLoggerService
from feature_logger.types import *

router = Router()

# Feature Log Upload Data
@router.post("/upload")
def upload_feature_log(request, payload: FeatureLogT):
    FeatureLoggerService.log(feature_log_data=payload)
    return Response(data={'upload': 'successful'}, status=HTTPStatus.OK)