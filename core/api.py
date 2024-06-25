import requests
from core.core import Config


class API:
    def __init__(self):
        self.config = Config()

        self.api_endpoint = self.config.API_PRODUCTION_ENDPOINT \
            if self.config.APP_DEBUG.lower() == "false" else self.config.API_TEST_ENDPOINT
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        match self.config.API_AUTHORIZATION:
            case "Bearer":
                self.headers['Authorization'] = f"Bearer {self.config.API_BEARER_TOKEN}"
            case None:
                pass

    def append_headers(self, headers: dict) -> None:
        for i in range(len(headers)):
            header = list(headers.keys())[i]
            value = list(headers.values())[i]
            self.headers[header] = value

    def get(self, endpoint: str, payload: dict = None):
        if payload is not None:
            endpoint = endpoint + "?"

            for i in range(len(payload)):
                key = list(payload.keys())[i]
                value = list(payload.values())[i]
                endpoint += str(key) + "=" + str(value)
                if i < len(payload):
                    endpoint += "&"

        return self.send_request('get', endpoint, payload)

    def post(self, endpoint: str, payload: dict = None):
        return self.send_request('post', endpoint, payload)

    def put(self, endpoint: str, payload: dict):
        return self.send_request('put', endpoint, payload)

    def send_request(self, method: str, endpoint: str, payload: dict = None):
        request_method = getattr(requests, method)

        response = request_method(
            self.api_endpoint + endpoint,
            headers=self.headers,
            json=payload
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return None

        return response.json()
