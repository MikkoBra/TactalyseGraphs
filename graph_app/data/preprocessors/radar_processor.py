from .preprocessor import Preprocessor
from .randomizer import Randomizer
from ..excel_reader import ExcelReader


class RadarProcessor(Preprocessor):
    def __init__(self):
        self.__randomizer = Randomizer()
        self.__reader = ExcelReader()

    def get_columns_radar_chart(self, position):
        """
        Function that provides a list of headers to use for graphing the radio chart.

        :param position: Full position name of the player whose stats to graph.
        :return: List of column headers in string form to extract from dataframes when creating PDF graphs.
        """
        return self.league_category_dictionary().get(position)

    def extract_radar_data(self, param_map):
        """
        Function that extracts all required data from the passed league data Excel file.

        :param param_map:
        :return: Dataframe containing a single row with the player's league data (player_row), columns to use for graphing
                 (columns), main position of the passed player (main_pos_long), and the position abbreviated (main_pos).
        """
        radar_map = {'type': "radar"}
        league_df = param_map.get('league_df')
        if league_df is None:
            league_df = self.__reader.all_league_data()
            league_df = league_df.fillna(0.0)
            param_map['league_df'] = league_df
            print("Extracted data into dataframe")

        radar_map = self.set_player(param_map, radar_map)
        radar_map = self.set_player_data(league_df, radar_map)
        radar_map = self.set_compare(param_map, league_df, radar_map)
        radar_map = self.set_stats(league_df, radar_map)

        return radar_map

    def set_player(self, param_map, radar_map):
        player = param_map.get('player')
        if not player:
            player = self.__randomizer.random_player()
        radar_map.update({'player': player})
        return radar_map

    def set_player_data(self, league_df, radar_map):
        player = radar_map.get('player')
        player_row = self.__reader.league_data(player, league_df)
        radar_map.update({'player_row': player_row})

        main_pos = self.main_position_league_file(player_row)
        main_pos_long = self.position_dictionary().get(main_pos)
        radar_map.update({'main_pos_long': main_pos_long})

        main_pos = self.shortened_dictionary().get(main_pos)
        radar_map.update({'main_pos': main_pos})
        return radar_map

    def set_compare(self, param_map, league_df, radar_map):
        if not param_map.get('compare'):
            return radar_map

        compare = param_map.get('compare')
        radar_map.update({'compare': compare})

        compare_df = self.__reader.league_data(compare, league_df)
        radar_map.update({'compare_row': compare_df})
        return radar_map

    def set_stats(self, league_df, radar_map):
        main_pos = radar_map['main_pos']
        columns = self.get_columns_radar_chart(main_pos)
        radar_map.update({'columns': columns})

        max_vals_df = league_df[columns].max(axis=0)
        max_vals = max_vals_df.tolist()
        radar_map.update({'scales': max_vals})

        return radar_map
