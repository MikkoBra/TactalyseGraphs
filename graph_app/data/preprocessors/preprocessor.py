from collections import Counter

from graph_app.data.excel_reader import ExcelReader


class Preprocessor:

    def __init__(self, *args, **kwargs):
        self._reader = ExcelReader()

    def position_dictionary(self):
        """
        Creates a collection of all position codes as found in the league file, with their associated general position
        in full words.

        :return: Dictionary containing all position abbreviations as keys, and the associated general positions as
        values.
        """

        pos_dict = dict.fromkeys(['RW', 'RWF', 'LWF', 'LW'], 'Winger')
        pos_dict.update(dict.fromkeys(['GK'], 'Goalkeeper'))
        pos_dict.update(dict.fromkeys(['LB', 'LB5', 'LWB', 'RB', 'RB5', 'RWB'], 'Full Back'))
        pos_dict.update(dict.fromkeys(['RCB', 'RCB3', 'CB', 'LCB', 'LCB3'], 'Center Back'))
        pos_dict.update(
            dict.fromkeys(['DMF', 'LCMF', 'RCMF', 'LDMF', 'RDMF', 'LCMF3', 'RCMF3'], 'Defensive Midfielder'))
        pos_dict.update(dict.fromkeys(['AMF', 'LAMF', 'RAMF'], 'Attacking Midfielder'))
        pos_dict.update(dict.fromkeys(['CF', 'LCF', 'RCF'], 'Striker'))

        return pos_dict

    def shortened_dictionary(self):
        """
        Creates a collection of all position codes as found in the league file, with their associated general position
        as abbreviations.

        :return: Dictionary containing all position abbreviations as keys, and the associated general position
        abbreviations as values.
        """
        pos_dict = dict.fromkeys(['RW', 'RWF', 'LWF', 'LW'], 'WI')
        pos_dict.update(dict.fromkeys(['GK'], 'GK'))
        pos_dict.update(dict.fromkeys(['LB', 'LB5', 'LWB', 'RB', 'RB5', 'RWB'], 'FB'))
        pos_dict.update(dict.fromkeys(['RCB', 'RCB3', 'CB', 'LCB', 'LCB3'], 'CB'))
        pos_dict.update(dict.fromkeys(['DMF', 'LCMF', 'RCMF', 'LDMF', 'RDMF', 'LCMF3', 'RCMF3'], 'DM'))
        pos_dict.update(dict.fromkeys(['AMF', 'LAMF', 'RAMF'], 'AM'))
        pos_dict.update(dict.fromkeys(['CF', 'LCF', 'RCF'], 'ST'))

        return pos_dict

    def league_category_dictionary(self):
        """
        Creates a collection of all positions, along with the league stats that should be graphed in the radar chart for
        each position.

        :return: Dictionary containing all shortened positions as keys, and a list containing the associated stats as
        values.
        """

        cat_dict = dict.fromkeys(['GK'], ['Shots blocked per 90', 'Long passes per 90',
                                          'Accurate long passes, %', 'Key passes per 90',
                                          'Smart passes per 90', 'Accurate smart passes, %',
                                          'Aerial duels won, %', 'Clean sheets'])
        cat_dict.update(dict.fromkeys(['FB'], ['Sliding tackles per 90', 'Interceptions per 90',
                                               'Crosses per 90', 'Accurate crosses, %',
                                               'Defensive duels per 90', 'Defensive duels won, %',
                                               'Accurate passes, %', 'Key passes per 90']))
        cat_dict.update(dict.fromkeys(['CB'], ['Shots blocked per 90', 'Interceptions per 90',
                                               'Accurate passes, %', 'Aerial duels won, %',
                                               'Defensive duels per 90', 'Defensive duels won, %',
                                               'Crosses per 90', 'Dribbles per 90']))
        cat_dict.update(dict.fromkeys(['DM'], ['Sliding tackles per 90', 'Interceptions per 90',
                                               'Crosses per 90', 'Accurate crosses, %',
                                               'Defensive duels per 90', 'Defensive duels won, %',
                                               'Accurate passes, %', 'Key passes per 90']))
        cat_dict.update(dict.fromkeys(['AM'], ['Progressive runs per 90', 'Assists per 90',
                                               'Offensive duels won, %', 'Key passes per 90',
                                               'Accurate passes, %', 'Goals per 90',
                                               'Shots per 90', 'Shots on target, %']))
        cat_dict.update(dict.fromkeys(['WI'], ['Crosses per 90', 'Assists per 90',
                                               'Offensive duels won, %', 'Key passes per 90',
                                               'Accurate passes, %', 'Goals per 90',
                                               'Shots per 90', 'Shots on target, %']))
        cat_dict.update(dict.fromkeys(['ST'], ['Successful dribbles, %', 'Assists per 90',
                                               'Key passes per 90', 'xG',
                                               'Accurate passes, %', 'Goals per 90',
                                               'Shots per 90', 'Shots on target, %']))
        return cat_dict

    def main_position_league_file(self, player_row):
        """
        Function that retrieves the main position of a football player from the league file row of the player.

        :param player_row: Dataframe containing the league data of a single player.
        :return: The first position in the list of player positions.
        """
        player_positions = player_row['Position'].iloc[0]
        first_position = player_positions.split(', ')[0]
        return first_position

    def extract_league_data(self, param_map):
        """
        Function that extracts all league data into a DataFrame, and puts it in the passed parameter map for further
        use.

        :param param_map: Parameter map containing data passed to the API endpoint.
        :return: Parameter map updated with a DataFrame containing all data in the league file (league_df).
        """
        league_df = self._reader.all_league_data(param_map['league'])
        league_df = league_df.fillna(0.0)
        param_map['league_df'] = league_df
        print("Extracted data into dataframe")
        return param_map

    def main_position_player_file(self, player_df):
        """
        Function that retrieves the main position of a football player from their match data file.

        :param player_df: Dataframe containing the match data of a single player.
        :return: The most frequently occurring position for the player in the match data file.
        """
        positions = []
        for entry in player_df['Position']:
            if not isinstance(entry, str):
                continue
            separated_positions = entry.split(', ')
            positions.extend(separated_positions)
        position_counter = Counter(positions)
        most_common = position_counter.most_common(1)[0][0]
        return most_common
