from tickers.ticker import Ticker
from tickers.load_tickers import load_tickers
from telegram.ext import CallbackContext
from telegram import Update
from alpaca_trade_api.rest import REST


api = REST()


def daily_report(update: Update, context: CallbackContext) -> None:
    """Gives a daily report of followed tickers."""
    tickers = load_tickers()
    update.message.reply_text(_make_ticker_report(tickers))


def _make_ticker_report(tickers: list[Ticker]) -> str:
    report = ''
    for t in tickers:
        latest = api.get_latest_bar(t.symbol)
        report += f'{t.symbol} closed at {round(latest.c / t.prev_quarter_average * 100, 2)}% of previous quarter average.\n'
    return report
