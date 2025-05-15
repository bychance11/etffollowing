from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from config.settings import ETF_CSV_PATH, ETF_PRICE_PATH  # ETF_PRICE_PATH는 새로 지정

ETF_CANDIDATES = [
    'SPY', 'QQQ', 'DIA', 'IWM', 'TLT', 'HYG', 'XLF', 'XLK', 'XLY', 'XLI', 'XLV', 'XLE',
    'ARKK', 'VTI', 'IEMG', 'EFA', 'VWO', 'GDX', 'GLD', 'SLV', 'USO', 'XBI', 'SOXX', 'SMH',
    'BITO', 'SCHD', 'JEPI', 'VOO', 'VEA', 'VXUS', 'BND', 'LQD', 'EMB', 'SHV', 'XLC', 'XLRE'
]

def update_etf_csv_and_prices(top_n=300):
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)
    six_months_ago = today - timedelta(days=180)

    etf_data = []

    # ✅ Step 1: 거래량 기준 top_n ETF 선정
    for ticker in ETF_CANDIDATES:
        try:
            df = yf.download(ticker, start=today, end=tomorrow, progress=False)
            if df.empty or 'Volume' not in df.columns:
                continue

            volume_series = df['Volume'].dropna()
            if volume_series.empty:
                continue

            volume = float(volume_series.iloc[0])
            etf_data.append((ticker, volume))
        except Exception as e:
            print(f"{ticker} 실패: {e}")
            continue

    etf_data = [(t, v) for t, v in etf_data if isinstance(v, (int, float))]
    top_etfs = sorted(etf_data, key=lambda x: x[1], reverse=True)[:top_n]

    # ✅ Step 2: 기본 ETF 목록 저장
    df_out = pd.DataFrame(top_etfs, columns=['Ticker', 'Volume'])
    df_out.to_csv(ETF_CSV_PATH, index=False, encoding='cp949')
    print(f"✅ ETF 목록이 {ETF_CSV_PATH}에 저장되었습니다.")

    # ✅ Step 3: 6개월 종가 데이터 수집
    price_records = []

    for ticker, _ in top_etfs:
        try:
            df_price = yf.download(ticker, start=six_months_ago, end=today + timedelta(days=1), progress=False)
            if df_price.empty:
                print(f"{ticker} 데이터 없음")
                continue

            # 멀티인덱스 컬럼일 경우 해제
            if isinstance(df_price.columns, pd.MultiIndex):
                df_price.columns = [col[0] for col in df_price.columns]

            df_price = df_price.reset_index()

            if 'Close' not in df_price.columns:
                print(f"{ticker} 종가 다운로드 실패: 'Close' 컬럼 없음")
                continue

            df_price['Ticker'] = ticker
            df_price = df_price[['Date', 'Close', 'Ticker']]
            price_records.append(df_price)

        except Exception as e:
            print(f"{ticker} 종가 다운로드 실패: {e}")
            continue

    if price_records:
        df_prices_all = pd.concat(price_records, ignore_index=True)

        # 중복 컬럼 제거 (혹시라도 concat 후 중복이 생긴 경우)
        df_prices_all = df_prices_all.loc[:, ~df_prices_all.columns.duplicated()]

        df_prices_all = df_prices_all.sort_values(by=['Date', 'Ticker', 'Close'])

        df_prices_all.to_csv(ETF_PRICE_PATH, index=False, encoding='cp949')
        print(f"✅ ETF 가격 정보가 {ETF_PRICE_PATH}에 저장되었습니다.")
    else:
        print("❌ 저장할 ETF 가격 데이터가 없습니다.")