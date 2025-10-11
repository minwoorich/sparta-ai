from upbit import UpbitDataCollector

collector = UpbitDataCollector()

major_tickers = ["KRW-BTC", "KRW-ETH", "KRW-XRP", "KRW-DOGE", "KRW-ADA", "KRW-SOL"]

def collect_market_data(major_tickers):
    #  현재가 조회
    current_prices = collector.get_current_prices(major_tickers)
    for ticker, price in current_prices.items():
        print(f"{ticker}: {price:,} KRW")
    
    # OHLCV 데이터 조회 (최근 30일)
    ohlcv_data = collector.get_multiple_ohlcv(major_tickers, interval="day", count=30)
    print(f"OHLCV 데이터 수집 완료: {len(ohlcv_data)} 건")
    print(f"데이터 컬럼: {list(ohlcv_data.columns)}")

    return ohlcv_data, current_prices

raw_data, prices = collect_market_data(major_tickers)

# 가격 변동 컬럼 추가 (금액, 퍼센트)
raw_data["price_change"] = raw_data["close"] - raw_data["open"]
raw_data["price_change_pct"] = raw_data["price_change"] / raw_data["open"] * 100
raw_data["high_low_diff"] = raw_data["high"] - raw_data["low"]
raw_data["high_low_diff_pct"] = raw_data["high_low_diff"] / raw_data["open"] * 100

# 이동 평균 컬럼 추가
raw_data["ma5"] = raw_data["close"].rolling(window=5).mean().fillna(raw_data["close"])
raw_data["ma20"] = raw_data["close"].rolling(window=20).mean().fillna(raw_data["close"])
raw_data["ma60"] = raw_data["close"].rolling(window=60).mean().fillna(raw_data["close"])    
raw_data["ma120"] = raw_data["close"].rolling(window=120).mean().fillna(raw_data["close"])
raw_data["ma240"] = raw_data["close"].rolling(window=240).mean().fillna(raw_data["close"])

# 그룹바이
grouped_data = raw_data.groupby("ticker")

print(raw_data.head(10))