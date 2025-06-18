import streamlit as st
import pandas as pd
from db_utils import fetch_recent_consulting, fetch_consulting_by_id, load_category_from_api, filter_consultings

st.set_page_config(page_title="VoC 고객상담 분석 서비스", layout="wide")

# ✅ 서비스 요약
st.markdown("""
<div style='text-align:center;'>
    <h1 style='color:#003366;'>🎯 VoC 고객상담 분석 서비스</h1>
    <p>고객 상담 데이터를 분석하여 운영 인사이트를 제공하는 실무 중심의 분석 도구입니다.</p>
    <p><b>📌 주요 기능:</b> 실시간 상담 내역, 고객 이력 확인, 감정 및 키워드 분석, 일일 리포트 생성 등</p>
</div>
""", unsafe_allow_html=True)

# st.markdown("""
# <h1 style='color:#003366;'>🎯 VOC 고객상담 분석 서비스</h1>
# <p>고객 상담 데이터를 분석하여 운영 인사이트를 제공하는 실무 중심의 분석 도구입니다.</p>
# <p><b>📌 주요 기능:</b> 실시간 상담 트렌드 분석, 감정 및 키워드 시각화, 고객 이력 확인, 리포트 생성 등</p>
# """, unsafe_allow_html=True)

# 세션 초기화
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# ✅ 간단한 사용자 계정 정보 (예: 하드코딩된 유저 DB)
USER_CREDENTIALS = {
    "전희진": "0000",
    "권오준": "0000",
    "조성근": "0000",
    "배형균": "0000"
}

# ✅ 로그인 UI
with st.sidebar:
    st.markdown("## 👤 로그인")

    if not st.session_state.logged_in:
        username = st.text_input("상담사 이름", key="login_input")
        password = st.text_input("비밀번호", type="password", key="password_input")
        login_button = st.button("로그인")

        if login_button:
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ 로그인 정보가 올바르지 않습니다.")
    else:
        st.success(f"🟢 {st.session_state.username} 상담사님 로그인 중입니다.")
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
# 본문 영역
if not st.session_state.logged_in:
    st.warning("🔒 로그인 후 이용 가능합니다.")
    st.stop()

st.markdown(f"""
<div style='text-align:center;'>
    <p style='color:green; font-weight:bold; font-size:1.2rem;'>✅ {st.session_state.username} 상담사님, 환영합니다!</p>
    <p>아래에서 상담 분석을 확인해보세요.</p>
</div>
""", unsafe_allow_html=True)

# st.success(f"✅ {st.session_state.username} 상담사님, 환영합니다!")
# st.write("아래에서 상담 분석을 확인해보세요.")

st.markdown("---")

# ✅ 메인 기능 소개
st.subheader("🔍 서비스 구성")

# 컬럼 3개로 분할 (기능 3개니까)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📊 VoC 일일 리포트")
    st.markdown("- 문의 수 및 부정 응답률\n- 일별 문의 수 그래프 시각화\n- 카테고리 및 키워드 TOP 5")
    if st.button("📊 일일 리포트 보기", key="report_btn"):
        st.switch_page("pages/5_report.py")

with col2:
    st.markdown("### 📋 상담 내역 조회")
    st.markdown("- 상담 ID 또는 조건별 상세 조회\n- 상담 대화 내용을 채팅 UI로 표현\n- 키워드 및 감정 분석 자동 제공")
    if st.button("📋 상담 내역 조회", key="consulting_btn"):
        st.switch_page("pages/2_consulting.py")

with col3:
    st.markdown("### 🔎 고객 정보 조회")
    st.markdown("- 고객 ID 또는 성명 기반 상담 이력 탐색\n- 가입일, 해지 여부 등 메타데이터 확인\n- 고객별 최근 문의 및 상세 분석 접근")
    if st.button("🔍 고객 조회", key="client_btn"):
        st.switch_page("pages/4_client.py")


# ✅ 푸터
st.markdown("""
<hr style='margin-top:2rem;margin-bottom:1rem;'>
<p style='text-align:center;color:gray;'>© 2025 VOC - 고객 인사이트를 향한 첫걸음</p>
""", unsafe_allow_html=True)