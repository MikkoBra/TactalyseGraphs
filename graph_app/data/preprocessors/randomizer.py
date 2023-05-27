import os
import random

from ..text_cleaner import TextCleaner
from graph_app.data.excel_reader import ExcelReader
from .preprocessor import Preprocessor


class Randomizer(Preprocessor):
    def __init__(self):
        self.__cleaner = TextCleaner()
        self.__reader = ExcelReader()

    def set_random_parameters(self, param_map):
        if param_map.get('graph_type') == "radar":
            league_df = self.__reader.all_league_data()
            league_df = league_df.fillna(0.0)
            param_map['league_df'] = league_df
            print("Extracted data into dataframe")

        if param_map.get('player') is None:
            if param_map['graph_type'] == "line":
                param_map['player'] = self.random_player_line()
            else:
                league_df = param_map['league_df']
                random_value = league_df['Player'].sample(n=1).values[0]
                param_map['player'] = random_value

        if param_map.get('graph_type') == "radar" and param_map.get('compare') is None:
            league_df = param_map['league_df']
            player_pos = self.main_position_league_file(self.__reader.league_data(param_map['player'], league_df))
            param_map['compare'] = self.random_compare_radar(league_df, player_pos, param_map.get('player'))

        if param_map['graph_type'] == "line" and param_map.get('stat') is None:
            param_map['stat'] = self.random_player_stat()

        if param_map.get('league') is None:
            param_map['league'] = "rando2"

        return param_map

    def random_player_line(self):
        files_folder = "graph_app/files/players"
        player_files = os.listdir(files_folder)

        random_player_file = random.choice(player_files)

        # Extract the file name
        file_name = os.path.splitext(random_player_file)[0]
        player_name = self.__cleaner.clean_player_name(file_name)

        # Return the player name as a string
        return player_name

    def random_player_radar(self, league_df):
        random_value = league_df['Player'].sample(n=1).values[0]
        return random_value

    def random_compare_radar(self, league_df, player_pos, player):
        position_df = league_df[league_df['Position'].str.contains(player_pos)]
        random_player = player
        while random_player == player:
            random_player = position_df['Player'].sample(n=1).values[0]
        return random_player

    def random_player_stat(self):
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
