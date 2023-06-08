from abc import ABC, abstractmethod


class Service(ABC):
    """
    Abstract class providing a blueprint for a class that handles incoming request data, and passing it to "Connector"
    classes, which pass this data on to other modules.
    """

    @abstractmethod
    def json_process(self, payload):
        pass

    @abstractmethod
    def key_value_process(self, files, form):
        pass

    @abstractmethod
    def pass_data(self, param_map):
        pass
