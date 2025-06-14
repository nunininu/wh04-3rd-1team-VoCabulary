import streamlit as st
import pandas as pd
from db_utils import fetch_consulting_detail, load_analysis_result

st.set_page_config(page_title="상담 상세 페이지", layout="wide")
st.title("📋 문의 내역 상세 보기")

# ✅ 세션에서 consulting_id 가져오기
consulting_id = st.session_state.get("consulting_id")

if not consulting_id:
    st.error("❗ 상담 ID가 제공되지 않았습니다. 목록에서 상세보기를 통해 접근하세요.")
    st.stop()

# ✅ 상담 상세 정보 로드
df = fetch_consulting_detail(consulting_id)

if df.empty:
    st.warning("해당 상담 정보를 불러오지 못했습니다.")
    st.stop()

data = df.iloc[0]

# ✅ 문의 기본 정보 출력
st.markdown("### 🧾 문의 기본 정보")
st.markdown(f"- 고객 성명: **{data.get('client_name', 'N/A')}**")
st.markdown(f"- 고객 ID: `{data.get('client_id', 'N/A')}`")
st.markdown(f"- 카테고리: **{data.get('category_name', 'N/A')}**")
st.markdown(f"- 문의일시: {pd.to_datetime(data.get('consulting_datetime')).strftime('%Y-%m-%d %H:%M')}")

st.markdown("---")

# ✅ 채팅 UI 출력
st.markdown("### 💬 상담 내용")

st.markdown("""
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}
.chat-right {
    align-self: flex-end;
    background-color: #f1f1f1;
    padding: 0.7em 1em;
    border-radius: 10px;
    max-width: 70%;
}
.chat-left {
    align-self: flex-start;
    background-color: #d4eaf7;
    padding: 0.7em 1em;
    border-radius: 10px;
    max-width: 70%;
}
</style>
""", unsafe_allow_html=True)

# ✅ content 전처리 및 분리
raw_content = data.get("content", "")
cleaned_content = raw_content.replace("\\n", "\n").replace("\\\\n", "\n").replace("\\\n", "\n")
lines = cleaned_content.splitlines()

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for line in lines:
    stripped = line.strip()
    if stripped.startswith("상담사:"):
        msg = stripped.replace("상담사:", "").strip()
        st.markdown(f'<div class="chat-right">🎧 {msg}</div>', unsafe_allow_html=True)
    elif stripped.startswith("고객:"):
        msg = stripped.replace("고객:", "").strip()
        st.markdown(f'<div class="chat-left">🙋‍♀️ {msg}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ✅ 분석 결과 API 호출
analysis = load_analysis_result(consulting_id)

# ✅ 키워드 표시
st.markdown("### 🔑 주요 키워드")
keywords = analysis.get("keywords") if analysis else None
if keywords and pd.notna(keywords):
    st.code(keywords, language="plaintext")
else:
    st.info("키워드가 없습니다.")

st.markdown("---")

# ✅ 감정 분석 결과
st.markdown("### 😐 감정 분석 결과")
if analysis:
    is_negative = analysis.get("is_negative", None)
    negative_point = analysis.get("negative_point", None)

    if is_negative is True:
        st.error("불만 있음 ❗")
        if negative_point:
            st.markdown(f"📝 불만 사유: **{negative_point}**")
    elif is_negative is False:
        st.success("불만 없음 😊")
    else:
        st.warning("감정 분석 데이터가 없습니다.")
else:
    st.warning("감정 분석 결과를 불러오지 못했습니다.")
