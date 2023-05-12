from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def json_process(self, payload):
        pass

    @abstractmethod
    def key_value_process(self, files, form):
        pass

    @abstractmethod
    def pass_data(self, param_map):
        pass
