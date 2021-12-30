from scripts.file_controller import FileController
from scripts.data_controller import DataController
from loguru import logger


class ProfileMover:

    def run(self):
        logger.info('Start')
        profiles = DataController().get_accs_paths()

        logger.info(f'Profiles found: {len(profiles)}')

        for one_profile in profiles:
            profile_path = FileController(profile_name=one_profile).create_profile_folder()
            logger.info(f'Profile number: {profiles.index(one_profile) + 1}')

        logger.info('Complete')
        input()

if __name__ == '__main__':
    ProfileMover().run()