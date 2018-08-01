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
    time.sleep(1/1000)
    return str(int(time.time()*1000))

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
        url = 'https://indodax.com/tapi'
        params['method'] = method
        params['nonce'] = nonce()
        auth = vipAuth(self.__key, signature(self.__secret, urlencode(params))) 
        response = self.__requests_session.api_request(url, params, auth, 'post')
        
        return response['return']

    def getInfo(self):
        return self.__post('getInfo', {})

    def transHistory(self):
        return self.__post('transHistory', {})

    def trade(self, pair, ttype, amount, price):
        params = {
            "pair" : pair,
            "type" : ttype,
            "price" : price}
        if ttype == 'buy':
            params[pair[-3:]] = amount
        elif ttype == 'sell':
            params[pair[:3]] = amount
        return self.__post('trade', params)

    def tradeHistory(self, pair, **kwargs):
        '''Keyword arguments : count, from_id, end_id, order, since, end'''
        params = {
            "pair" : pair
        }
        if kwargs:
            for key, value in kwargs.items():
                params[key] = value
        return self.__post('tradeHistory', params)

    def openOrders(self, pair):
        params = { "pair" : pair }
        return self.__post('openOrders', params)
    
    def orderHistory(self, pair, **kwargs):
        '''Keyword arguments : count, from'''
        params = {
            "pair" : pair
        }
        if kwargs:
            for key, value in kwargs.items():
                params[key] = value
        return self.__post('orderHistory', params)

    def getOrder(self, pair, order_id):
        params = {
            "pair" : pair,
            "order_id" : order_id
        }
        return self.__post('getOrder', params)

    def cancelOrder(self, pair, ttype, order_id):
        params = {
            'pair' : pair,
            "order_id" : order_id,
            'type' : ttype}
        return self.__post('cancelOrder', params)
