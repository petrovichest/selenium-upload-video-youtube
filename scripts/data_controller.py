import json


class DataController:

    def read_accs_json(self):
        with open('./res/accs_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def write_accs_json(self, data):
        with open(f'./res/accs_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_accs_paths(self):
        data = self.read_accs_json()
        accs_paths = [data.get(x).get('profile_path') for x in data if data.get(x).get('status')]
        return accs_paths

    def write_acc_data(self, acc_data):
        acc_file_data = self.read_accs_json()
        acc_name = acc_data.get('acc_name')
        acc_file_data[acc_name] = acc_data
        self.write_accs_json(acc_file_data)