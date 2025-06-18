# pages/4_client.py
import streamlit as st
import pandas as pd
from db_utils import fetch_client_by_name, fetch_client_by_id

st.set_page_config(page_title="고객 조회 페이지", layout="wide")
st.title("📇 고객 정보 조회")
st.markdown("---")

search_mode = st.radio("검색 기준을 선택하세요", ["고객 성명", "고객 ID"], horizontal=True)
query = st.text_input("고객 {}을 입력하세요".format("성명" if search_mode == "고객 성명" else "ID"))

if not query:
    st.info("고객 {}을 입력해주세요.".format("성명" if search_mode == "고객 성명" else "ID"))
    st.stop()

# 🔍 성명 조회
if search_mode == "고객 성명":
    data = fetch_client_by_name(query)
    if not data:
        st.warning("검색 결과가 없습니다.")
    else:
        st.markdown("### 👤 고객 성명 조회 결과")
        df = pd.DataFrame(data)
        df = df.rename(columns={
            "client_name": "성명",
            "client_id": "ID",
            "gender": "성별",
            "age": "연령",
            "signup_datetime": "가입일자",
            "latest_consulting_datetime": "최근문의일시",
            "is_terminated": "해지여부"
        })
        df["가입일자"] = pd.to_datetime(df["가입일자"]).dt.strftime("%Y-%m-%d")
        df["최근문의일시"] = pd.to_datetime(df["최근문의일시"]).dt.strftime("%Y-%m-%d")
        df["해지여부"] = df["해지여부"].map({True: "해지", False: "유지"})
        st.dataframe(df, use_container_width=True)

# 🔍 ID 조회
else:
    data = fetch_client_by_id(query)
    if not data:
        st.warning("조회된 고객 정보가 없습니다.")
    else:
        st.markdown("### 🧾 고객 기본 정보")
        st.markdown(f"- 고객 성명: **{data['client_name']}**")
        st.markdown(f"- 고객 ID: `{data['client_id']}`")
        st.markdown(f"- 성별: {data.get('gender', '-')}")
        st.markdown(f"- 연령대: {data.get('age', '-')}")
        st.markdown(f"- 가입일자: {pd.to_datetime(data['signup_datetime']).strftime('%Y-%m-%d')}")
        st.markdown(f"- 해지 여부: **{'해지' if data['is_terminated'] else '유지'}**")

        # 최근 문의
        st.markdown("### 🕓 고객 최근 문의 내역")
        consultings = data.get("consultings", [])
        if not consultings:
            st.info("문의 내역이 없습니다.")
        else:
            df = pd.DataFrame(consultings)
            df["consulting_datetime"] = pd.to_datetime(df["consulting_datetime"]).dt.strftime("%Y-%m-%d %H:%M")
            for _, row in df.iterrows():
                cols = st.columns([3, 3, 2])
                cols[0].markdown(f"📁 {row['category_name']}")
                cols[1].markdown(f"🗓 {row['consulting_datetime']}")
                if cols[2].button("➡ 상세보기", key=row["consulting_id"]):
                    st.session_state["consulting_id"] = row["consulting_id"]
                    st.switch_page("pages/3_consulting_detail.py")
