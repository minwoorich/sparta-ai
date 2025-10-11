import pyupbit
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import time
import warnings

# 경고 메시지 숨기기
warnings.filterwarnings("ignore")


# 한글 폰트 설정
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False


class UpbitDataCollector:
    """Upbit API를 활용한 데이터 수집 클래스"""

    def __init__(self):
        self.supported_tickers = None

    def get_krw_tickers(self):
        """KRW 마켓의 모든 티커 조회"""
        try:
            tickers = pyupbit.get_tickers(fiat="KRW")
            self.supported_tickers = tickers
            return tickers
        except Exception as e:
            print(f"티커 조회 오류: {e}")
            return []

    def get_current_prices(self, tickers):
        """현재가 조회"""
        try:
            return pyupbit.get_current_price(tickers)
        except Exception as e:
            print(f"현재가 조회 오류: {e}")
            return None

    def get_ohlcv_data(self, ticker, interval="day", count=30):
        """OHLCV 데이터 조회"""
        try:
            df = pyupbit.get_ohlcv(ticker, interval=interval, count=count)
            if df is not None:
                df["ticker"] = ticker
                df.reset_index(inplace=True)
            return df
        except Exception as e:
            print(f"{ticker} OHLCV 데이터 조회 오류: {e}")
            return None

    def get_multiple_ohlcv(self, tickers, interval="day", count=30, delay=0.1) -> pd.DataFrame:
        """여러 티커의 OHLCV 데이터 일괄 조회"""
        all_data = []

        for ticker in tickers:
            print(f"{ticker} 데이터 수집 중...")
            data = self.get_ohlcv_data(ticker, interval, count)
            if data is not None:
                all_data.append(data)
            time.sleep(delay)  # API 호출 제한 고려

        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()
