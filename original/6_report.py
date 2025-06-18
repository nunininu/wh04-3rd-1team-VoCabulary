# report.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="VOC 리포트 요약", layout="wide")

st.title("📋 상담 매니저용 요약 리포트")
st.markdown("""
CS 상담 매니저가 실무 현장에서 빠르게 파악할 수 있도록 다음 항목을 요약해 제공합니다:

- 오늘의 상담 지표 현황
- 상담 실패 및 위험 유형
- 고객 이슈 TOP5
- 상담사 대응 요령 및 템플릿
""")

st.markdown("---")

# ✅ 오늘의 상담 지표 요약
st.subheader("📊 오늘의 주요 상담 지표")
kpi = pd.DataFrame({
    "항목": ["총 상담 수", "처리 완료", "콜백 필요", "미처리"],
    "건수": [320, 270, 30, 20]
})
st.dataframe(kpi, use_container_width=True)

# ✅ 위험 유형 예시
st.subheader("🚨 상담 실패 및 위험 유형")
st.markdown("""
- [🔴] 불만 표출 후 이탈 (예: "끊어!", "다신 안 써!")
- [🟡] 약속 미이행 (예: "3일 뒤 연락 준다며?")
- [🟠] 반복 문의 (예: "계속 이 내용으로 전화했어요")

**⚠ 즉시 보고 및 선조치 대상입니다.**
""")

# ✅ 이슈 키워드 TOP5 (예시)
st.subheader("📌 고객 이슈 TOP 5")
issue_top = pd.DataFrame({
    "순위": [1, 2, 3, 4, 5],
    "이슈 키워드": ["해지", "요금제", "데이터", "연결 안됨", "상담사 태도"],
    "건수": [48, 42, 38, 29, 26]
})
st.dataframe(issue_top, use_container_width=True)

# ✅ 상담 대응 요령 예시
def render_template(title, content):
    with st.expander(title):
        st.markdown(content)

st.subheader("🗂 상담사 대응 요령 템플릿")
render_template("📎 해지 요청", "고객의 해지 배경을 확인하고, 혜택 안내 후 유지 유도 → 그래도 원하면 빠른 처리")
render_template("📎 요금제 불만", "실제 사용 패턴에 맞는 요금제 제안 및 데이터 리필권 등 안내")
render_template("📎 불친절 항의", "먼저 사과 후 공식 대응 안내 및 개선 약속")