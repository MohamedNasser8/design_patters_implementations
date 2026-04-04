from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
import requests
from typing import Optional, Self

class HttpRequest:
    def __init__(self):
        self.method: Optional[str] = None
        self.url: str = ""
        self.headers: Optional[dict] = None
        self.body: Optional[dict] = None
        self.query_params: Optional[dict] = None
        self.path_params: Optional[dict] = None
        self.auth: Optional[dict] = None
        self.timeout: Optional[int] = None
        self.retries: Optional[int] = None

class HttpBuilder(ABC):
    def __init__(self):
        self.request = HttpRequest()

    def set_url(self, url: str) -> Self:
        self.request.url = url
        return self

    def set_headers(self, headers: dict) -> Self:
        self.request.headers = headers
        return self

    @abstractmethod
    def set_body(self, body: dict) -> Self:
        pass

    def set_method(self, method: str) -> Self:
        self.request.method = method
        return self

    def set_query_params(self, query_params: dict) -> Self:
        self.request.query_params = query_params
        return self

    def set_path_params(self, path_params: dict) -> Self:
        self.request.path_params = path_params
        return self

    def set_auth(self, auth: dict) -> Self:
        self.request.auth = auth
        return self

    def set_timeout(self, timeout: int) -> Self:
        self.request.timeout = timeout
        return self

    def set_retries(self, retries: int) -> Self:
        self.request.retries = retries
        return self

    def build(self) -> HttpRequest:
        return self.request



class RegularHttpBuilder(HttpBuilder):
    def set_body(self, body: dict) -> HttpBuilder:
        self.request.body = body
        return self

class JsonHttpBuilder(HttpBuilder):
    def set_body(self, body: dict) -> HttpBuilder:
        self.request.body = body
        return self

class XmlHttpBuilder(HttpBuilder):
    def set_body(self, body: dict) -> HttpBuilder:
        self.request.body = ET.fromstring(body)
        return self


class HttpDirector:
    def __init__(self, builder: HttpBuilder):
        self.builder = builder

    def build_regular_GET_request(self, url: str, headers: dict) -> HttpRequest:
        self.builder.set_url(url)
        self.builder.set_method("GET")
        self.builder.set_headers(headers)
        self.builder.set_timeout(10)
        self.builder.set_retries(3)
        self.builder.set_auth({"username": "testuser", "password": "testpassword"})
        return self.builder.build()
    
    def change_builder(self, builder: HttpBuilder):
        self.builder = builder
    
    def send_request(self, request: HttpRequest):
        return requests.request(method=request.method, url=request.url, headers=request.headers, json=request.body, params=request.query_params, timeout=request.timeout)