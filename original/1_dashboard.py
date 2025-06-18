import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os
from db_utils import fetch_all_consulting

st.set_page_config(page_title="VOC 상담 분석 대시보드", layout="wide")
st.title("📅 VOC 상담 추이 분석")

# ✅ 환경 변수 로드 및 API 호출
load_dotenv()
API_URL_1 = os.getenv("API_URL_1")
df = fetch_all_consulting()

if df.empty:
    st.warning("상담 데이터를 불러올 수 없습니다.")
    st.stop()

# ✅ 날짜 전처리
df["consulting_datetime"] = pd.to_datetime(df["consulting_datetime"])
df["date"] = df["consulting_datetime"].dt.date

# ✅ KPI 카드 요약
daily = df.groupby("date").size().reset_index(name="total")
daily["diff"] = daily["total"].diff()
daily["rate"] = daily["diff"] / daily["total"].shift(1) * 100
latest = daily.iloc[-1]
prev = daily.iloc[-2]

col1, col2 = st.columns(2)
with col1:
    st.metric("총 상담 건수", f"{latest['total']}건", delta=f"{int(latest['diff'])}건")
with col2:
    st.metric("증가율", f"{latest['rate']:.1f}%", delta=f"{latest['rate'] - prev['rate']:.1f}%")

# ✅ 상담 추이 그래프
fig = px.line(daily, x="date", y="total", markers=True, title="📈 날짜별 상담 추이")
st.plotly_chart(fig, use_container_width=True)

# ✅ 카테고리 TOP5
st.subheader("🏆 최근 상담 카테고리 TOP5")
top5 = df["category_name"].value_counts().head(5).reset_index()
top5.columns = ["카테고리", "건수"]
st.dataframe(top5, use_container_width=True)

st.markdown("---")
st.caption("데이터 기반 VOC 분석 대시보드 (API 기반 실시간 데이터)")