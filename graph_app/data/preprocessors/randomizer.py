import os
import random

from .preprocessor import Preprocessor
from ..text_cleaner import TextCleaner


class Randomizer(Preprocessor):
    """
    Class that handles the generation of random values for any unfilled API request parameters for the random graph
    endpoint. It uses the local files in the files folder in graph_app for setting random player data.
    """

    def __init__(self, *args, **kwargs):
        super(Randomizer, self).__init__(*args, **kwargs)
        self.__cleaner = TextCleaner()

    def set_random_parameters(self, param_map):
        """
        Function that sets random values for each missing parameter in the parameter map.

        :param param_map: Parameter map containing data passed to the API endpoint.
        :return: Parameter map with a DataFrame containing league data (league_df), a random player's name (player), a
        random compare player's name (compare) if a radar graph is requested, a random stat from the player match files
        (stat) if a line graph is requested, and the player's league (league) set to a default value if not included.
        """

        if param_map.get('league') is None:
            param_map['league'] = self.random_league()

        if param_map.get('graph_type') == "radar":
            param_map = self.extract_league_data(param_map)

        if param_map.get('player') is None:
            param_map = self.random_player(param_map)

        if param_map.get('graph_type') == "radar" and param_map.get('compare') is None:
            param_map = self.random_compare(param_map)

        if param_map['graph_type'] == "line" and param_map.get('stat') is None:
            param_map['stat'] = self.random_player_stat()

        return param_map


    def random_player(self, param_map):
        """
        Function that chooses a random name from the local player files for line graphs, or a random name from the
        league dataframe for radar graphs.

        :param param_map: Parameter map containing data passed to the API endpoint and, for radar graphs, the league
        dataframe (league_df).
        :return: Parameter map updated with a random player name (player).
        """
        if param_map['graph_type'] == "line":
            param_map['player'] = self.random_player_line()

        else:
            league_df = param_map['league_df']
            random_value = self.random_player_radar(league_df)
            param_map['player'] = random_value

        return param_map

    def random_compare(self, param_map):
        """
        Function that finds the position of the main player, and selects a random player from the league dataframe with
        the same position.

        :param param_map: Parameter map containing data passed to the API endpoint, the league dataframe (league_df),
        and the main player's name (player).
        :return: Parameter map updated with a random compare player name (compare).
        """
        league_df = param_map['league_df']
        player = param_map['player']
        player_row = self._reader.league_data(param_map['player'], league_df)
        player_pos = self.main_position_league_file(player_row)
        param_map['compare'] = self.select_random_compare(league_df, player_pos, player)
        return param_map

    def random_player_line(self):
        """
        Function that selects a random name from the local player files for line graphs.

        :return: A player name extracted from the titles of the local player files.
        """
        files_folder = "graph_app/files/players"
        player_files = os.listdir(files_folder)

        random_player_file = random.choice(player_files)

        file_name = os.path.splitext(random_player_file)[0]
        player_name = self.__cleaner.clean_player_name(file_name)

        return player_name

    def random_player_radar(self, league_df):
        """
        Function that selects a random player name from the league dataframe.

        :param league_df: DataFrame containing league data.
        :return: The name of the player to use for the radar graph.
        """
        random_value = league_df['Player'].sample(n=1).values[0]
        return random_value

    def select_random_compare(self, league_df, player_pos, player=None):
        """
        Function that selects a random player name to compare to from the league dataframe that matches the
        passed player position. If passed, the name of the main player is avoided.

        :param league_df: DataFrame containing league data.
        :param player_pos: The position the returned player should have.
        :param player: The name of the main player. Will be avoided in selecting the compare name.
        :return: The name of the player to compare to.
        """
        position_df = league_df[league_df['Position'].str.contains(player_pos)]
        random_player = player
        while random_player == player:
            random_player = position_df['Player'].sample(n=1).values[0]
        return random_player

    def random_player_stat(self):
        """
        Function that randomly selects a stat used in the player match files. Currently based on a hardcoded list.

        :return: Randomly selected player file column header as a string.
        """

        stats = ["Minutes played", "Total actions / successful", "Goals", "Assists", "Shots / on target", "xG",
                 "Passes / accurate", "Long passes / accurate", "Crosses / accurate", "Dribbles / successful",
                 "Duels / won", "Aerial duels / won", "Interceptions", "Losses / own half", "Recoveries / opp. half",
                 "Yellow card", "Red card", "Defensive duels / won", "Loose ball duels / won",
                 "Sliding tackles / successful", "Clearances", "Fouls", "Yellow cards", "Red cards", "Shot assists",
                 "Offensive duels / won", "Touches in penalty area", "Offsides", "Progressive runs", "Fouls suffered",
                 "Through passes / accurate", "xA", "Second assists", "Passes to final third / accurate",
                 "Passes to penalty area / accurate", "Received passes", "Forward passes / accurate",
                 "Back passes / accurate", "Conceded goals", "xCG", "Shots against", "Saves / with reflexes", "Exits",
                 "Passes to GK / accurate", "Goal kicks", "Short goal kicks", "Long goal kicks"]
        return random.choice(stats)

    @property
    def reader(self):
        """
        Getter for the reader attribute of the Randomizer.

        :return: ExcelReader object representing the Randomizer's Excel file and DataFrame reader.
        """
        return self._reader

    @property
    def cleaner(self):
        """
        Getter for the cleaner attribute of the Randomizer.

        :return: TextCleaner object representing the Randomizer's text cleaner.
        """
        return self.__cleaner
