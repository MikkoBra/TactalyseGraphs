from .preprocessor import Preprocessor
from .randomizer import Randomizer
from ..excel_reader import ExcelReader


class LineProcessor(Preprocessor):
    """
    Class that handles data extraction and processing specific to line graphs. It allows for extracting the required
    stats to be graphed from an excel file, and for generating a map containing the parameters needed by the line graph
    module.
    """

    def __init__(self, *args, **kwargs):
        super(LineProcessor, self).__init__(*args, **kwargs)
        self.__randomizer = Randomizer()

    def get_columns_line_plots(self, player_pos):
        """
        Function that provides a list of headers to use for graphing the line plots.

        :param player_pos: Abbreviated position of the player whose stats to graph.
        :return: Pandas Series containing the required stats to graph.
        """
        stats_file = "graph_app/files/Stats per position.xlsx"
        stats_pd = ExcelReader().read_file(stats_file)
        stats_necessary = stats_pd[['Attribute', player_pos]]
        stats_necessary = stats_necessary[stats_necessary[player_pos] == 1.0]
        return stats_necessary['Attribute']

    def extract_line_data(self, param_map):
        """
        Function that takes information of the player from the passed parameter map, and generates a map containing
        data processed for use by the graph module.

        :param param_map: Parameter map containing information that should be used to create the graph. The player's
        name (player) is required. Optional parameters are the name of the player to compare to (compare), the
        stat to graph (stat), the player's league (league), and tactalyse's start and end dates (start_date, end_date).
        If compare is omitted, the graph will be a single-player graph. If stat is omitted, a random stat is selected.
        The rest is fully optional.
        :return: Parameter map with the player's name (player), a DataFrame with the player's data (player_data), the
        compare player's name (compare) and data (compare_data), the passed league if any (league), the player's
        position as the abbreviation from the player file (main_pos), in full (player_pos), and abbreviated
        (main_pos_short), tactalyse start and end dates (start_date, end_date), the stat to graph (stat), and columns
        to use for graphing (columns).
        """
        line_map = {'type': "line"}

        line_map = self.set_player(param_map, line_map)
        line_map = self.set_compare(param_map, line_map)
        line_map = self.set_league(param_map, line_map)
        line_map = self.set_player_data(line_map)
        line_map = self.set_tactalyse_data(param_map, line_map)
        line_map = self.set_stats(param_map, line_map)

        return line_map

    def set_player(self, param_map, line_map):
        """
        Function that sets the player's name in the line graph parameter map. If it was not passed, it is randomized.

        :param param_map: Parameter map containing data passed to the API endpoint.
        :param line_map: Parameter map to be used by the line graph module.
        :return: Line graph parameter map updated with a player name (player).
        """
        player = param_map.get('player')
        if not player:
            player = self.__randomizer.random_player_line()
        line_map.update({'player': player})
        return line_map

    def set_compare(self, param_map, line_map):
        """
        Function that sets the compare player's name in the line graph parameter map, along with their match data.
        If no name was included in the input parameter map, it is entirely omitted.

        :param param_map: Parameter map containing data passed to the API endpoint.
        :param line_map: Parameter map to be used by the line graph module.
        :return: Line graph parameter map updated with a compare player name (compare), and their match data in a
        DataFrame (compare_data).
        """
        if not param_map.get('compare'):
            return line_map

        compare = param_map.get('compare')
        line_map.update({'compare': compare})

        compare_df = self.__reader.player_data(compare)
        line_map.update({'compare_data': compare_df})
        return line_map

    def set_league(self, param_map, line_map):
        """
        Function that sets the player's league in the line graph parameter map. If no league name was included in the
        input parameter map, it is set to "League".

        :param param_map: Parameter map containing data passed to the API endpoint.
        :param line_map: Parameter map to be used by the line graph module.
        :return: Line graph parameter map updated with the league's name (league).
        """
        league = param_map.get('league')
        if league:
            league = league.upper()
        else:
            league = "League"
        line_map.update({'league': league})
        return line_map

    def set_player_data(self, line_map):
        """
        Function that sets the player's match data in the line graph parameter map, along with their position in
        different formats.

        :param param_map: Parameter map containing data passed to the API endpoint.
        :param line_map: Parameter map to be used by the line graph module.
        :return: Line graph parameter map updated with a player match DataFrame (player_data), the player's position
        as stated in the match data file (main_pos), the corresponding general position name (player_pos), and the
        abbreviation of the general position (main_pos_short).
        """
        player = line_map.get('player')
        player_df = self.__reader.player_data(player)
        line_map.update({'player_data': player_df})

        main_pos = self.main_position_player_file(player_df)
        line_map.update({'main_pos': main_pos})

        player_pos = self.position_dictionary().get(main_pos)
        line_map.update({'player_pos': player_pos})

        main_pos_short = self.shortened_dictionary().get(main_pos)
        line_map.update({'main_pos_short': main_pos_short})
        return line_map

    def set_tactalyse_data(self, param_map, line_map):
        """
        Function that sets the start and end dates for tactalyse's services for the passed player.
        If no dates were included in the input parameter map, they're set to None.

        :param param_map: Parameter map containing data passed to the API endpoint.
        :param line_map: Parameter map to be used by the line graph module.
        :return: Line graph parameter map updated with a start date for tactalyse's services (start_date), and an end
        date (end_date).
        """
        start_date = param_map.get('start_date')
        line_map.update({'start_date': start_date})

        end_date = param_map.get('end_date')
        line_map.update({'end_date': end_date})
        return line_map

    def set_stats(self, param_map, line_map):
        """
        Function that sets the stat to be graphed in the line graph parameter map.
        If no stat was included in the input parameter map, it is randomized.

        :param param_map: Parameter map containing data passed to the API endpoint.
        :param line_map: Parameter map to be used by the line graph module.
        :return: Line graph parameter map updated with a stat to be graphed (stat).
        """
        stat = param_map.get('stat')
        if not stat:
            stat = self.__randomizer.random_player_stat()
        columns = [stat]
        line_map.update({'columns': columns})
        return line_map

    @property
    def randomizer(self):
        return self.__randomizer

    @property
    def reader(self):
        return self._reader
