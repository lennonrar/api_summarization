import requests as http_requests


class RequestService:

    def __init__(self):
        self.default_headers = {"User-Agent": 'api_summarization_test'}
        self.respect_robots = True
    async def get_data(self, url, json_response=True, params=None, headers: dict | None = None) -> str:
        req_headers = dict(self.default_headers)
        req_headers.update(headers or {})
        response = http_requests.get(url, params=params, headers=req_headers, timeout=10)
        if not json_response:
            return response.content

        return response.json()

    def post_data(self, url, data, headers: dict | None = None):
        req_headers = dict(self.default_headers)
        req_headers.update(headers or {})
        response = http_requests.post(url, json=data, headers=req_headers, timeout=20)
        return response.json()