from ..excel_reader import ExcelReader


class Preprocessor:

    def position_dictionary(self):
        """
        Creates a collection of all position codes, with their associated general position in full words.
        Work in progress.

        :return: Dictionary containing all position abbreviations as keys, and the associated general positions as values.
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
        Creates a collection of all position codes, with their associated general position as abbreviations.
        Work in progress.

        :return: Dictionary containing all position abbreviations as keys, and the associated general position abbreviations
                 as values.
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
        Creates a collection of all positions, along with the league stats that should be graphed in the radio chart for
        each position.
        Work in progress.

        :return: Dictionary containing all positions as keys, and the associated stats as values.
        """

        cat_dict = dict.fromkeys(['GK'], ['Shots blocked per 90', 'Long passes per 90',
                                          'Accurate long passes, %', 'Key passes per 90',
                                          'Smart passes per 90', 'Accurate smart passes, %',
                                          'Aerial duels won, %'])
        cat_dict.update(dict.fromkeys(['FB'], ['Sliding tackles per 90', 'Interceptions per 90',
                                               'Crosses per 90', 'Accurate crosses, %',
                                               'Defensive duels per 90', 'Defensive duels won, %',
                                               'Pass accuracy (%)', 'Key passes per 90']))
        cat_dict.update(dict.fromkeys(['CB'], ['Shots blocked per 90', 'Interceptions per 90',
                                               'Pass accuracy (%)', 'Aerial duels won, %',
                                               'Defensive duels per 90', 'Defensive duels won, %',
                                               'Crosses per 90', 'Dribbles per 90']))
        cat_dict.update(dict.fromkeys(['DM'], ['Sliding tackles per 90', 'Interceptions per 90',
                                               'Crosses per 90', 'Accurate crosses, %',
                                               'Defensive duels per 90', 'Defensive duels won, %',
                                               'Pass accuracy (%)', 'Key passes per 90']))
        cat_dict.update(dict.fromkeys(['AM'], ['Progressive runs per 90', 'Assists per 90',
                                               'Offensive duels won, %', 'Key passes per 90',
                                               'Pass accuracy (%)', 'Goals per 90',
                                               'Shots per 90', 'Shots on target, %']))
        cat_dict.update(dict.fromkeys(['WI'], ['Crosses per 90', 'Assists per 90',
                                               'Offensive duels won, %', 'Key passes per 90',
                                               'Pass accuracy (%)', 'Goals per 90',
                                               'Shots per 90', 'Shots on target, %']))
        cat_dict.update(dict.fromkeys(['ST'], ['Successful dribbles, %', 'Assists per 90',
                                               'Key passes per 90', 'xG/Shot',
                                               'Pass accuracy (%)', 'Goals per 90',
                                               'Shots per 90', 'Shots on target, %']))
        return cat_dict

    def main_position(self, player_row):
        """
        Function that retrieves the main position of a football player.

        :param player_row: Dataframe containing the league data of a single player.
        :return: The first position in the list of player positions.
        """
        player_positions = player_row['Position'].iloc[0]
        first_position = player_positions.split(', ')[0]
        return first_position

    def in_league(self, league_file, player_name):
        """
        Function that checks if the player is included in the league file

        :param league_file:
        :param player_name:
        :return: True if they're in the league file, false if not
        """

        league_df = ExcelReader().all_league_data(league_file)
        if player_name in league_df['Player'].values:
            return True
        else:
            return False
