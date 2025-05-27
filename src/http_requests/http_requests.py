import requests

class HttpRequests:
    def get_request(url):
        try:
            response = requests.get(url)

            if response.status_code == requests.codes.ok:
                return response.json()
            else:
                raise requests.exceptions.RequestException
        except requests.exceptions.HTTPError as e:
            raise Exception(f'Error in get request: {e}')
