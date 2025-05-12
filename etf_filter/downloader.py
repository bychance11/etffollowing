# etf_filter/downloader.py

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd


def get_previous_business_day():
    today = datetime.today().date()

    # 오늘이 주말이면 금요일로 설정
    if today.weekday() == 0:  # 월요일인 경우
        previous_business_day = today - timedelta(days=3)  # 지난 금요일로 설정
    elif today.weekday() >= 5:  # 5 = 토요일, 6 = 일요일
        previous_business_day = today - timedelta(days=today.weekday() - 4)  # 지난 금요일로 설정
    else:
        previous_business_day = today - timedelta(days=1)  # 오늘이 평일이라면, 하루 전날을 가져옴

    return previous_business_day


def get_price_on_date(ticker, date):
    try:
        # Ticker 객체 생성
        stock = yf.Ticker(ticker)
        # 23:59:59까지의 데이터로 설정 (자정은 제외)
        end_date = date + timedelta(days=1)  # 날짜를 하루 더 추가하여 자정까지 포함

        # `history()` 메서드를 사용하여 주어진 날짜의 데이터 가져오기
        df = stock.history(start=date, end=end_date)

        if df.empty:
            print(f"No data available for {ticker} on {date}")
            return None

        # 종가를 반환 (해당 날짜의 종가)
        return df['Close'].iloc[0]  # 첫 번째 행 (해당 날짜의 종가)

    except Exception as e:
        print(f"⚠️ {ticker} 실패: {e}")
        return None