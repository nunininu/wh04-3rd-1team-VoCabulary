from kafka import KafkaConsumer
import json
from keybert import KeyBERT
from konlpy.tag import Okt

# Kafka Consumer 설정
consumer = KafkaConsumer(
    "voc-json",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="analyzer-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# 키워드 추출기 및 형태소 분석기
kw_model = KeyBERT()
okt = Okt()

# 형태소 전처리 함수 (명사 추출)
def preprocess_korean(text):
    tokens = okt.nouns(text)
    return " ".join(tokens)

print("🔍 Kafka 한국어 분석 서버 실행 중...")

for message in consumer:
    data = message.value
    text = data.get("consulting_content", "")
    category = data.get("consulting_category", "")

    if not isinstance(text, str) or not text.strip():
        print("⚠️ consulting_content 필드가 없거나 비어 있음. 스킵.")
        continue

    print("\n📩 수신된 메시지 내용:")
    print(text)

    # ✅ 키워드 추출 실행 (카테고리 포함)
    try:
        combined_text = f"{category} {text}"
        preprocessed_text = preprocess_korean(combined_text)
        keywords = kw_model.extract_keywords(preprocessed_text, top_n=5)
        keywords = [kw[0] for kw in keywords]
        print("🔑 키워드:", keywords)
    except Exception as e:
        print(f"❌ 키워드 추출 오류: {e}")
