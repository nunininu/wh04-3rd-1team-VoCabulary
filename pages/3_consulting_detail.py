# pages/3_consulting_detail.py
import streamlit as st
import pandas as pd
from db_utils import fetch_consulting_detail, load_analysis_result


st.set_page_config(page_title="상담 상세 페이지", layout="wide")
st.title("📋 문의 내역 상세 보기")

# ✅ 세션 상태로부터 consulting_id 받기
consulting_id = st.session_state.get("consulting_id")

if not consulting_id:
    st.error("❗ 상담 ID가 제공되지 않았습니다. 목록에서 상세보기를 통해 접근하세요.")
    st.stop()

# ✅ 데이터 로딩
df = fetch_consulting_detail(consulting_id)

if df.empty:
    st.warning("해당 상담 정보를 불러오지 못했습니다.")
    st.stop()

data = df.iloc[0]

st.markdown("---")

# ✅ 문의 기본 정보 출력
st.markdown("### 🧾 문의 기본 정보")
st.markdown(f"- 고객 성명: **{data['client_name']}**")
st.markdown(f"- 고객 ID: `{data['client_id']}`")
st.markdown(f"- 카테고리: **{data['category_name']}**")
st.markdown(f"- 문의일시: {pd.to_datetime(data['consulting_datetime']).strftime('%Y-%m-%d %H:%M')}")

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

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for line in (data["content"] or "").split("\n"):
    if line.startswith("상담사:"):
        content = line.replace("상담사:", "").replace("<", "**").replace(">", "**").strip()
        st.markdown(f'<div class="chat-right">🎧 {content}</div>', unsafe_allow_html=True)
    elif line.startswith("고객:"):
        content = line.replace("고객:", "").replace("<", "**").replace(">", "**").strip()
        st.markdown(f'<div class="chat-left">🙋‍♀️ {content}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


analysis = load_analysis_result(consulting_id)

st.markdown("---")

# ✅ 키워드 별도 표시
st.markdown("### 🔑 주요 키워드")
if analysis is not None and pd.notna(analysis["keywords"]):
    st.code(analysis["keywords"], language="plaintext")
else:
    st.warning("키워드 정보가 없습니다.")

st.markdown("---")

# ✅ 감정 분석 별도 표시
st.markdown("### 😐 감정 분석 결과")
if analysis is not None and pd.notna(analysis["positive"]) and pd.notna(analysis["negative"]):
    pos = analysis["positive"]
    neg = analysis["negative"]
    if pos > 0.1:
        st.success(f"긍정적 응답 ({pos:.2f})")
    elif neg > 0.1:
        st.error(f"부정적 응답 ({neg:.2f})")
else:
    st.warning("감정 분석 결과가 없습니다.")