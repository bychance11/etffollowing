# app.py

import streamlit as st
from etf_filter.calculator import run_filter_and_return
from etf_filter.etf_universe import update_etf_csv_and_prices


st.set_page_config(page_title="ETF 추세 필터", layout="centered")
st.title("📈 ETF 추세 반등 추적기")

st.markdown("""
이 앱은 최근 수익률 기준으로 '하락 후 반등'한 ETF를 자동으로 분석합니다.

`Yahoo Finance` 데이터를 기반으로 작동하며, 거래량 상위 ETF 목록도 갱신할 수 있습니다.\\
기준일은 조회일 기준 전 영업일 입니다.


|---------y주 전 --------|--------- x주 전 -------|

▲ 기준 시작점 (P₀)                   ▲ 반등 시작점 (P₁)                 ▲ 전일 종가 (P₂)

 - 하락률 계산   (P₁ - P₀) / P₀ * 100 

 - 반등률 계산            (P₂ - P₁) / P₁ * 100


""")

x = st.number_input("최근 주 수 (x)", min_value=1, max_value=12, value=2)
y = st.number_input("그 이전 주 수 (y)", min_value=1, max_value=12, value=4)
update_flag = st.checkbox("📌 거래량 기준 ETF 티커 업데이트(현재 불필요, 관리자가 업데이트중)")

if st.button("🔍 분석 시작(10초 이상 소요)"):
    if update_flag:
        update_etf_csv_and_prices()
        st.success("✅ ETF 목록이 성공적으로 갱신되었습니다.")

    result_df, excluded_df = run_filter_and_return(x, y)
    if result_df.empty:
        st.warning("조건에 맞는 ETF가 없습니다.")
        st.dataframe(excluded_df)
    else:
        st.success(f"{len(result_df)}개 ETF가 조건에 부합합니다.")
        st.dataframe(result_df)
        st.error(f"{len(excluded_df)}개 ETF가 조건에 부합하지 않습니다.")
        st.dataframe(excluded_df)
        # 결과 다운로드 버튼
        st.download_button(
            label="📥 결과 다운로드 (.csv)",
            data=result_df.to_csv(index=False).encode('utf-8-sig'),
            file_name="filtered_etfs.csv",
            mime="text/csv"
        )