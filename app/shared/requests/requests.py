import requests


class RequestService:
    @staticmethod
    def get_requests(url, json_response=True, params=None) -> str:
        response = requests.get(url, params=params)
        if not json_response:
            return response.content

        return response.json()

    @staticmethod
    def post_request(url, data):
        response = requests.post(url, json=data)
        return response.json()