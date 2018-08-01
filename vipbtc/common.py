import requests
import time

class APIResponseError(Exception):
    """ Exception raise if the API replies with an HTTP code
    not in the 2xx range. """
    pass

class Session:
    def __init__(self):
        self.__requests_session = requests.Session()
        # self.__requests_session.headers.update({'User-Agent': 'medex'})

    def api_request(self, url, params=None, auth=None, http_call='get'):
        if http_call == 'get':
            response = self.__requests_session.get(url)
        elif http_call == 'post':
            response = self.__requests_session.post(url, data=params, auth=auth)
        
        if not response.ok:
            if response.status_code == 429:
                time.sleep(15)
            msg = "Status Code: {}".format(response.status_code)
            raise APIResponseError(msg)
        else:
            response = response.json()
        
        if "error" in response:
            msg = "Error: {}".format(response["error"])
            if "error_description" in response:
                msg = "{}; Description: {}".format(msg, response["error_description"])
            if response["error"] == "too_many_requests":
                time.sleep(15)
            raise APIResponseError(msg)
        
        return response
