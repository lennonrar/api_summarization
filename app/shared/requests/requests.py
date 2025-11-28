import requests as http_requests


class RequestService:
    async def get_requests(self, url, json_response=True, params=None) -> str:
        response = http_requests.get(url, params=params)
        if not json_response:
            return response.content

        return response.json()

    @staticmethod
    def post_request(url, data):
        response = http_requests.post(url, json=data)
        return response.json()