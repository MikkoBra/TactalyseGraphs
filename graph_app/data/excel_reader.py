import os

import pandas as pd


class ExcelReader:
    """
    Class that contains functionality related to reading data from Excel files.
    """

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.__source_folder = os.path.abspath(os.path.join(current_dir, '..', '..'))

    def read_file(self, file):
        """
        General function for reading data from an Excel (.xlsx) file into a Pandas dataframe.

        :param file: The Excel file containing desired data.
        :return: A Pandas dataframe containing all data in the Excel file, including headers.
        """
        return pd.read_excel(file)

    def player_data(self, player):
        """
        Function for extracting the match data of a football player from an Excel file.

        :param player: The name of the player whose match data to extract.
        :return: A Pandas dataframe containing all data in the Excel file, including headers.
        """
        files_folder = os.path.join(self.__source_folder, 'graph_app', 'files', 'players')

        for dirpath, dirnames, filenames in os.walk(files_folder):
            for filename in filenames:
                if filename.startswith("Player stats") and filename.endswith(".xlsx") and player in filename:
                    file_path = os.path.join(dirpath, filename)
                    print("File found:", file_path)
                    return self.read_file(file_path)
        print("Player file not found.")
        return pd.DataFrame()

    def league_data(self, player, league_df):
        """
        Function for extracting the football league data of a single player from an Excel file.

        :param player:
        :param league:
        :return: A Pandas dataframe containing all data in the Excel file, including headers.
        """
        if league_df is None:
            return pd.DataFrame()
        try:
            player = league_df.loc[league_df['Player'] == player]
        except KeyError:
            raise KeyError("Player did not exist in the league file.")
        return player

    def all_league_data(self):
        """
        Function for extracting all data from a league file into a dataframe.

        :return: Dataframe containing data for all players in a specified football league file.
        """
        files_folder = os.path.join(self.__source_folder, 'graph_app', 'files', 'leagues')
        for dirpath, dirnames, filenames in os.walk(files_folder):
            for filename in filenames:
                if "league" in filename:
                    file_path = os.path.join(dirpath, filename)
                    print("File found:", file_path)
                    return self.read_file(file_path)
        print("League file not found.")
        return pd.DataFrame()
