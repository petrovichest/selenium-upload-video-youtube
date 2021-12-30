import json
import os
import random
import shutil
import time
import traceback


class FileController:

    def __init__(self, **kwargs):
        try:
            self.profile_name = kwargs.get('profile_name').split(';')[0].split("\\")[-1]
            self.profile_path = kwargs.get('profile_name').split(';')[0].replace(self.profile_name, '')
            pass
        except:
            pass



    def startup_check(self):
        try:
            os.mkdir('./Profiles')
        except:
            pass
        accs = os.listdir('./Profiles')
        config = self.read_json()
        for acc in accs:
            if acc not in config['accounts_options']:
                config['accounts_options'][acc] = {"planet": 'None'}

        self.write_json(config)



    def read_json(self):
        with open('./res/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config

    def write_json(self, data):
        with open('./res/config.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    def read_random_proxy(self):
        try:
            with open('./res/proxy.txt', 'r', encoding='utf-8') as f:
                proxy_list = [x.strip() for x in f.read().split('\n') if x]
        except:
            with open('./res/proxy.txt', 'w', encoding='utf-8') as f:
                proxy_list = []

        if not proxy_list:
            return []
        proxy = random.choice(proxy_list)
        return proxy

    def create_profile_folder(self):
        self.delete_profile_folder()

        try:
            bot_folder = f'bot {self.profile_name.split(" ")[1]}'
        except:
            return False

        try:
            os.mkdir(f'{self.profile_path}/{bot_folder}')
        except:
            pass

        try:
            shutil.copytree(f'{self.profile_path}/{self.profile_name}', f'{self.profile_path}/{bot_folder}/{self.profile_name}')
        except:
            self.delete_profile_folder()
            return False

        try:
            shutil.copy(f'{self.profile_path}/Local State', f'{self.profile_path}/{bot_folder}')
        except:
            self.delete_profile_folder()
            return False

        return f'{self.profile_path}/{bot_folder}/{self.profile_name}'


    def delete_profile_folder(self):
        bot_folder = f'bot {self.profile_name.split(" ")[1]}'

        try:
            shutil.rmtree(f'{self.profile_path}/{bot_folder}')
        except:
            # traceback.print_exc()
            pass

    def get_log_pass_authed(self):
        try:
            with open('res/profiles_paths_non-relocatable.txt', 'r', encoding='utf-8') as f:
                profiles = [x.strip() for x in f.read().split('\n') if x]
        except:
            with open('res/profiles_paths_non-relocatable.txt', 'w', encoding='utf-8') as f:
                profiles = []

        return profiles

    def get_log_pass_unauthed(self):
        try:
            with open('res/profiles_paths_non-relocatable_to_auth.txt', 'r', encoding='utf-8') as f:
                profiles = [x.strip() for x in f.read().split('\n') if x]
        except:
            with open('res/profiles_paths_non-relocatable_to_auth.txt', 'w', encoding='utf-8') as f:
                profiles = []

        return profiles

    def write_log_pass_authed_accs(self, log_pass):
        with open('res/profiles_paths_non-relocatable.txt', 'a', encoding='utf-8') as f:
            f.write(f'{log_pass}\n')

    def write_log_pass_non_authed_accs(self, log_pass):
        with open('res/profiles_paths_non-relocatable_to_auth.txt', 'a', encoding='utf-8') as f:
            f.write(f'{log_pass}\n')


    def delete_log_pass_authed_accs(self, log_pass):
        with open('res/profiles_paths_non-relocatable_to_auth.txt', 'r', encoding='utf-8') as f:
            profiles = [x.strip() for x in f.read().split('\n') if x]
        try:
            profiles.remove(log_pass)
        except:
            pass

        with open('res/profiles_paths_non-relocatable_to_auth.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(profiles))

    def delete_log_pass_non_authed_accs(self, log_pass):
        with open('res/profiles_paths_non-relocatable.txt', 'r', encoding='utf-8') as f:
            profiles = [x.strip() for x in f.read().split('\n') if x]
        try:
            profiles.remove(log_pass)
        except:
            pass

        with open('res/profiles_paths_non-relocatable.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(profiles))


    def read_telegram_token(self):
        try:
            with open('res/telegram_token.txt', 'r', encoding='utf-8') as f:
                telegram_token = f.read().split('\n')[0]
        except:
            with open('res/telegram_token.txt', 'w', encoding='utf-8') as f:
                telegram_token = ''
        return telegram_token

    def read_telegram_chat_ids(self):
        try:
            with open('res/chat_ids.txt', 'r', encoding='utf-8') as f:
                chat_ids = [x.strip() for x in f.read().split('\n') if x]
        except:
            with open('res/chat_ids.txt', 'w', encoding='utf-8') as f:
                chat_ids = []
        return chat_ids


if __name__ == '__main__':
    FileController(profile_name=r'C:\Users\kate\AppData\Local\Google\Chrome\User Data\Profile 10')
    FileController().delete_profile_folder(r'C:\Users\kate\AppData\Local\Google\Chrome\User Data', 'Profile 10')

    print('Start')
    start_time = int(time.time())
    FileController().create_profile_folder(r'C:\Users\kate\AppData\Local\Google\Chrome\User Data', 'Profile 10')
    end_time = int(time.time())
    print('End')
    print(end_time - start_time)
