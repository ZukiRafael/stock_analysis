from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import pandas as pd
from alpaca_secrets.alpaca_keys import alpaca_secret, alpaca_key


def _verify_dates(dates=None):
    if dates and (len(dates) == 2):
        start = dates[0]
        end = dates[1]
    else:
        start, end = sdk.get_bar_times()
    return start, end


def get_daily_stock_bar_data(ticker,
                             time_frame=TimeFrame(1, TimeFrameUnit.Minute),
                             dates=None):
    start, end = _verify_dates(dates)
    alpaca = REST(alpaca_key, alpaca_secret)
    df = alpaca.get_bars(ticker, time_frame, start, end, adjustment='raw').df
    return df


def fetch_data(ticker, year):
    start_date = year + '-01-01'
    end_date = year + '-12-31'
    if year == 'ytd':
        start_date = "2022-01-01"
        end_date = "2022-09-08"
    df = get_daily_stock_bar_data(ticker, dates=[start_date, end_date])
    df.to_csv("../export/" + ticker + "-" + year + ".csv")
    return df


if __name__ == "__main__":
    target_ticker = 'NFLX'
    years = ['ytd'] + [str(yr) for yr in range(2021, 2002, -1)]
    for year in years:
        fetch_data(target_ticker, year)
