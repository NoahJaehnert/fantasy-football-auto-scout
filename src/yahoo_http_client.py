import random
import time
from os import path
from pathlib import Path
from typing import Optional

import requests

from src.constants import base_url
from src.env import request_cookie

min_seconds_between_requests: float = 5
max_seconds_between_requests: float = 10


class YahooHttpClient:
    __last_http_request: Optional[float] = None

    def get(self, url_path: str) -> str:
        url = '%s%s' % (base_url, url_path)
        cache_dir = '.cache'
        Path(cache_dir).mkdir(exist_ok=True)
        cache_file_path = path.join(
            cache_dir,
            '%s.html' % url.replace('/', ':')
        )
        cached_html = self.__get_from_cache(cache_file_path)
        if cached_html is not None:
            return cached_html
        self.__conditionally_sleep()
        html = requests.get(url, headers={'cookie': request_cookie}).text
        self.__update_last_http_request_time()
        with open(cache_file_path, 'w+') as cached_file:
            cached_file.write(html)
        return html

    @staticmethod
    def __conditionally_sleep() -> None:
        if YahooHttpClient.__last_http_request is not None:
            seconds_since_last_http_request = time.time() - YahooHttpClient.__last_http_request
            randomized_throttle_buffer = random.uniform(min_seconds_between_requests, max_seconds_between_requests)
            sleep_time = max(randomized_throttle_buffer - seconds_since_last_http_request, 0)
            time.sleep(sleep_time)

    @staticmethod
    def __update_last_http_request_time() -> None:
        YahooHttpClient.__last_http_request = time.time()

    @staticmethod
    def __get_from_cache(cache_file_path: str) -> Optional[str]:
        if path.exists(cache_file_path):
            with open(cache_file_path) as cached_file:
                return cached_file.read()
