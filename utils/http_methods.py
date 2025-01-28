import requests


# Список HTTP методов
class HttpMethods:
    headers = {'Content_Type': 'application/json'}
    cookie = ''

    @staticmethod
    def get(url, headers=None):
        result = requests.get(url, headers=headers, cookies=HttpMethods.cookie)
        return result

    @staticmethod
    def post(url, body=None, headers=None):
        result = requests.post(url, json=body, headers=headers, cookies=HttpMethods.cookie)
        return result

    @staticmethod
    def put(url, body=None, headers=None):
        result = requests.put(url, json=body, headers=headers, cookies=HttpMethods.cookie)
        return result

    @staticmethod
    def delete(url, body=None):
        result = requests.delete(url, json=body, headers=HttpMethods.headers, cookies=HttpMethods.cookie)
        return result
