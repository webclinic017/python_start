import yfinance as yf
kuaishou = yf.Ticker("1024.HK")
# print(msft.info)
kuaishou_hist = kuaishou.history(period="max")
kuaishou_hist.to_csv("strategy/1024.HK.csv")