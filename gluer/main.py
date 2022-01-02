from scripts.data_controller import DataController
from gluer.videos_processor import VideosProcessor

class GluerController:

    def run(self):
        accs_data = DataController().read_accs_json()
        for one_acc in accs_data:
            acc_status = accs_data.get(one_acc).get('status')
            if acc_status:
                category = accs_data.get(one_acc).get('category')
                VideosProcessor(category=category).compose_videos(length=900)


if __name__ == '__main__':
    GluerController().run()