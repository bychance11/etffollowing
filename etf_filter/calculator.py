import pandas as pd
from datetime import datetime, timedelta
from etf_filter.downloader import get_price_on_date
from config.settings import ETF_CSV_PATH
from etf_filter.downloader import get_previous_business_day

def get_date_ranges(x, y):
    end_date = get_previous_business_day()
    x_start = end_date - timedelta(weeks=x)
    y_start = x_start - timedelta(weeks=y)
    return y_start, x_start, end_date


def run_filter_and_return(x, y):
    df_etf = pd.read_csv(ETF_CSV_PATH, encoding='cp949')
    tickers = df_etf['Ticker'].dropna().unique().tolist()

    y_start, x_start, end_date = get_date_ranges(x, y)
    results = []  # 필터에 포함된 ETF
    excluded = []  # 필터에 제외된 ETF
    logs = []

    for ticker in tickers:
        prior_price = get_price_on_date(ticker, pd.to_datetime(y_start))
        x_price = get_price_on_date(ticker, pd.to_datetime(x_start))
        end_price = get_price_on_date(ticker, pd.to_datetime(end_date))

        if not prior_price or not x_price or not end_price:
            logs.append(f"{ticker}: 가격 데이터 없음 → 제외")
            excluded.append({'Ticker': ticker, 'Reason': 'No price data'})  # 제외 이유와 함께 저장
            continue

        prior_return = (x_price - prior_price) / prior_price * 100
        recent_return = (end_price - x_price) / x_price * 100

        if prior_return < 0 and recent_return > 0:
            results.append({
                'Ticker': ticker,
                'Prior Return (%)': round(prior_return, 2),
                'Recent Return (%)': round(recent_return, 2)
            })
        else:
            logs.append(f"{ticker}: prior={prior_return:.2f}%, recent={recent_return:.2f}% → 제외")
            excluded.append({'Ticker': ticker,
                             'Prior Return (%)': round(prior_return, 2),
                             'Recent Return (%)': round(recent_return, 2)})  # 제외된 ETF 저장

    if logs:
        print("\n[필터링 로그]")
        for line in logs:
            print(line)

    print(f"\n총 대상 ETF 수: {len(tickers)}개")
    print(f"하락 후 반등한 ETF 수: {len(results)}개")


    return pd.DataFrame(results), pd.DataFrame(excluded)