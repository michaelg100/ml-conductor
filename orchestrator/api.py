from ninja import Router

from orchestrator.online_controller import OnlineOrcaService
from orchestrator.types import *

router = Router()

# Online model service call 
@router.post("/orchestration/serve", response=RetreivalResponseT)
def orchestration_online_service(request, payload: RetreivalT):
    res = OnlineOrcaService.retrieve(payload)
    return res