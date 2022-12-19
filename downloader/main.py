from scripts.data_controller import DataController
from downloader.tiktok_download import TikTokDownload

class TikTokController:

    def run(self):
        accs_data = DataController().read_accs_json()
        for one_acc in accs_data:
            acc_status = accs_data.get(one_acc).get('status')
            if not acc_status:
                continue

            category = accs_data.get(one_acc).get('category')
            TikTokDownload().download_by_hashtag(category, videos_count=300)
