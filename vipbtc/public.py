import pandas as pd

from . import common


def get_data(pair, param, requests_session):
    if requests_session is None:
        requests_session = common.Session()

    url = 'https://indodax.com/api/'+pair+'/'+param

    response = requests_session.api_request(url)
    
    return response


def getTicker(pair="btc_idr", session=None):
    """
    Retrieve the ticker for the given pair.  Returns a Ticker instance.

    Arguments:
    pair : trading pair
    session : vipbtc.Session object
    """
    pair_counter, pair_base = pair.split('_')

    response = get_data(pair, 'ticker', requests_session=session)

    ticker = {}
    for s in ('high', 'low', 'last', 'buy', 'sell', 'server_time'):
        tick = response['ticker'].get(s)
        ticker[s] = float(tick) if pair_base == 'btc' and s != 'server_time' else int(tick)

    vol_base = "vol_" + pair_base
    vol_counter = "vol_" + pair_counter

    for s in (vol_base, vol_counter):
        ticker[s] = float(response['ticker'].get(s))

    return ticker


def getDepth(pair="btc_idr", session=None):
    """
    Retrieve the depth for the given pair.  Returns a dictionary of asks and bids dataframe.
    
    Arguments:
    pair : trading pair
    session : vipbtc.Session object
    """

    depth = get_data(pair, 'depth', requests_session=session)

    asks = pd.DataFrame(depth['sell'])
    asks.rename(columns={0:'price',1:'volume'},inplace=True)
    asks[['price', 'volume']] = asks[['price', 'volume']].apply(pd.to_numeric)

    bids = pd.DataFrame(depth['buy'])
    bids.rename(columns={0:'price',1:'volume'},inplace=True)
    bids[['price', 'volume']] = bids[['price', 'volume']].apply(pd.to_numeric)

    return {"Asks": asks, "Bids": bids}


def getTradeHistory(pair="btc_idr", session=None):
    """
    Retrieve the trade history for the given pair.  Returns a pandas dataframe.
    
    Arguments:
    pair : trading pair
    session : vipbtc.Session object
    """

    history = get_data(pair, 'trades', requests_session=session)

    df = pd.DataFrame(history)
    df[['date' , 'price', 'amount', 'tid']] = df[['date' , 'price', 'amount', 'tid']].apply(pd.to_numeric)
    df.set_index(df.tid.values , drop=False, inplace=True)
    df = df.reindex(columns=['tid', 'date', 'price', 'amount', 'type'])

    return df
