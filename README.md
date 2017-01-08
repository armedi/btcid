# btcid
Python wrapper for bitcoin.co.id API

Gunakan python versi 3

```sh
import vipbtc
```

Public API:
```sh
vipbtc.getTicker()
vipbtc.getDepth()
vipbtc.getTradeHistory()
```

Trade API:
```sh
key = "API key anda"
secret = "Secret key anda"

akun = vipbtc.TradeAPI(key, secret)

akun.getInfo()
akun.transHistory()
akun.trade(ttype, amount, price)
akun.tradeHistory()
akun.openOrders()
akun.cancelOrder(ttype, order_id)
```
