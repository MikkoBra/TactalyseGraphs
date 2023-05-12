import os
import shutil


class FileUpdater:
    def update(self, files, folder):
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)

        for file in files:
            shutil.copy(file, folder)

    def update_league_files(self, new_files):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Get the absolute path of the parent directory (source folder)
        source_folder = os.path.abspath(os.path.join(current_dir, '..', '..'))
        files_folder = os.path.join(source_folder, 'graph_app', 'files', 'leagues')
        self.update(new_files, files_folder)

    def update_player_files(self, new_files):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Get the absolute path of the parent directory (source folder)
        source_folder = os.path.abspath(os.path.join(current_dir, '..', '..'))
        files_folder = os.path.join(source_folder, 'graph_app', 'files', 'players')
        self.update(new_files, files_folder)
