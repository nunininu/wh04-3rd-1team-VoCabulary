# db_utils.py
import os
import pandas as pd
import requests
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime, date

load_dotenv()

API_CONSULTINGS = os.getenv("API_consultings")
API_CONSULTING = os.getenv("API_consulting")
API_CLIENT = os.getenv("API_client")

PAGE_SIZE = 20

# 🔹 상담 리스트 + 카테고리 동시 수신
def fetch_recent_consulting(page: int = 0, category_id: int = -1):
    try:
        response = requests.get(API_CONSULTINGS, params={"page": page + 1, "limit": PAGE_SIZE, "category_id": category_id})
        if response.status_code == 200:
            data = response.json()
            consultings = pd.DataFrame(data.get("consultings", []))
            category_map = data.get("category", {})
            category_df = pd.DataFrame(
                [(k, v) for k, v in category_map.items()],
                columns=["category_name", "category_id"]
            )
            category_df = category_df.sort_values("category_id").reset_index(drop=True)
            return consultings, category_df
        else:
            st.error(f"API 요청 실패: {response.status_code}")
            return pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        st.error(f"API 오류: {e}")
        return pd.DataFrame(), pd.DataFrame()

# 🔹 필터 파라미터 기반 상담 조회
def fetch_filtered_consultings(params: dict):
    try:
        response = requests.get(API_CONSULTINGS, params=params)
        if response.status_code == 200:
            consultings = pd.DataFrame(response.json().get("consultings", []))
            return consultings, None
        else:
            return pd.DataFrame(), f"API 오류: {response.status_code}"
    except Exception as e:
        return pd.DataFrame(), f"요청 실패: {e}"

# ✅ 단일 상담 ID로 조회
def fetch_consulting_by_id(consulting_id):
    try:
        url = f"{API_CONSULTING}{consulting_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame([response.json()])
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

# ✅ 전체 카테고리만 로드 (카테고리 이름 + ID)
def load_category_from_api():
    try:
        # 카테고리만 가져오기 위해 limit=1 요청
        response = requests.get(API_CONSULTINGS, params={"page": 1, "limit": 1})
        if response.status_code == 200:
            data = response.json()
            category_map = data.get("category", {})
            category_df = pd.DataFrame(
                [(k, v) for k, v in category_map.items()],
                columns=["category_name", "category_id"]
            )
            return category_df.sort_values("category_id")
        else:
            st.error(f"카테고리 API 실패: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"카테고리 로드 중 오류 발생: {e}")
        return pd.DataFrame()

# ✅ 날짜 + 카테고리 필터링 (단순 필터)
def filter_consultings(start_date, end_date, selected_category):
    try:
        response = requests.get(API_CONSULTINGS, params={"limit": 1000})
        if response.status_code == 200:
            df = pd.DataFrame(response.json().get("consultings", []))
            df["consulting_datetime"] = pd.to_datetime(df["consulting_datetime"])
            df = df[(df["consulting_datetime"] >= pd.to_datetime(start_date)) &
                    (df["consulting_datetime"] <= pd.to_datetime(end_date))]
            if selected_category != "전체":
                df = df[df["category_name"] == selected_category]
            return df
        else:
            st.error(f"API 요청 실패: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"데이터 필터링 실패: {e}")
        return pd.DataFrame()
    
def fetch_consulting_detail(consulting_id):
    try:
        url = f"{API_CONSULTING}{consulting_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame([response.json()])
        else:
            st.error(f"API 요청 실패: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"상세 조회 실패: {e}")
        return pd.DataFrame()
    
def load_analysis_result(consulting_id):
    try:
        url = f"{API_CONSULTING}{consulting_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "keywords": data.get("keywords", ""),
                "is_negative": data.get("is_negative", None),
                "negative_point": data.get("negative_point", None)
            }
        else:
            st.error(f"API 오류: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"API 호출 오류: {e}")
        return None
    
# ✅ 고객 성명으로 고객 목록 조회
def fetch_client_by_name(client_name: str):
    try:
        response = requests.get(API_CLIENT, params={"client_name": client_name})
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"[이름 조회] API 오류: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"[이름 조회] 요청 실패: {e}")
        return []


# ✅ 고객 ID로 단건 조회
def fetch_client_by_id(client_id: str):
    try:
        response = requests.get(f"{API_CLIENT}{client_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"[ID 조회] API 오류: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"[ID 조회] 요청 실패: {e}")
        return None

def fetch_report_data():
    try:
        response = requests.get(os.getenv("API_report"))
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"/report API 오류: {response.status_code}")
            return {}
    except Exception as e:
        st.error(f"/report API 요청 실패: {e}")
        return {}
    
# 🔎 1. 불만 사유 Top3
def get_top_negative_reasons(consulting_ids):
    reasons = []
    for cid in consulting_ids:
        try:
            res = requests.get(f"{API_CONSULTING}{cid}")
            if res.status_code == 200:
                data = res.json()
                if data.get("is_negative") and data.get("keywords"):
                    for kw in data["keywords"].split(","):
                        reasons.append(kw.strip())
        except:
            continue
    if not reasons:
        return pd.DataFrame()
    
    reason_counts = pd.Series(reasons).value_counts().nlargest(3).reset_index()
    reason_counts.columns = ["불만 키워드", "건수"]
    return reason_counts
   
def fetch_consultings_by_range(start_date: date, end_date: date):
    try:
        response = requests.get(API_CONSULTINGS, params={"limit": 1000})
        if response.status_code == 200:
            df = pd.DataFrame(response.json().get("consultings", []))
            if df.empty:
                return df

            df["consulting_datetime"] = pd.to_datetime(df["consulting_datetime"])
            # ✅ UTC → KST 변환 필수
            df["consulting_datetime"] = df["consulting_datetime"].dt.tz_localize("UTC").dt.tz_convert("Asia/Seoul")
            
            # ✅ 날짜 필터 (KST 기준)
            df_filtered = df[
                (df["consulting_datetime"].dt.date >= start_date) &
                (df["consulting_datetime"].dt.date <= end_date)
            ]
            return df_filtered
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"[fetch_consultings_by_range 오류] {e}")
        return pd.DataFrame()