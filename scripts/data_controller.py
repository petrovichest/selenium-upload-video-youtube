import json


class DataController:

    def read_accs_json(self):
        with open('./res/accs.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def write_accs_json(self, data):
        with open(f'./res/accs.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_accs_paths(self):
        data = self.read_accs_json()
        accs_paths = [x.get('profile_path') for x in data if x]
        return accs_paths