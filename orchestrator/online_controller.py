from orchestrator.types import *


class OnlineOrcha:

    @classmethod
    def retrieve(cls, prompt: RetreivalT) -> RetreivalResponseT:
        if prompt.caching:
            cls._check_cache()
        # fetch feature schema from model

        # fetch features

        # send to model

        # log model response

        # allow to cache response
        if prompt.caching:
            cls._store_cache()
        # return model response
        pass
    

    @classmethod
    def _check_cache(cls, ):
        pass

    @classmethod
    def _store_cache(cls, ):
        pass