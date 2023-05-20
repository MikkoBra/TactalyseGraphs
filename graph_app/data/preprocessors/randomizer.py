import os
import random

from ..text_cleaner import TextCleaner


class Randomizer:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.__source_folder = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
        self.__cleaner = TextCleaner()

    def random_player(self):
        files_folder = os.path.join(self.__source_folder, 'graph_app', 'files', 'players')
        player_files = os.listdir(files_folder)

        random_player_file = random.choice(player_files)

        # Extract the file name
        file_name = os.path.splitext(random_player_file)[0]
        player_name = self.__cleaner.clean_player_name(file_name)

        # Return the player name as a string
        return player_name

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
