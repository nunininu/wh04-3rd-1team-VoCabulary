# db_utils.py
import os
import pandas as pd
import requests
from dotenv import load_dotenv
import streamlit as st
from collections import Counter

# .env 파일 로드
load_dotenv()

API_URL_1 = os.getenv("API_URL_1")
API_DETAIL_URL = os.getenv("API_DETAIL_URL")

PAGE_SIZE = 20

# ✅ 상담 리스트 + 카테고리 동시 수신

def fetch_recent_consulting(page: int = 0, category_id: int = -1):
    try:
        response = requests.get(
            API_URL_1, params={"page": page + 1, "limit": PAGE_SIZE, "category_id": category_id}
        )
        if response.status_code == 200:
            data = response.json()
            consultings = pd.DataFrame(data["consultings"])
            categories = data["category"]
            category_df = pd.DataFrame(
                [(v, k) for k, v in categories.items()], columns=["category_id", "category_name"]
            )
            return consultings, category_df.sort_values("category_id")
        else:
            st.error(f"API 요청 실패: 상태 코드 {response.status_code}")
            return pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        st.error(f"API 요청 중 오류 발생: {e}")
        return pd.DataFrame(), pd.DataFrame()

# ✅ 카테고리 목록 로드

def load_category_from_api():
    try:
        response = requests.get(API_URL_1, params={"page": 1, "limit": 1})
        if response.status_code == 200:
            data = response.json()
            category_map = data.get("category", {})
            return pd.DataFrame(
                [(v, k) for k, v in category_map.items()],
                columns=["category_id", "category_name"]
            ).sort_values("category_id")
        else:
            st.error(f"카테고리 API 실패: 상태 코드 {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"카테고리 로드 중 오류 발생: {e}")
        return pd.DataFrame()

# ✅ 상담 상세 정보 조회

def fetch_consulting_detail(consulting_id):
    try:
        url = f"{API_DETAIL_URL}{consulting_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame([response.json()])
        else:
            st.error(f"API 응답 오류: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"API 호출 실패: {e}")
        return pd.DataFrame()

# ✅ 상담 ID로 단건 조회

def fetch_consulting_by_id(consulting_id):
    try:
        url = f"{API_DETAIL_URL}{consulting_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return pd.DataFrame([response.json()])
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

# ✅ 조건 필터링된 상담 조회

def filter_consultings(start_date, end_date, selected_category):
    try:
        response = requests.get(f"{API_URL_1}?limit=1000")
        if response.status_code == 200:
            df = pd.DataFrame(response.json().get("consultings", []))
            df["consulting_datetime"] = pd.to_datetime(df["consulting_datetime"])

            df = df[(df["consulting_datetime"] >= pd.to_datetime(start_date)) &
                    (df["consulting_datetime"] <= pd.to_datetime(end_date))]

            if selected_category != "전체":
                df = df[df["category_name"] == selected_category]

            return df
        else:
            st.error(f"API 요청 실패: 상태 코드 {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"데이터 필터링 실패: {e}")
        return pd.DataFrame()

# ✅ 필터링 파라미터 기반 API 호출

def fetch_filtered_consultings(params: dict):
    try:
        response = requests.get(API_URL_1, params=params)
        if response.status_code == 200:
            data = response.json()
            consultings = pd.DataFrame(data["consultings"])
            return consultings, None
        else:
            return pd.DataFrame(), f"API 요청 실패: 상태 코드 {response.status_code}"
    except Exception as e:
        return pd.DataFrame(), f"API 요청 중 오류 발생: {e}"

# ✅ 전체 상담 데이터 조회

def fetch_all_consultings(limit=1000):
    try:
        response = requests.get(API_URL_1, params={"page": 1, "limit": limit, "category_id": -1})
        if response.status_code == 200:
            return pd.DataFrame(response.json().get("consultings", []))
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# ✅ 특정 날짜의 상담 데이터 필터링

def fetch_consultings_by_day(target_date):
    df = fetch_all_consultings()
    if df.empty:
        return pd.DataFrame()
    df["consulting_datetime"] = pd.to_datetime(df["consulting_datetime"])
    return df[df["consulting_datetime"].dt.date == target_date]

# ✅ 특정 날짜의 상담 데이터 필터링
def fetch_consultings_by_range(start_date, end_date):
    df = fetch_all_consultings()
    if df.empty:
        return pd.DataFrame()
    df["consulting_datetime"] = pd.to_datetime(df["consulting_datetime"])
    return df[(df["consulting_datetime"].dt.date >= start_date) & 
              (df["consulting_datetime"].dt.date <= end_date)]

# ✅ 부정 응답률 계산

def calculate_negative_stats(consulting_ids):
    total = len(consulting_ids)
    count = 0
    for cid in consulting_ids:
        try:
            detail = requests.get(f"{API_DETAIL_URL}{cid}")
            if detail.status_code == 200:
                neg = detail.json().get("negative", 0)
                if neg > 0.6:
                    count += 1
        except:
            continue
    rate = (count / total * 100) if total else 0
    return count, f"{rate:.1f}%"

# ✅ 카테고리 TOP 5

def get_top_categories(df):
    if "category_name" not in df.columns:
        return pd.DataFrame()
    top = df["category_name"].value_counts().head(5).reset_index()
    top.columns = ["카테고리", "개수"]
    top.insert(0, "순위", range(1, len(top)+1))
    return top

# ✅ 키워드 TOP 5

def get_top_keywords(consulting_ids):
    counter = Counter()
    for cid in consulting_ids:
        try:
            res = requests.get(f"{API_DETAIL_URL}{cid}")
            if res.status_code == 200:
                keywords = res.json().get("keywords", "")
                if keywords:
                    for k in keywords.split(","):
                        counter[k.strip()] += 1
        except:
            continue
    top = counter.most_common(5)
    if not top:
        return pd.DataFrame({"순위": [], "키워드": ["키워드가 없습니다"], "개수": [""]})
    return pd.DataFrame({
        "순위": range(1, len(top)+1),
        "키워드": [k for k, _ in top],
        "개수": [v for _, v in top]
    })

# ✅ 일별 상담 건수 추이

def get_daily_trend():
    try:
        result = requests.get(f"{API_URL_1}?limit=1000")
        if result.status_code == 200:
            data = result.json().get("consultings", [])
            df = pd.DataFrame(data)
            df["consulting_datetime"] = pd.to_datetime(df["consulting_datetime"])
            df["date"] = df["consulting_datetime"].dt.date
            daily = df.groupby("date").size().reset_index(name="total")
            return daily
        else:
            st.error(f"API 요청 실패: 상태 코드 {result.status_code}")
            return pd.DataFrame(columns=["date", "total"])
    except Exception as e:
        st.error(f"일별 추이 데이터를 가져오는 중 오류 발생: {e}")
        return pd.DataFrame(columns=["date", "total"])

    # ✅ 분석 결과 로드 (API 기반)
def load_analysis_result(consulting_id):
    try:
        url = f"{API_DETAIL_URL}{consulting_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "keywords": data.get("keywords", ""),
                "positive": data.get("positive", None),
                "negative": data.get("negative", None)
            }
        else:
            st.error(f"분석 결과 API 응답 오류: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"분석 결과 API 호출 실패: {e}")
        return None