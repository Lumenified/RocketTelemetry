import requests

def make_request_with_retry(url, headers, method='GET', max_retries=5, id=None, single=False):
    for attempt in range(max_retries):
        try:
            if method == 'GET':
                response = requests.get(url=url, headers=headers)
                if single is True and id is not None:
                    print(f"Retrying {method} request (Attempt {attempt + 1})")
                    return next((item for item in response.json() if item['id'] == id), None)
            elif method == 'PUT':
                response = requests.put(url=url, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url=url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()
        except Exception as err:
            if attempt < max_retries - 1 and isinstance(err, requests.exceptions.HTTPError):
                if err.response.status_code == 503 or err.response.status_code == 400:
                    if method in ["PUT", "DELETE"]:
                        url = "http://localhost:5000/rockets"
                        if method == "PUT" and "launched" in url:
                            headers.pop('Content-Type', None)
                        method="GET"
                        continue
            else:
                print(str(err) + " voila")