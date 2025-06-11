# report.py 
import streamlit as st
from datetime import datetime, timedelta
from db_utils import (
    fetch_consultings_by_day,
    calculate_negative_stats,
    fetch_consulting_detail,
    get_top_categories,
    get_top_keywords,
    get_daily_trend
)   
import plotly.express as px

st.set_page_config(page_title="일일 리포트", layout="wide")
st.title("📊 VOC 일일 리포트")

# 날짜 기준 설정 (오늘 = 기준일, 어제/그제 비교)
today = datetime.today().date()
yesterday = today - timedelta(days=1)

# 문의 수
df_today = fetch_consultings_by_day(today)
df_yesterday = fetch_consultings_by_day(yesterday)

count_t = len(df_today)
count_y = len(df_yesterday)
diff = count_t - count_y

st.markdown("---")

st.subheader("📌 문의 수 요약")
col1, col2 = st.columns(2)
with col1:
    st.metric(label=str(yesterday), value=f"{count_y}건")
with col2:
    st.metric(label=str(today), value=f"{count_t}건", delta=f"{diff:+}건")

st.markdown("---")

# 부정 응답률
neg_count_t, neg_rate_t = calculate_negative_stats(df_today["consulting_id"])
neg_count_y, neg_rate_y = calculate_negative_stats(df_yesterday["consulting_id"])

st.subheader("😡 부정 응답률")
st.markdown(f"- 어제 부정 응답 건수: **{neg_count_y}건** ({neg_rate_y})")
st.markdown(f"- 오늘 부정 응답 건수: **{neg_count_t}건** ({neg_rate_t})")

st.markdown("---")

st.subheader("😥 고객 불만 내용 모아보기")

neg_texts = []

for cid in df_yesterday["consulting_id"]:
    try:
        detail = fetch_consulting_detail(cid)
        if not detail.empty and detail["negative"].iloc[0] > 0.6:
            neg_texts.append({
                "cid": cid,
                "client_name": detail["client_name"].iloc[0],
                "negative": detail["negative"].iloc[0]
            })
    except:
        continue

if not neg_texts:
    st.info("부정도가 높은 상담이 없습니다.")
else:
    # ✅ 헤더
    header_cols = st.columns([3, 2, 2, 2])
    headers = ["상담ID", "고객명", "부정도", "상세보기"]
    for col, title in zip(header_cols, headers):
        col.markdown(f"**{title}**")

    # ✅ 내용 행
    for i, item in enumerate(neg_texts):
        row_cols = st.columns([3, 2, 2, 2])
        row_cols[0].markdown(f"`{item['cid']}`")
        row_cols[1].markdown(f"**{item['client_name']}**")
        row_cols[2].markdown(f"{item['negative']:.2f}")
        if row_cols[3].button("➡ 결과 상세보기", key=f"btn_neg_detail_{item['cid']}_{i}"):
            st.session_state["consulting_id"] = item["cid"]
            st.switch_page("pages/3_consulting_detail.py")

        st.markdown("---")

# 상담 추이 그래프
st.subheader("📈 날짜별 상담 추이 그래프")
daily = get_daily_trend()
fig = px.line(daily, x="date", y="total", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 카테고리 
st.subheader("🏆 카테고리 TOP 5")
top_cat = get_top_categories(df_yesterday)
if top_cat.empty or top_cat.shape[0] == 0:
    st.info("카테고리 정보가 없습니다.")
else:
    top_cat = top_cat.rename(columns={"개수": "건수"})
    top_cat["순위"] = range(1, len(top_cat) + 1)    
    top_cat = top_cat[["순위", "카테고리", "건수"]]
    st.dataframe(top_cat.reset_index(drop=True), use_container_width=True, hide_index=True)

st.markdown("---")

# 키워드
st.subheader("🔑 키워드 TOP 5")
top_kw = get_top_keywords(df_yesterday["consulting_id"])
if top_kw.empty or top_kw.shape[0] == 0:
    st.info("키워드 데이터가 없습니다.")
else:
    top_kw = top_kw.rename(columns={"개수": "건수"})
    top_kw["순위"] = range(1, len(top_kw) + 1)
    top_kw = top_kw[["순위", "키워드", "건수"]]
    st.dataframe(top_kw.reset_index(drop=True), use_container_width=True, hide_index=True)

st.markdown("---")

# ✅ 푸터
st.markdown("""
<hr style='margin-top:2rem;margin-bottom:1rem;'>
<p style='text-align:center;color:gray;'>© 2025 VOC - 고객 인사이트를 향한 첫걸음</p>
""", unsafe_allow_html=True)