import json
import logging
from datetime import date, timedelta

from alpaca_trade_api.rest import REST
from numpy import average

TODAY = date.today()
api = REST()
logging.basicConfig(level=logging.INFO)


def get_ticker_data(tickers: list[str]) -> dict[str, dict[str, float]]:
    ticker_data = {}
    for t in tickers:
        trades = api.get_bars(
            t,
            start=(TODAY-timedelta(days=365)).isoformat(),
            end=(TODAY-timedelta(days=2)).isoformat(),
            timeframe="1Day",
            limit=1000,
        )
        logging.info(f"Recieved {len(trades)} bars for {t}.")

        highs = [bar.h for bar in trades]
        lows = [bar.l for bar in trades]

        hi = max(highs)
        lo = min(lows)

        logging.info(f'Highest {t} price for the last year: ${hi}')
        logging.info(f'Lowest {t} price for the last year: ${lo}')

        ticker_data[t] = {'high': hi, 'low': lo, 'quarter_average': average(
            [bar.c for bar in trades[-90:]])}
    return ticker_data


def main():
    tickers = ['AAPL', 'MSFT', 'TSLA', 'TEAM', 'GTLB', 'GOOGL', 'PFE', 'NVDA']
    ticker_data = get_ticker_data(tickers)
    with open('ticker_data.json', 'w') as file:
        json.dump(ticker_data, file)


if __name__ == "__main__":
    main()
