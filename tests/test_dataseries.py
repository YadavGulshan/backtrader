import pandas as pd

import backtrader as bt
from backtrader.feeds import PandasData

data = {
    "datetime": pd.date_range(start="2024-04-01 08:00:00", periods=10, freq="min"),
    "open": [
        0.7250,
        0.7150,
        0.7400,
        0.7399,
        0.7400,
        2.6500,
        2.6900,
        2.7300,
        2.7000,
        2.7000,
    ],
    "high": [
        0.7250,
        0.7400,
        0.7400,
        0.7399,
        0.7400,
        2.6800,
        2.7400,
        2.7400,
        2.7300,
        2.7300,
    ],
    "low": [
        0.7250,
        0.7150,
        0.7400,
        0.7399,
        0.7400,
        2.6500,
        2.6900,
        2.7300,
        2.7000,
        2.7000,
    ],
    "close": [
        0.7250,
        0.7400,
        0.7400,
        0.7399,
        0.7400,
        2.6800,
        2.7400,
        2.7400,
        2.7300,
        2.7300,
    ],
    "volume": [100, 200, 150, 300, 250, 400, 350, 300, 450, 500],
    "cumulativevolume": [100, 300, 450, 750, 1000, 1400, 1750, 2050, 2500, 3000],
    "cumulativehigh": [
        0.725,
        0.740,
        0.740,
        0.740,
        0.740,
        3.200,
        3.200,
        3.200,
        3.200,
        3.200,
    ],
    "cumulativelow": [
        0.725,
        0.715,
        0.715,
        0.715,
        0.715,
        1.670,
        1.670,
        1.670,
        1.670,
        1.670,
    ],
    "cumulativeopen": [
        0.725,
        0.715,
        0.740,
        0.7399,
        0.740,
        2.650,
        2.690,
        2.730,
        2.700,
        2.700,
    ],
    "cumulativeclose": [
        0.725,
        0.740,
        0.740,
        0.7399,
        0.740,
        2.680,
        2.740,
        2.740,
        2.730,
        2.730,
    ],
}


class TestStrategy(bt.Strategy):
    def next(self):
        cumsum_vol = self.data.cumulativevolume[0]
        cumsum_high = self.data.cumulativehigh[0]
        cumsum_low = self.data.cumulativelow[0]
        cumsum_open = self.data.cumulativeopen[0]
        cumsum_close = self.data.cumulativeclose[0]

        close = self.data.close[0]
        open = self.data.open[0]
        high = self.data.high[0]
        low = self.data.low[0]
        datetime = self.data.datetime.datetime()

        print(
            f"{datetime} - Close: {close}, Cumulative Volume: {cumsum_vol}, Cumulative"
            f" High: {cumsum_high}, Cumulative Low: {cumsum_low}"
            f" Cumulative Open: {cumsum_open}, Cumulative Close: {cumsum_close}"
        )

        assert pd.notna(cumsum_vol)
        assert pd.notna(cumsum_high)
        assert pd.notna(cumsum_low)
        assert pd.notna(cumsum_open)
        assert pd.notna(cumsum_close)
        assert pd.notna(open)
        assert pd.notna(high)
        assert pd.notna(low)
        assert pd.notna(close)
        assert pd.notna(datetime)


def test_cumulative_pandas_data():
    global data
    df = pd.DataFrame(data)
    df.set_index("datetime", inplace=True)
    data = PandasData(dataname=df)
    cerebro = bt.Cerebro()
    # cerebro.adddata(data)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=2)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=5)

    cerebro.addstrategy(TestStrategy)
    cerebro.run()
