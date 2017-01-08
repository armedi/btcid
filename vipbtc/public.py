import pandas as pd

from . import common


def get_data(param, requests_session):
    if requests_session is None:
        requests_session = common.Session()

    url = 'https://vip.bitcoin.co.id/api/btc_idr/'+param
    
    return requests_session.api_request(url)


def getTicker(session=None):
    """
    Retrieve the ticker for the given pair.  Returns a Ticker instance.

    Arguments:
    session : vipbtc.Session object
    """

    response = get_data('ticker', requests_session=session).json()

    if not isinstance(response, dict):
        raise TypeError("The response is a %r, not a dict." % type(response))
    elif 'error' in response:
        print(("There is a error \"%s\" while obtaining ticker" % response['error'])) 
        ticker = None
    else:
        # ticker = Ticker(**response['ticker'])
        ticker = {}
        for s in ('high', 'low', 'vol_idr', 'last', 'buy', 'sell'):
            ticker[s] = int(response['ticker'].get(s))
        ticker['vol_btc'] = float(response['ticker'].get('vol_btc'))
        ticker['server_time'] = str(pd.to_datetime(response['ticker'].get('server_time'), unit='s'))

    return ticker


def getDepth(session=None):
    """
    Retrieve the depth for the given pair.  Returns a tuple (asks, bids);
    each of these is a list of (price, volume) tuples.
    
    Arguments:
    session : vipbtc.Session object
    """

    depth = get_data('depth', requests_session=session).json()
    if not isinstance(depth, dict):
        raise TypeError("The response is not a dict.")
    if not isinstance(depth.get('sell'), list):
        raise TypeError("The response does not contain an asks list.")
    if not isinstance(depth.get('buy'), list):
        raise TypeError("The response does not contain a bids list.")

    asks = pd.DataFrame(depth['sell'])
    asks.rename(columns={0:'price',1:'volume'},inplace=True)
    asks['volume'] = asks['volume'].apply(pd.to_numeric)

    bids = pd.DataFrame(depth['buy'])
    bids.rename(columns={0:'price',1:'volume'},inplace=True)
    bids['volume'] = bids['volume'].apply(pd.to_numeric)
    
    index = pd.MultiIndex.from_product([('asks', 'bids'),('price', 'volume')])

    df = pd.DataFrame(pd.concat([asks, bids], axis=1).values, columns=index)

    return df


def getTradeHistory(session=None):
    """
    Retrieve the trade history for the given pair.  Returns a list of
    Trade instances.
    
    Arguments:
    session : vipbtc.Session object
    """

    history = get_data('trades', requests_session=session).json()
    if not isinstance(history, list):
        raise TypeError("The response is a %r, not a list." % type(history))

    df = pd.DataFrame(history)
    df[['price', 'amount', 'tid']] = df[['price', 'amount', 'tid']].apply(pd.to_numeric)
    df.set_index('tid', inplace=True)
    df.date = pd.to_datetime(df.date, unit='s')
    df = df.reindex_axis(['date', 'price', 'amount', 'type'], axis=1)

    return df