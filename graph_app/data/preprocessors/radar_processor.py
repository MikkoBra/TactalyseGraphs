from .preprocessor import Preprocessor
from .randomizer import Randomizer


class RadarProcessor(Preprocessor):
    """
    Class that handles data extraction and processing specific to radar charts. It allows for extracting the required
    stats to be graphed from an excel file, and for generating a map containing the parameters needed by the radar chart
    module.
    """

    def __init__(self, *args, **kwargs):
        super(RadarProcessor, self).__init__(*args, **kwargs)
        self.__randomizer = Randomizer()

    def get_columns_radar_chart(self, position):
        """
        Function that provides a list of headers to use for graphing the radar chart.

        :param position: Full position name of the player whose stats to graph.
        :return: List of column headers in string form to extract from dataframes when creating PDF graphs.
        """
        return self.league_category_dictionary().get(position)

    def extract_radar_data(self, param_map):
        """
        Function that takes information of the player from the passed parameter map, and generates a map containing
        data processed for use by the graph module.

        :param param_map: Parameter map containing information that should be used to create the graph. The player's
        name (player) is required. Optional parameters are the name of the player to compare to (compare), and the
        player's league (league).
        If compare is omitted, the graph will be a single-player graph. The league parameter is fully optional.
        :return: Parameter map with the player's name (player), a DataFrame with the player's data (player_data), the
        compare player's name (compare) and data (compare_data), a DataFrame extracted from the player's league file
        (league_data), the player's position as found in the league file but in full (main_pos_long), and the interpreted
        long position name abbreviated (main_pos), the row of the league file that belongs to the mentioned player
        (player_row), the same for the compare player (compare_row), columns to use for graphing (columns), and the max
        value within the league for each of these columns in a list (scales).
        """
        radar_map = {'type': "radar"}
        if param_map.get('league_df') is None:
            param_map = self.extract_league_data(param_map)
        league_df = param_map.get('league_df')

        radar_map = self.set_player(param_map, league_df, radar_map)
        radar_map = self.set_player_data(league_df, radar_map)
        radar_map = self.set_player_positions(radar_map)
        radar_map = self.set_compare(param_map, league_df, radar_map)
        radar_map = self.set_stats(radar_map)
        radar_map = self.set_max_vals(league_df, radar_map)

        return radar_map

    def set_player(self, param_map, league_df, radar_map):
        """
        Function that sets the player's name in the radar graph parameter map. If it was not passed, it is randomized.

        :param league_df: DataFrame containing league data.
        :param param_map: Parameter map containing data passed to the API endpoint.
        :param radar_map: Parameter map to be used by the radar graph module.
        :return: Line graph parameter map updated with a player name (player).
        """
        player = param_map.get('player')
        if not player:
            player = self.__randomizer.random_player_radar(league_df)
        radar_map.update({'player': player})
        return radar_map

    def set_player_data(self, league_df, radar_map):
        """
        Function that sets the player's league data in the radar graph parameter map.

        :param league_df: DataFrame containing data for all players in the passed player's league.
        :param radar_map: Parameter map to be used by the radar graph module.
        :return: Radar graph parameter map updated with a player's row from the league DataFrame (player_data), the
        player's position as stated in the league data file (main_pos), the corresponding general position name
        (player_pos), and the abbreviation of the general position (player_pos_short).
        """
        player = radar_map.get('player')
        player_row = self._reader.league_data(player, league_df)
        radar_map.update({'player_row': player_row})
        return radar_map

    def set_player_positions(self, radar_map):
        """
        Function that sets the player's position in the radar graph parameter map in different formats

        :param radar_map: Parameter map to be used by the radar graph module.
        :return: Radar graph parameter map updated with the player's position as stated in the league data file
        (main_pos), the corresponding general position name (player_pos), and the abbreviation of the general position
        (player_pos_short).
        """
        player_row = radar_map.get('player_row')
        main_pos = self.main_position_league_file(player_row)
        radar_map.update({'main_pos': main_pos})
        main_pos_long = self.position_dictionary().get(main_pos)
        radar_map.update({'player_pos': main_pos_long})

        main_pos_short = self.shortened_dictionary().get(main_pos)
        radar_map.update({'player_pos_short': main_pos_short})
        return radar_map

    def set_compare(self, param_map, league_df, radar_map):
        """
        Function that sets the compare player's name in the radar graph parameter map, along with their league data.
        If no name was included in the input parameter map, it is entirely omitted.

        :param param_map: Parameter map containing data passed to the API endpoint.
        :param league_df: DataFrame containing data for all players in the passed player's league.
        :param radar_map: Parameter map to be used by the radar graph module.
        :return: Radar graph parameter map updated with a compare player name (compare), and their row from the league
        DataFrame (compare_row).
        """
        if not param_map.get('compare'):
            return radar_map

        compare = param_map.get('compare')
        radar_map.update({'compare': compare})

        compare_df = self._reader.league_data(compare, league_df)
        radar_map.update({'compare_row': compare_df})
        return radar_map

    def set_stats(self, radar_map):
        """
        Function that sets the stats to be graphed in the radar graph parameter map. They are retrieved from the
        column dictionary from the Preprocessor class based on the player's position

        :param radar_map: Parameter map to be used by the radar graph module.
        :return: Radar graph parameter map updated with a list containing stats to be graphed (columns).
        """
        main_pos = radar_map['player_pos_short']
        columns = self.get_columns_radar_chart(main_pos)
        radar_map.update({'columns': columns})
        return radar_map

    def set_max_vals(self, league_df, radar_map):
        """
        Function that retrieves the maximum value in the league for each stat to be graphed in the radar chart, and
        updates the radar graph parameter map to include a list containing them.

        :param league_df: DataFrame containing data for all players in the passed player's league.
        :param radar_map: Parameter map to be used by the radar graph module.
        :return: Radar graph parameter map updated with a list containing the maximum value for each stat to be graphed
        (scales)
        """
        columns = radar_map.get('columns')
        max_vals_df = league_df[columns].max(axis=0)
        max_vals = max_vals_df.tolist()
        radar_map.update({'scales': max_vals})
        return radar_map

    @property
    def randomizer(self):
        """
        Getter for the randomizer attribute of the RadarProcessor.

        :return: Randomizer object representing the RadarProcessor's random value generator.
        """
        return self.__randomizer

    @property
    def reader(self):
        """
        Getter for the reader attribute of the RadarProcessor.

        :return: ExcelReader object representing the RadarProcessor's Excel file and DataFrame reader.
        """
        return self._reader
