import requests
from urllib.error import HTTPError

def make_request_with_retry(url, headers, method='GET', max_retries=5):
    for attempt in range(max_retries):
        try:
            if method == 'GET':
                response = requests.get(url=url, headers=headers)
            elif method == 'PUT':
                response = requests.put(url=url, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url=url, headers=headers)
            else:
                # Handle other HTTP methods if needed
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 503 and attempt < max_retries - 1:
                # Retry the request if it's a 503 error
                print(f"Retrying {method} request (Attempt {attempt + 1})")
            else:
                # Raise the exception if it's not a 503 error or if max_retries is reached
                print(http_err)