from ...graph_generator.factories.graph_factory import GraphFactory


class GraphConnector:
    def get_data(self, param_map):
        return self.create_graph(param_map)

    def create_graph(self, param_map):
        """
        Function that retrieves a drawn radio chart for further use.

        :param param_map:
        :return: The radio chart drawn based on passed parameters, in byte form.
        """
        factory = GraphFactory()
        plot_obj = factory.create_instance(param_map)
        plot = plot_obj.draw_all(param_map)
        return plot
