# Factor model combined with portfolio optimization
- Two factors are chosen: momentum and size
- Three portfolio optimization models: Markowitz mean variance portfolio, inverse variance portfolio and hierarchy risk parity portfolio
- Two back test cases are considers: W/O transaction cost and with transaction cost
- Testing period: 20150101-20180108
- Transaction cost is estimated as (bid-ask)/mid price for each stock and apply to the backtest for each stock respectively.
- Bid and ask price are obtained via Pyspark with S3 TAQ data(20141201-20141230)
