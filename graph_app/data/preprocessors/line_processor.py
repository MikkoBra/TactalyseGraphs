from .preprocessor import Preprocessor
from .randomizer import Randomizer
from ..excel_reader import ExcelReader


class LineProcessor(Preprocessor):
    def __init__(self):
        self.__randomizer = Randomizer()
        self.__reader = ExcelReader()

    def get_columns_line_plots(self, player_pos):
        """
        Function that provides a list of headers to use for graphing the line plots.

        :param player_pos: Abbreviated position of the player whose stats to graph.
        :return: DataFrame containing the required stats to graph.
        """
        stats_file = "graph_app/files/Stats per position.xlsx"
        stats_pd = ExcelReader().read_file(stats_file)
        stats_necessary = stats_pd[['Attribute', player_pos]]
        stats_necessary = stats_necessary[stats_necessary[player_pos] == 1.0]
        return stats_necessary['Attribute']

    def extract_line_data(self, param_map):
        """
        Function that extracts all required data from the passed player match data Excel file.

        :param param_map:
        :return: DataFrame containing the player's match data (player_df), columns to use for graphing (columns).
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
        player = param_map.get('player')
        if not player:
            player = self.__randomizer.random_player()
        line_map.update({'player': player})
        return line_map

    def set_compare(self, param_map, line_map):
        if not param_map.get('compare'):
            return line_map

        compare = param_map.get('compare')
        line_map.update({'compare': compare})

        compare_df = self.__reader.player_data(compare)
        line_map.update({'compare_data': compare_df})
        return line_map

    def set_league(self, param_map, line_map):
        league = param_map['league'].upper()
        line_map.update({'league': league})
        return line_map

    def set_player_data(self, line_map):
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
        start_date = param_map.get('start-date')
        line_map.update({'start_date': start_date})

        end_date = param_map.get('end-date')
        line_map.update({'end_date': end_date})
        return line_map

    def set_stats(self, param_map, line_map):
        stat = param_map.get('stat')
        if not stat:
            stat = self.__randomizer.random_player_stat()
        columns = [stat]
        line_map.update({'columns': columns})
        return line_map
