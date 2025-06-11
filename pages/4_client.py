# pages/client.py
import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

st.set_page_config(page_title="고객 조회 페이지", layout="wide")
st.title("📇 고객 정보 조회")

st.markdown("---")

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
    try:
        response = requests.get(f"{API_BASE_URL}/client/{query}")
        if response.status_code == 200:
            data = response.json()
            if not data:
                st.warning("조회된 고객 정보가 없습니다.")
            else:
                st.markdown("### 🧾 고객 기본 정보")
                st.markdown(f"- 고객 성명: **{data['client_name']}**")
                st.markdown(f"- 고객 ID: `{data['client_id']}`")
                st.markdown(f"- 가입 일자: {pd.to_datetime(data['signup_datetime']).strftime('%Y-%m-%d')}")
                st.markdown(f"- 해지 여부: {'해지' if data['is_terminated'] else '유지'}")

                # ✅ 긍정도, 부정도 표시 (색상 적용)
                positive = data.get('positive', None)
                negative = data.get('negative', None)

                if isinstance(positive, (int, float)):
                    st.markdown(f"- 긍정도: <span style='color:green; font-weight:bold;'>{positive:.2f}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("- 긍정도: `N/A`")

                if isinstance(negative, (int, float)):
                    st.markdown(f"- 부정도: <span style='color:red; font-weight:bold;'>{negative:.2f}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("- 부정도: `N/A`")
    
                st.markdown("### 🕓 고객 최근 문의 내역")
                if not data.get("consultings"):
                    st.info("문의 내역이 없습니다.")
                else:
                    df = pd.DataFrame(data["consultings"])
                    df["consulting_datetime"] = pd.to_datetime(df["consulting_datetime"]).dt.strftime("%Y-%m-%d %H:%M")
                    for _, row in df.iterrows():
                        cols = st.columns([3, 3, 2])
                        cols[0].markdown(row["category_name"])
                        cols[1].markdown(row["consulting_datetime"])
                        if cols[2].button("➡ 결과 상세보기", key=row["consulting_id"]):
                            st.session_state["consulting_id"] = row["consulting_id"]
                            st.switch_page("pages/3_consulting_detail.py")
        else:
            st.error(f"API 요청 실패: 상태 코드 {response.status_code}")
    except Exception as e:
        st.error(f"API 호출 중 오류 발생: {e}")