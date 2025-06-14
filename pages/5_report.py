# ✅ report.py

import streamlit as st
from db_utils import (
    fetch_report_data,
    fetch_consultings_by_range,
    get_top_negative_reasons
)
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="일일 리포트", layout="wide")
st.title("📊 VOC 일일 리포트")

# ✅ 현재 시간 기준 설명 표시
now = datetime.now()
time_str = now.strftime("%H:%M")
today = now.date()
yesterday = today - timedelta(days=1)
day_before_yesterday = today - timedelta(days=2)

st.info(f"""
ℹ️ 기준 시간: **{now.strftime('%Y-%m-%d %H:%M:%S')} 기준**

- 오늘: **{yesterday.strftime('%Y-%m-%d')} {time_str}** 부터 **{now.strftime('%Y-%m-%d %H:%M')}** 까지  
- 어제: **{day_before_yesterday.strftime('%Y-%m-%d')} {time_str}** 부터 **{yesterday.strftime('%Y-%m-%d')} {time_str}** 까지
""")

# ✅ /report API 데이터 호출
report = fetch_report_data()

# ✅ 문의 수 요약
cnt_y = report.get("consulting_cnt", {}).get("consulting_cnt_yesterday", 0)
cnt_t = report.get("consulting_cnt", {}).get("consulting_cnt_today", 0)
diff = cnt_t - cnt_y

st.subheader("📌 문의 수 요약")
col1, col2 = st.columns(2)
col1.metric("어제", f"{cnt_y}건")
col2.metric("오늘", f"{cnt_t}건", delta=f"{diff:+}건")
st.markdown("---")

# ✅ 불만 응답 건수
neg_y = report.get("negative_cnt", {}).get("negative_cnt_yesterday", 0)
neg_t = report.get("negative_cnt", {}).get("negative_cnt_today", 0)
diff_n = neg_t - neg_y

st.subheader("😡 불만 응답 건수")
col1, col2 = st.columns(2)
col1.metric("어제", f"{neg_y}건")
col2.metric("오늘", f"{neg_t}건", delta=f"{diff_n:+}건")
st.markdown("---")

# ✅ 상담 데이터 전체 조회 (2일치)
all_data = fetch_consultings_by_range(day_before_yesterday, today)
df_today = all_data[all_data["consulting_datetime"].dt.date == today]
df_yesterday = all_data[all_data["consulting_datetime"].dt.date == yesterday]

# ✅ 불만 키워드 TOP 3
st.subheader("🧨 불만 사유 TOP 3")
if not df_yesterday.empty:
    reasons = get_top_negative_reasons(df_yesterday["consulting_id"])
    if reasons.empty:
        st.info("불만 사유 데이터가 없습니다.")
    else:
        st.dataframe(reasons, use_container_width=True, hide_index=True)
else:
    st.info("어제 상담 데이터가 없습니다.")
st.markdown("---")

# ✅ 연령대별 불만 응답 요약
# ✅ 현재 시각 기준 설정
now = datetime.now()
time_str = now.strftime('%H:%M')
today = now.date()
yesterday = today - timedelta(days=1)

# ✅ 오늘 분석 범위: 어제 같은 시각 ~ 지금
start_time = datetime.combine(yesterday, now.time())
end_time = now

# ✅ 연령대별 불만 응답 분석

st.markdown("---")

# ✅ 카테고리 TOP 5
st.subheader("🏆 카테고리 TOP 5")
cat_data = report.get("top_categories", [])
if not cat_data:
    st.info("카테고리 정보가 없습니다.")
else:
    df = pd.DataFrame(cat_data)
    df = df.rename(columns={"category_name": "카테고리", "cnt": "건수"})
    df["순위"] = range(1, len(df) + 1)
    df = df[["순위", "카테고리", "건수"]]
    st.dataframe(df, use_container_width=True, hide_index=True)
st.markdown("---")

# ✅ 키워드 TOP 5
st.subheader("🔑 키워드 TOP 5")
kw_data = report.get("top_keywords", [])
if not kw_data:
    st.info("키워드 정보가 없습니다.")
else:
    df = pd.DataFrame(kw_data)
    df = df.rename(columns={"keyword": "키워드", "cnt": "건수"})
    df["순위"] = range(1, len(df) + 1)
    df = df[["순위", "키워드", "건수"]]
    st.dataframe(df, use_container_width=True, hide_index=True)
st.markdown("---")

# ✅ 푸터
st.markdown("""
<hr style='margin-top:2rem;margin-bottom:1rem;'>
<p style='text-align:center;color:gray;'>© 2025 VOC - 고객 인사이트를 향한 첫걸음</p>
""", unsafe_allow_html=True)



