# etf_filter/etf_universe.py

import yfinance as yf
import pandas as pd
from config.settings import ETF_CSV_PATH

# 기본 ETF 후보 리스트 (거래량 상위 가능성 높은 ETF)
ETF_CANDIDATES = [
      'SPY', 'QQQ', 'DIA', 'IWM', 'TLT', 'HYG', 'XLF', 'XLK', 'XLY', 'XLI', 'XLV', 'XLE',
    'ARKK', 'VTI', 'IEMG', 'EFA', 'VWO', 'GDX', 'GLD', 'SLV', 'USO', 'XBI', 'SOXX', 'SMH',
    'BITO', 'SCHD', 'JEPI', 'VOO', 'VEA', 'VXUS', 'BND', 'LQD', 'EMB', 'SHV', 'XLC', 'XLRE']

def update_etf_csv(top_n=300):
    etf_data = []


    for ticker in ETF_CANDIDATES:
        try:
            df = yf.download(ticker, period='5d', progress=False)
            if df.empty or 'Volume' not in df.columns:
                continue
            volume_series = df['Volume'].dropna()
            if volume_series.empty:
                continue
            volume = float(volume_series.iloc[-1])
            etf_data.append((ticker, volume))
        except Exception as e:
            print(f"{ticker} 실패: {e}")
            continue

    etf_data = [(t, v) for t, v in etf_data if isinstance(v, (int, float))]
    top_etfs = sorted(etf_data, key=lambda x: x[1], reverse=True)[:top_n]

    df_out = pd.DataFrame(top_etfs, columns=['Ticker', 'Volume'])
    df_out.to_csv(ETF_CSV_PATH, index=False, encoding='cp949')
    print(f"✅ ETF 목록이 {ETF_CSV_PATH}에 저장되었습니다.")
