import re


class TextCleaner:
    """
    Class used for preprocessing String text into a format usable by the graph generator.
    """

    def clean_player_name(self, text):
        """
        Function for separating all non-important information from a String containing a player name.

        :param text: String containing the player name, usually extracted from a player file name.
        :return: The name of the player.
        """
        text = self.remove_after_non_alphanumeric(text)
        text = self.remove_extra_whitespace(text)
        text = self.remove_player_stats(text)
        return text

    def remove_after_non_alphanumeric(self, text):
        """
        Function for removing all text from a string after a non-alphanumeric character.

        :param text: String to perform the clean action on.
        :return: The cleaned String.
        """
        pattern = r'[^0-9a-zA-Z.\s]'
        parts = re.split(pattern, text)
        return parts[0]

    def remove_extra_whitespace(self, text):
        """
        Function for changing all whitespace in a String to a single whitespace.

        :param text: String to perform the clean action on.
        :return: The cleaned String.
        """
        return re.sub(r'\s+', ' ', text)

    def remove_player_stats(self, text):
        """
        Function for removing "Player stats " from a passed String.

        :param text: String to perform the clean action on.
        :return: The cleaned String.
        """
        return text.replace("Player stats ", "")
