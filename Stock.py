import pandas as pd
import yfinance as yf


def analyze_stock(ticker_symbol):
  stock = yf.Ticker(ticker_symbol.upper())

  # Get historical data for price and percent change
  hist = stock.history(period="2d")
  if hist.empty:
    print(f"Could not find price data for ticker: {ticker_symbol.upper()}")
    return

  current_price = hist["Close"].iloc[-1]
  prev_close = hist["Close"].iloc[-2]
  percent_change = ((current_price - prev_close) / prev_close) * 100
  volume = hist["Volume"].iloc[-1]

  print(f"\n=== Market Summary: {ticker_symbol.upper()} ===")
  print(f"Current Price: ${current_price:.2f}")
  print(f"Performance: {percent_change:+.2f}%")
  print(f"Stock Volume: {volume:,}")

  # Options Data
  try:
    exp_dates = stock.options
    if exp_dates:
      # Pull options chain for the nearest expiration date
      nearest_exp = exp_dates[0]
      chain = stock.option_chain(nearest_exp)

      print(f"\n--- Options Highlights (Expiration: {nearest_exp}) ---")

      # Highest Volume Call
      calls = chain.calls.copy()
      calls["volume"] = calls["volume"].fillna(0)
      if not calls.empty and calls["volume"].sum() > 0:
        max_call = calls.loc[calls["volume"].idxmax()]
        print(
            "Highest Volume Call: "
            f"Strike ${max_call['strike']} | "
            f"Volume: {int(max_call['volume']):,} | "
            f"Last Price: ${max_call['lastPrice']:.2f}"
        )
      else:
        print("Highest Volume Call: None/Zero volume traded")

      # Highest Volume Put
      puts = chain.puts.copy()
      puts["volume"] = puts["volume"].fillna(0)
      if not puts.empty and puts["volume"].sum() > 0:
        max_put = puts.loc[puts["volume"].idxmax()]
        print(
            "Highest Volume Put:  "
            f"Strike ${max_put['strike']} | "
            f"Volume: {int(max_put['volume']):,} | "
            f"Last Price: ${max_put['lastPrice']:.2f}"
        )
      else:
        print("Highest Volume Put: None/Zero volume traded")
    else:
      print("\nNo options chain available for this ticker.")
  except Exception as e:
    print(f"\nCould not fetch options data: {e}")


if __name__ == "__main__":
  user_ticker = input("Enter stock ticker symbol (e.g., AAPL, NVDA, TSLA): ")
  analyze_stock(user_ticker)