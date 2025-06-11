# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(page_title="VOC 상담 분석 대시보드", layout="wide")

st.title("📅 VOC 상담 추이 분석")
st.caption("전반적인 문의량 증가로 신규 이슈가 있었습니다.")

# ✅ 상단 제어 버튼 영역
with st.container():
    col1, col2, col3 = st.columns([1.5, 1, 3])
    with col1:
        st.button("🔄 데이터 동기화하기")
    with col2:
        st.selectbox("📆 단위", ["일", "주", "월"], index=1)
    with col3:
        st.selectbox("비교 기간", ["30일", "60일", "90일"], index=0)

st.markdown("---")

# ✅ KPI 카드 요약 (전체 문의 수 & 부정 비율 기반 클레임 대체)
total = 1024
total_prev = 991
positive = 804
negative = 220

percent_negative = round((negative / total) * 100, 1)
percent_negative_prev = round((180 / total_prev) * 100, 1)
delta_negative = percent_negative - percent_negative_prev

total_diff = total - total_prev

total_col, neg_col = st.columns(2)
with total_col:
    st.metric(label="총 상담 건수", value=f"{total}건", delta=f"{total_diff}건 ({round((total_diff / total_prev) * 100, 1)}%)")
with neg_col:
    st.metric(label="부정 응답률", value=f"{percent_negative}%", delta=f"{delta_negative:+.1f}%")

st.markdown("---")

# ✅ 추이 그래프 (일별 문의 수)
date_data = pd.DataFrame({
    "날짜": pd.date_range(start="2024-06-17", periods=29),
    "문의 수": [25, 13, 18, 15, 14, 3, 2, 14, 17, 16, 16, 16, 7, 2, 28, 19, 12, 13, 9, 21, 18, 16, 15, 13, 17, 12, 6, 8, 25]
})
fig = px.line(date_data, x="날짜", y="문의 수", markers=True, title="📈 문의 건수 추이")
st.plotly_chart(fig, use_container_width=True)

# ✅ 감정 분석 (막대그래프)
st.subheader("😊 감정 분석 결과")
sentiment_df = pd.DataFrame({
    "감정": ["긍정", "부정"],
    "건수": [positive, negative]
})
fig_sentiment = px.bar(sentiment_df, x="감정", y="건수", color="감정",
                       title="긍정/부정 감정 응답 수", text_auto=True,
                       color_discrete_map={"긍정": "#2ca02c", "부정": "#d62728"})
fig_sentiment.update_layout(showlegend=False)
st.plotly_chart(fig_sentiment, use_container_width=True)

# ✅ 일자별 상세 테이블
st.subheader("📅 일자별 VOC 통계")
st.dataframe(date_data.rename(columns={"날짜": "일자"}).set_index("일자"), use_container_width=True)

st.markdown("---")

# 📞 채널별 상담 비율
st.subheader("📞 채널별 상담 비율")
pie_data = pd.DataFrame({
    "channel": ["콜센터", "챗봇", "홈페이지"],
    "count": [450, 380, 194]
})
fig1 = px.pie(pie_data, names='channel', values='count', title='채널 비중')
st.plotly_chart(fig1, use_container_width=True)

# 🗓 요일별 상담 건수
st.subheader("🗓 요일별 상담 건수")
bar_data = pd.DataFrame({
    "요일": ["월", "화", "수", "목", "금", "토", "일"],
    "건수": [130, 160, 190, 220, 180, 80, 64]
})
fig2 = px.bar(bar_data, x="요일", y="건수", title="요일별 상담량")
st.plotly_chart(fig2, use_container_width=True)

# 🏆 상담 시나리오 TOP5
st.subheader("🏆 최근 상담 카테고리 TOP5")
scenario_data = pd.DataFrame({
    "순위": [1, 2, 3, 4, 5],
    "시나리오": ["요금제 변경", "해지 요청", "신규 가입", "단말기 문제", "데이터 추가"],
    "건수": [201, 188, 160, 140, 115]
})
st.dataframe(scenario_data, use_container_width=True)

# ⏰ 시간대별 상담 분포
st.subheader("⏰ 시간대별 상담 분포")
time_data = pd.DataFrame({
    "시간대": [f"{i}시" for i in range(24)],
    "건수": [5, 8, 12, 20, 50, 80, 110, 130, 160, 190, 180, 160,
             140, 130, 120, 100, 90, 70, 50, 30, 20, 15, 10, 5]
})
fig3 = px.line(time_data, x="시간대", y="건수", markers=True, title="시간대별 상담량 추이")
st.plotly_chart(fig3, use_container_width=True)

# 📈 주차별 감정 변화 추이
st.subheader("📈 주차별 감정 변화 추이")
sentiment_weekly = pd.DataFrame({
    "주차": ["1주차", "2주차", "3주차", "4주차"],
    "긍정": [80, 75, 70, 60],
    "부정": [20, 25, 30, 40]
})
fig4 = px.line(sentiment_weekly, x="주차", y=["긍정", "부정"], markers=True, title="긍정/부정 추이")
st.plotly_chart(fig4, use_container_width=True)

# 🔑 상담 키워드 워드클라우드
st.subheader("🔑 상담 키워드 워드클라우드")
keywords = ["요금", "해지", "데이터", "이벤트", "혜택", "단말기", "속도", "상담원", "고장", "요금"] * 10 + ["불만", "서비스", "해지"] * 5
keyword_freq = dict(Counter(keywords))

if keyword_freq:
    wc = WordCloud(
        width=800,
        height=400,
        background_color="#f9f9f9",
        font_path="/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        colormap="Set2",
        prefer_horizontal=0.9,
        max_words=100
    )
    wc.generate_from_frequencies(keyword_freq)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
else:
    st.info("표시할 키워드가 없습니다.")