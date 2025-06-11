# pages/2_consulting.py
import streamlit as st
import pandas as pd
import requests
from db_utils import fetch_recent_consulting, fetch_filtered_consultings

st.set_page_config(page_title="상담 입력 페이지", layout="wide")

# 세션 초기화
if "page_num" not in st.session_state:
    st.session_state["page_num"] = 0
if "filter_clicked" not in st.session_state:
    st.session_state["filter_clicked"] = False

st.title("📋 문의 내역 조회")

tab1, tab2 = st.tabs(["ID 조회", "세부 조회"])

# 🔹 탭 1: ID 조회 (최근 목록 제거됨)
with tab1:
    st.subheader("🧾 상담 ID로 조회")
    consulting_id = st.text_input("상담 ID를 입력하세요")

    if st.button("➡ 결과 페이지로 이동", key="go_detail_btn"):
        st.session_state["consulting_id"] = consulting_id
        st.switch_page("pages/3_consulting_detail.py")

# 🔹 탭 2: 세부 조회
with tab2:
    st.subheader("📆 기간 및 카테고리로 조회")

    start_date = st.date_input("시작일자", pd.to_datetime("today") - pd.Timedelta(days=30))
    end_date = st.date_input("종료일자", pd.to_datetime("today"))

    # 카테고리 목록 가져오기
    _, category_df = fetch_recent_consulting(0)
    category_options = category_df["category_name"].tolist()
    selected_category_name = st.selectbox("카테고리 선택", category_options)

    category_id = -1 if selected_category_name == "전체" else int(
        category_df[category_df["category_name"] == selected_category_name]["category_id"].values[0]
    )

    # 조회 버튼 클릭 시 상태 초기화
    if st.button("🔍 조회하기", key="filter_btn"):
        st.session_state["page_num"] = 0
        st.session_state["filter_clicked"] = True
        st.rerun()

    # 조회 버튼을 누른 후에만 결과 출력
    if st.session_state["filter_clicked"]:
        params = {
            "page": st.session_state["page_num"] + 1,
            "limit": 20,
            "category_id": category_id,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        consultings, error = fetch_filtered_consultings(params)
        if error:
            st.error(error)
        elif consultings.empty:
            st.info("해당 조건에 맞는 데이터가 없습니다.")
        else:
            header_cols = st.columns([2, 2, 3, 3, 2])
            headers = ["고객ID", "고객명", "상담일시", "카테고리", "상세보기"]
            for col, title in zip(header_cols, headers):
                col.markdown(f"**{title}**")

            for i, row in consultings.iterrows():
                row_cols = st.columns([2, 2, 3, 3, 2])
                row_cols[0].markdown(f"{row['client_id']}")
                row_cols[1].markdown(f"{row['client_name']}")
                row_cols[2].markdown(f"{pd.to_datetime(row['consulting_datetime']).strftime('%Y-%m-%d %H:%M')}")
                row_cols[3].markdown(f"{row['category_name']}")
                if row_cols[4].button("➡ 결과 상세보기", key=f"btn_filter_detail_{row['consulting_id']}_{i}"):
                    st.session_state["consulting_id"] = row["consulting_id"]
                    st.switch_page("pages/3_consulting_detail.py")

                st.markdown("---")

            st.caption(f"총 {len(consultings)}건, 페이지: {st.session_state.page_num + 1}")

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.session_state.page_num > 0:
                    if st.button("⬅ 이전 페이지", key="prev_page_btn"):
                        st.session_state.page_num -= 1
                        st.rerun()
            with col3:
                if st.button("다음 페이지 ➡", key="next_page_btn"):
                    st.session_state.page_num += 1
                    st.rerun()
