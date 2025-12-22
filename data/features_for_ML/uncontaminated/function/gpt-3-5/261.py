def check_and_notify():
    import requests
    import json

    def get_latest_version():
        response = requests.get('https://api.example.com/version')
        data = response.json()
        return data['version']

    def get_current_version():
        with open('version.txt', 'r') as file:
            return file.read()

    def notify_user(version):
        print(f'New version {version} is available! Please update.')

    latest_version = get_latest_version()
    current_version = get_current_version()

    if latest_version != current_version:
        notify_user(latest_version)