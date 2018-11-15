import requests


class HTTP:
    @staticmethod
    def get(url, return_json=True):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json() if return_json else response.text
        else:
            return {} if return_json else ''