# btcid
Python wrapper for indodax.com API

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
akun.trade()
akun.tradeHistory()
akun.openOrders()
akun.orderHistory()
akun.getOrder()
akun.cancelOrder()
```
