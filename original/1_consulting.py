import streamlit as st
import pandas as pd
from db_utils import fetch_recent_consulting

st.set_page_config(page_title="상담 입력 페이지", layout="wide")

# 세션 초기화
if "page_num" not in st.session_state:
    st.session_state["page_num"] = 0

st.title("📋 문의 내역 조회")

name = st.text_input("상담ID를 입력하세요")

if st.button("➡ 결과 페이지로 이동", key="go_detail_btn"):
    st.session_state["consulting_id"] = name
    st.switch_page("pages/2_consulting_detail.py")  # ✅ 파일 이름 기준

st.title("🕵🏻 최근 문의 목록")

# 데이터 로드 (페이지 넘버 전달)
df = fetch_recent_consulting(st.session_state["page_num"])

# 데이터가 비어있을 경우 예외 처리
if df.empty:
    st.warning("최근 상담 데이터가 없습니다. API 연결 상태 또는 데이터 확인이 필요합니다.")
else:
    # 테이블 헤더 출력
    header_cols = st.columns([2, 2, 3, 3, 2])
    headers = ["고객ID", "고객명", "상담일시", "카테고리", "상세보기"]
    for col, title in zip(header_cols, headers):
        col.markdown(f"**{title}**")

    # 테이블 데이터 출력
    for i, row in df.iterrows():
        row_cols = st.columns([2, 2, 3, 3, 2])
        row_cols[0].markdown(f"{row['client_id']}")
        row_cols[1].markdown(f"{row['client_name']}")
        row_cols[2].markdown(f"{pd.to_datetime(row['consulting_datetime']).strftime('%Y-%m-%d %H:%M')}")
        row_cols[3].markdown(f"{row['category_name']}")
        if row_cols[4].button("➡ 결과 상세보기", key=f"btn_detail_{row['consulting_id']}_{i}"):
            st.session_state["consulting_id"] = row["consulting_id"]
            st.switch_page("pages/2_consulting_detail.py")

    # 페이지 정보 출력
    st.caption(f"페이지: {st.session_state.page_num + 1}")

    # 페이지네이션 하단 컨트롤
    PAGE_SIZE = 20
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

