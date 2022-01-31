import json

from alpaca_trade_api.rest import REST
from alpaca_trade_api.stream import Stream

from tickers.ticker import Ticker

api = REST()

TICKER_DATA_FILE = '/Users/jansen/Documents/personal_projs/alpaca/tickers/ticker_data.json'


def load_tickers() -> list[Ticker]:
    with open(TICKER_DATA_FILE) as f:
        tickers = json.load(f)
    return [Ticker(symbol=t, high=tickers[t]['high'], low=tickers[t]['low'], prev_quarter_average=tickers[t]['quarter_average']) for t in tickers.keys()]


async def trade_callback(t):
    print('trade', t)


async def quote_callback(q):
    print('quote', q)


def main():
    tickers = load_tickers()
    # stream = Stream()
    for t in tickers:
        latest = api.get_latest_bar(t.symbol)
        print(
            f'{t.symbol} closed at {round(latest.c / t.prev_quarter_average * 100, 2)}% of previous quarter average.')
        # stream.subscribe_quotes(quote_callback, 'IBM')
        # stream.subscribe_trades(trade_callback, 'AAPL')

    # stream.run()


if __name__ == "__main__":
    main()
