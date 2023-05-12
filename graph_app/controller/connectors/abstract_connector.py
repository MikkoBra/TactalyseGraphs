from abc import ABC, abstractmethod


class AbstractConnector(ABC):
    @abstractmethod
    def get_data(self, param_map):
        pass
