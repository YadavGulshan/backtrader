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
}


class TestStrategy(bt.Strategy):
    def next(self):
        cumsum_vol = self.data.cumulativevolume[0]
        cumsum_high = self.data.cumulativehigh[0]
        cumsum_low = self.data.cumulativelow[0]
        cumsum_open = self.data.cumulativeopen[0]
        cumsum_close = self.data.cumulativeclose[0]
        daily_high = self.data.dailyhigh[0]
        daily_low = self.data.dailylow[0]

        close = self.data.close[0]
        open = self.data.open[0]
        high = self.data.high[0]
        low = self.data.low[0]
        datetime = self.data.datetime.datetime()

        print(
            f"{datetime} - Close: {close}, Cumulative Volume: {cumsum_vol}, Cumulative"
            f" High: {cumsum_high}, Cumulative Low: {cumsum_low}"
            f" Cumulative Open: {cumsum_open}, Cumulative Close: {cumsum_close}"
            f" Daily High: {daily_high}, Daily Low: {daily_low}"
        )

        assert pd.notna(cumsum_vol)
        assert pd.notna(cumsum_high)
        assert pd.notna(cumsum_low)
        assert pd.notna(cumsum_open)
        assert pd.notna(cumsum_close)

        assert pd.notna(daily_high)
        assert pd.notna(daily_low)

        assert pd.notna(open)
        assert pd.notna(high)
        assert pd.notna(low)
        assert pd.notna(close)
        assert pd.notna(datetime)


def test_cumulative_pandas_data():
    global data
    df = pd.DataFrame(data)
    df.set_index("datetime", inplace=True)
    df = set_cumulative_data(df)
    df = set_daily_high_low(df)

    data = PandasData(dataname=df)
    cerebro = bt.Cerebro()
    # cerebro.adddata(data)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=2)
    cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=5)

    cerebro.addstrategy(TestStrategy)
    cerebro.run()


def set_cumulative_data(df):
    date_groups = df.groupby(df.index.date)

    df["cumulativevolume"] = date_groups["volume"].cumsum()
    df["cumulativeopen"] = date_groups["open"].cumsum()
    df["cumulativeclose"] = date_groups["close"].cumsum()
    df["cumulativehigh"] = date_groups["high"].cummax()
    df["cumulativelow"] = date_groups["low"].cummin()

    return df


def set_daily_high_low(df):
    date_groups = df.groupby(df.index.date)

    df["dailyhigh"] = date_groups["high"].transform(lambda x: x.cummax())
    df["dailylow"] = date_groups["low"].transform(lambda x: x.cummin())

    return df
