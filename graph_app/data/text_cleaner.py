import re


class TextCleaner:
    def clean_player_name(self, text):
        text = self.remove_after_non_alphanumeric(text)
        text = self.remove_extra_whitespace(text)
        text = self.remove_player_stats(text)
        return text

    def remove_after_non_alphanumeric(self, text):
        pattern = r'[^0-9a-zA-Z.\s]'
        parts = re.split(pattern, text)
        return parts[0]

    def remove_extra_whitespace(self, text):
        return re.sub(r'\s+', ' ', text)

    def remove_player_stats(self, text):
        return text.replace("Player stats ", "")
