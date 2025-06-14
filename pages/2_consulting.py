# pages/2_consulting.py
import streamlit as st
import pandas as pd
from db_utils import fetch_recent_consulting, fetch_filtered_consultings

st.set_page_config(page_title="📋 상담 내역 조회", layout="wide")

if "page_num" not in st.session_state:
    st.session_state["page_num"] = 0
if "filter_clicked" not in st.session_state:
    st.session_state["filter_clicked"] = False

st.title("📋 문의 내역 조회")

tab1, tab2 = st.tabs(["ID 조회", "세부 조회"])

# 🔹 탭 1: ID 입력 조회
with tab1:
    st.subheader("🧾 상담 ID로 조회")
    consulting_id = st.text_input("상담 ID를 입력하세요")

    if st.button("➡ 결과 페이지로 이동", key="go_detail_btn"):
        st.session_state["consulting_id"] = consulting_id
        st.switch_page("pages/3_consulting_detail.py")

# 🔹 탭 2: 조건 조회
with tab2:
    st.subheader("📆 기간 및 카테고리 조회")

    start_date = st.date_input("시작일자", pd.to_datetime("today") - pd.Timedelta(days=30))
    end_date = st.date_input("종료일자", pd.to_datetime("today"))

    # 카테고리 로드
    _, category_df = fetch_recent_consulting()
    category_df = category_df.sort_values("category_id")
    category_options = category_df["category_name"].tolist()
    selected_category = st.selectbox("카테고리 선택", category_options)

    category_id = int(category_df[category_df["category_name"] == selected_category]["category_id"].values[0])

    if st.button("🔍 조회하기", key="filter_btn"):
        st.session_state["page_num"] = 0
        st.session_state["filter_clicked"] = True
        st.rerun()

    if st.session_state["filter_clicked"]:
        params = {
            "page": st.session_state["page_num"] + 1,
            "limit": 20,
            "category_id": category_id,
            "start_date": start_date.strftime("%Y-%m-%d"),
            # ✅ 종료일 포함 범위 확장
            "end_date": (end_date + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        }

        consultings, error = fetch_filtered_consultings(params)
        if error:
            st.error(error)
        elif consultings.empty:
            st.info("조건에 맞는 상담이 없습니다.")
        else:
            st.write(f"총 {len(consultings)}건 / 페이지 {st.session_state['page_num'] + 1}")

            for i, row in consultings.iterrows():
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 3, 2])
                    col1.write(row["client_id"])
                    col2.write(row["client_name"])
                    col3.write(pd.to_datetime(row["consulting_datetime"]).strftime('%Y-%m-%d %H:%M'))
                    col4.write(row["category_name"])
                    if col5.button("➡ 상세", key=f"btn_{i}"):
                        st.session_state["consulting_id"] = row["consulting_id"]
                        st.switch_page("pages/3_consulting_detail.py")

            col_prev, _, col_next = st.columns([1, 1, 1])
            with col_prev:
                if st.session_state["page_num"] > 0:
                    if st.button("⬅ 이전", key="prev_page_btn"):
                        st.session_state["page_num"] -= 1
                        st.rerun()
            with col_next:
                if st.button("다음 ➡", key="next_page_btn"):
                    st.session_state["page_num"] += 1
                    st.rerun()
