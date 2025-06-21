# ☎️ 고객 상담 이력 자동 분석 서비스, VoCabulary
> **LG U+ Why Not SW Camp4 4기 3차(최종) 프로젝트**
>
> 고객과의 상담 데이터를 자동으로 수집 및 처리하여 시각화하는 서비스
---
**Child Git Repo URL**
- [상담 키워드 및 감정 분석 서버](https://github.com/nunininu/VoC-local)
- [API 서버](https://github.com/nunininu/VoC-instance1)
- [데이터 ETL 서버](https://github.com/nunininu/VoC-instance2)
- [대시보드 시각화](https://github.com/nunininu/VoC-instance3)

<br>


# 👋 팀원 소개
|[권오준](https://github.com/vhzkclq0705)|[전희진](https://github.com/heejin131)|[조성근](https://github.com/nunininu)|[배형균](https://github.com/lucas-hub12)|
|---|---|---|---|
|<img src="https://avatars.githubusercontent.com/u/75382687?v=4" width="100">|<img src="https://avatars.githubusercontent.com/u/194044481?v=4" width="100">|<img src="https://avatars.githubusercontent.com/u/192968662?v=4" width="100">|<img src="https://avatars.githubusercontent.com/u/194044625?v=4" width="100">|
|테크 리더|프로젝트 리더|형상 관리자|애자일 코치|
|백엔드<br>인프라 설계 및 구축<br>데이터 파이프라인|데이터 분석<br>데이터 수집 및 가공<br>NLP 서버|대시보드<br>데이터 분석 및 시각화<br>Github 관리|시각화<br>UI/UX 설계<br>스크럼 및 미팅 관리|

<br>

## 🛠 기술 스택
### Infra
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=&logo=amazon-aws&logoColor=white) ![Amazon EC2](https://img.shields.io/badge/Amazon_EC2-%23FF9900.svg?style=&logo=amazon-aws&logoColor=white) ![Amazon S3](https://img.shields.io/badge/Amazon%20S3-009900?style=&logo=amazons3&logoColor=white) ![Amazon RDS](https://img.shields.io/badge/Amazon_RDS-7D4698?style=&logo=aws&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=&logo=docker&logoColor=white)

### Data ETL
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=&logo=Apache%20Airflow&logoColor=white) ![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=&logo=apachekafka) ![Apache Spark](https://img.shields.io/badge/Apache%20Spark-FDEE21?style=&logo=apachespark&logoColor=black)

### LLM & ML
![Exaone](https://img.shields.io/badge/Exaone-CE3DF3?style=&logo=exaone&logoColor=white) ![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFFFFF?style=&logo=huggingface&logoColor=yellow)

### Backend
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=&logo=fastapi)

### Visualization
![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=&logo=streamlit&logoColor=white) ![Superset](https://img.shields.io/badge/Superset-375BD2?style=&logo=Superset&logoColor=white)


<br>

## 📚 위키
[VoCabulary Wiki](https://github.com/nunininu/wh04-3rd-1team-VoCabulary/wiki)

<br>

## 📄 문서
<details>
<summary>프로젝트 계획서</summary>
<div markdown="1">

### 📢 프로젝트 개요
- 프로젝트명: 고객 상담 이력 자동 분석 서비스
    - 고객과의 상담 데이터를 수집 및 처리하여 시각화하는 자동화 시스템
    - 수집된 자료를 분석하여 개선점 등 인사이트 도출
 
### ✔ 목표
- 다양한 상담 데이터를 자동으로 수집·정제하고, 고객의 불만 여부 및 핵심 키워드를 분석하는 시스템을 구축한다.
- 로그 데이터와 분석 결과는 한눈에 파악할 수 있도록 직관적인 대시보드로 시각화한다.

### 🙏 기대효과
- 고객의 요구를 더 정확히 이해하고, 내부 운영 및 서비스 품질 개선을 위한 의사결정을 데이터 기반으로 수행할 수 있다.

### 🚩 MVP - 최소 기능 제품
- 다음 세 가지 핵심 기능을 중심으로 최소 기능 제품을 정의

**1. 데이터 수집 및 정제 자동화**
- 상담 데이터를 수집 → 처리 → 저장의 자동화 파이프라인 구축
  - Kafka 기반 실시간 데이터 수집
  - Airflow 기반 주기적 데이터 수집

**2. 상담 내용 분석 기능**
- KeyBERT, ELECTRA 등 텍스트 분석 모델 기반으로 대화 내용을 카테고리화 및 불만 표현 탐지  

**3. 분석 결과 시각화 대시보드** 
- Superset 으로 웹 브라우저에서 접근 가능한 대시보드 제공
- Streamlit 으로 고객 정보 및 상담 정보, 분석 결과, 일일 리포트 등 확인  
- 상담 건수, 주요 키워드, 불만 상담 비율 등을 직관적으로 시각화

### 🛠 사용 기술

**인프라(AWS)**
- S3: 상담 원본 데이터 및 분석 결과, 집계 결과 저장소
- EC2 + Docker: Airflow, Spark, Kafka, API 서버, 시각화 툴 구동
- RDS: 고객, 상담, 분석 등의 데이터 저장소
- IAM / Security Group: 접근 제어 및 인바운드 관리

**데이터 ETL**
- 수집: REST API, Kafka, 수동 업로드 등으로 상담 데이터 수집
- Airflow: 데이터 수집 → 처리 → 저장 흐름 자동화
- Spark: 대량 로그를 병렬로 전처리 및 집계 

**분석 기능** 
- 키워드 추출: TF-IDF, KeyBERT 등 활용
- 불만 탐지: ELECTRA 를 활용하여 불만 문의 탐지

**시각화** 
- Superset: 분석 결과를 웹 대시보드로 제공
- Streamlit: 고객, 상담 정보, 일일 리포트 제공 및 유저 상호작용

</div>
</details>

<br>

<details>
<summary>요구사항 정의서</summary>
<div markdown="2">

### ✅ 사용자 요구사항

1. **상담 로그 자동 수집**  
   - 채팅, 전화 등 다양한 채널에서 상담 로그 수집  
   - Kafka 기반 실시간 데이터 수집  
   - Airflow 기반 주기적 데이터 수집   

2. **로그 정제 및 저장**  
   - 수집된 로그 데이터를 분석에 적합하도록 전처리 
   - RDS 및 S3에 저장

3. **주제 분류**  
   - 상담 내용을 자동으로 카테고리 분류 (예: 결제, 환불, 불만 등)  

4. **감정 분석**  
   - 고객 발화에서 긍정/부정 감정을 분류  
   - XLM-RoBERTa, TextBlob 등 활용  

5. **키워드 추출**  
   - 핵심 단어 추출 및 시각화  
   - KeyBERT, Okt 형태소 분석 기반  

6. **분석 결과 대시보드 시각화**  
   - 상담 건수, 감정 비율, 키워드 등 시각화  
   - Tableau 또는 Superset 기반  

### 🛡️ 관리자 요구사항

1. **수집 주기 설정 기능**  
   - Airflow UI를 통해 주기 조정 가능

2. **분석 모듈 모니터링**  
   - 수집/전처리/분석 파이프라인 상태 확인  
   - Spark UI, Airflow UI 활용

3. **사용자 접근 제어**  
   - IAM, Security Group 기반의 사용자 권한 설정

4. **로그 이력 관리**  
   - 로그 수집 및 분석 기록 관리 및 검색 


</div>
</details>

<br>

<details>
<summary>WBS</summary>
<div markdown="3">


</div>
</details>

<br>

<details>
<summary>모델 정의서</summary>
<div markdown="4">



</div>
</details>

<br>

<details>
<summary>성능 평가 결과서</summary>
<div markdown="5">


</div>
</details>


<br>

<details>
<summary>최종 보고서</summary>
<div markdown="5">


</div>
</details>

---
