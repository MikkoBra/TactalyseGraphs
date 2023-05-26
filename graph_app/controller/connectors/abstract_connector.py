from abc import ABC, abstractmethod


class AbstractConnector(ABC):
    """
    Class meant for communication between the API endpoints and the rest of the app. Should not do data processing, only
    whatever is necessary to facilitate data flow between modules. Each Connector should communicate with a specific
    module or serve a specific purpose.
    """

    @abstractmethod
    def get_data(self, param_map):
        """
        Function that passes data coming from an API request to a module, and returns whatever the module sends in
        response.

        :param param_map: Map containing key/value pairs representing input parameters.
        :return: The return value of whichever functions were called from other modules.
        """
        pass
