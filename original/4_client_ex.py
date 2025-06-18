# pages/client_ex.py
import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

st.set_page_config(page_title="고객 조회 페이지", layout="wide")
st.title("📇 고객 정보 조회")

# 입력 모드 선택 (이름 또는 ID)
search_mode = st.radio("검색 기준을 선택하세요", ["고객 성명", "고객 ID"], horizontal=True)

query = st.text_input("고객 {}을(를) 입력하세요".format("성명" if search_mode == "고객 성명" else "ID"))

if not query:
    st.info("고객 {}을 입력해주세요.".format("성명" if search_mode == "고객 성명" else "ID"))
    st.stop()

# 고객 성명으로 조회
if search_mode == "고객 성명":
    try:
        response = requests.get(f"{API_BASE_URL}/client", params={"client_name": query})
        if response.status_code == 200:
            data = response.json()
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
                    "is_terminated": "해지/유지 여부"
                })
                df["가입일자"] = pd.to_datetime(df["가입일자"]).dt.strftime("%Y-%m-%d")
                df["최근문의일시"] = pd.to_datetime(df["최근문의일시"]).dt.strftime("%Y-%m-%d")
                df["해지/유지 여부"] = df["해지/유지 여부"].map({True: "해지", False: "유지"})
                st.dataframe(df)
        else:
            st.error(f"API 요청 실패: 상태 코드 {response.status_code}")
    except Exception as e:
        st.error(f"API 호출 중 오류 발생: {e}")

# 고객 ID로 조회
elif search_mode == "고객 ID":
    category_filter = st.selectbox("카테고리 선택", ["전체", "요금 안내", "요금 납부", "부가서비스 안내", "해지 요청", "개통/장애 문의"])
    date_range = st.date_input("조회 기간", [], format="YYYY-MM-DD")

    try:
        response = requests.get(f"{API_BASE_URL}/client/{query}")
        if response.status_code == 200:
            data = response.json()
            if not data:
                st.warning("조회된 고객 정보가 없습니다.")
            else:
                st.markdown("### 🧾 문의 기본 정보")
                st.markdown(f"- 고객 성명: **{data['client_name']}**")
                st.markdown(f"- 고객 ID: `{data['client_id']}`")
                st.markdown(f"- 가입 일자: {pd.to_datetime(data['signup_datetime']).strftime('%Y-%m-%d')}")
                st.markdown(f"- 해지 여부: {'해지' if data['is_terminated'] else '유지'}")

                st.markdown("### 🕓 고객 최근 문의 내역")
                consultings = data.get("consultings", [])
                df = pd.DataFrame(consultings)

                if df.empty:
                    st.info("문의 내역이 없습니다.")
                else:
                    df["consulting_datetime"] = pd.to_datetime(df["consulting_datetime"])

                    # 필터 적용
                    if category_filter != "전체":
                        df = df[df["category_name"] == category_filter]
                    if len(date_range) == 2:
                        start, end = date_range
                        df = df[(df["consulting_datetime"] >= pd.to_datetime(start)) & (df["consulting_datetime"] <= pd.to_datetime(end))]

                    df = df.sort_values("consulting_datetime", ascending=False).head()
                    df["consulting_datetime"] = df["consulting_datetime"].dt.strftime("%Y-%m-%d %H:%M")

                    for _, row in df.iterrows():
                        cols = st.columns([3, 3, 2])
                        cols[0].markdown(row["category_name"])
                        cols[1].markdown(row["consulting_datetime"])
                        if cols[2].button("➡ 결과 상세보기", key=row["consulting_id"]):
                            st.session_state["consulting_id"] = row["consulting_id"]
                            st.switch_page("pages/2_consulting_detail.py")
        else:
            st.error(f"API 요청 실패: 상태 코드 {response.status_code}")
    except Exception as e:
        st.error(f"API 호출 중 오류 발생: {e}")
