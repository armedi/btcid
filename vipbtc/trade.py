from requests.auth import AuthBase
from urllib.parse import urlencode
import hashlib
import hmac
import time

from . import common

class vipAuth(AuthBase):
    def __init__(self, key, sign):
        # setup any auth-related data here
        self.key = key
        self.sign = sign
    def __call__(self, r):
        # modify and return the request
        r.headers['Key'] = self.key
        r.headers['Sign'] = self.sign
        return r

def nonce():
    time.sleep(1)
    return str(time.time()).split('.')[0]

def signature(secret, params):
    sig = hmac.new(secret.encode(), params.encode(), hashlib.sha512)
    return sig.hexdigest()


class TradeAPI:  
    def __init__(self, key, secret, requests_session=None):
        self.__key = key
        self.__secret = secret

        if requests_session is not None:
            self.__requests_session = requests_session
        else:
            self.__requests_session = common.Session()

    def __post(self, method, params):        
        url = 'https://vip.bitcoin.co.id/tapi'
        params['method'] = method
        params['nonce'] = nonce()
        auth = vipAuth(self.__key, signature(self.__secret, urlencode(params))) 
        response = self.__requests_session.api_request(url, params, auth, 'post')
        
        return response.json()

    def getInfo(self):
        return self.__post('getInfo', {})

    def transHistory(self):
        return self.__post('transHistory', {})

    def trade(self, ttype, amount, price):
        params = {
            "pair" : 'btc_idr',
            "type" : ttype,
            "price" : price}
        if ttype == 'buy':
            params['idr'] = amount
        elif ttype == 'sell':
            params['btc'] = amount
        return self.__post('trade', params)

    def tradeHistory(self, **kwargs):
        '''Arguments : count, from_id, end_id, order, since, end'''
        params = {"pair" : 'btc_idr'}
        if kwargs:
            for key, value in kwargs.items():
                params[key] = value
        return self.__post('tradeHistory', params)

    def openOrders(self):
        params = { "pair" : 'btc_idr' }
        return self.__post('openOrders', params)

    def cancelOrder(self, ttype, order_id):
        params = {
            'pair' : 'btc_idr',
            "order_id" : order_id,
            'type' : ttype}
        return self.__post('cancelOrder', params)