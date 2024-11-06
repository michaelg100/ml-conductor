from abc import ABC, abstractmethod
from typing import Any, Dict
from feature_service.types import Feature, FeatureFetchResponse


class MLModelCaller(ABC):
    """ For primarily creating something to call an ML Model"""

    @property
    def feature_types(self):
        """ Store the feature name -> serializable type """
        pass

    @abstractmethod
    def format_features(self) -> Dict[str, Any]:
        """ Serialize features """
        pass

    @abstractmethod
    def feature_mapper(self, feature_name: str, feature_value: Feature):
        """ Convert the feature into the type required by the model """
        pass

    @abstractmethod
    def serve(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """ Call external model service """
        pass


class TensorflowModelCaller(MLModelCaller):

    def __init__(self, features: FeatureFetchResponse) -> None:
        self.features = features

    @property
    def feature_types(self):
        return dict()
    
    def feature_mapper(self, feature_name: str, feature_value: Feature):
        if feature_type := self.feature_types.get(feature_name):
            return feature_type
        # convert to TF Type
        feature_type = str
        self.feature_types[feature_name] = feature_type
        return feature_type

    def format_features(self):
        formatted_features = []
        for feature_store in self.features.data:
            sub_data = []
            for features in feature_store.data:
                for name, value in features.items():
                    sub_data.append(
                        self.feature_mapper(feature_name=name, feature_value=value)
                    )
        return {
            "instances": formatted_features
        }

    def serve(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # requests.get TFX model
        # https://www.tensorflow.org/tfx/serving/api_rest
        return {"response": 1.0}


class ScikitModelCaller(MLModelCaller):

    def __init__(self, features: FeatureFetchResponse) -> None:
        self.features = features

    @property
    def feature_types(self):
        return dict()
    
    def feature_mapper(self, feature_name: str, feature_value: Feature):
        if feature_type := self.feature_types.get(feature_name):
            return feature_type
        # convert to Sickit Type
        feature_type = str
        self.feature_types[feature_name] = feature_type
        return feature_type

    def format_features(self):
        formatted_features = []
        for feature_store in self.features.data:
            sub_data = []
            for features in feature_store.data:
                for name, value in features.items():
                    sub_data.append(
                        self.feature_mapper(feature_name=name, feature_value=value)
                    )
        return {
            "instances": formatted_features
        }

    def serve(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # requests.get TFX model
        # https://www.tensorflow.org/tfx/serving/api_rest
        return {"response": 1.0}


class PytorchModelCaller(MLModelCaller):

    def __init__(self, features: FeatureFetchResponse) -> None:
        self.features = features

    @property
    def feature_types(self):
        return dict()
    
    def feature_mapper(self, feature_name: str, feature_value: Feature):
        if feature_type := self.feature_types.get(feature_name):
            return feature_type
        # convert to Pytorch Type
        feature_type = str
        self.feature_types[feature_name] = feature_type
        return feature_type

    def format_features(self):
        formatted_features = []
        for feature_store in self.features.data:
            sub_data = []
            for features in feature_store.data:
                for name, value in features.items():
                    sub_data.append(
                        self.feature_mapper(feature_name=name, feature_value=value)
                    )
        return {
            "instances": formatted_features
        }

    def serve(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # requests.get TFX model
        # https://www.tensorflow.org/tfx/serving/api_rest
        return {"response": 1.0}