import urllib3
from urllib3.exceptions import MaxRetryError
from urllib3.util import Retry, Timeout
import time
from settings import app_settings

def wait_for_server(url):
    retries = Retry(connect=100)
    timeout = Timeout(connect=30)
    http = urllib3.PoolManager(num_pools=1, retries=retries, timeout=timeout)
    while True:
        try:
            resp = http.request('GET',url)
            if resp.status == 200:
                break
            else:
                time.sleep(5)
        except MaxRetryError:
            pass

if __name__ == '__main__':
    url = f"http://{app_settings.APP_HOST}:{app_settings.APP_PORT}/api/openapi.json"
    wait_for_server(url)
