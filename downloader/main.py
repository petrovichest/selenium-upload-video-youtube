from scripts.data_controller import DataController
from downloader.tiktok_download import TikTokDownload

class TikTokController:

    def run(self):
        accs_data = DataController().read_accs_json()
        for one_acc in accs_data:
            category = one_acc.get('category')
            TikTokDownload().download_by_hashtag(category, videos_count=10)
