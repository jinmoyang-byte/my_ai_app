import streamlit as st
from google import genai
from google.genai import types

# -----------------------------------------------------------------
# 1️⃣ [Secrets 보안] Google Gemini API 클라이언트 생성
# -----------------------------------------------------------------
# Streamlit Secrets에서 GEMINI_API_KEY를 안전하게 불러옵니다.
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# -----------------------------------------------------------------
# 2️⃣ [Header Zone] 메인 제목 및 설명
# -----------------------------------------------------------------
st.title("🍕 시험 기간 맞춤 큐레이터 '야식요정 AI'")
st.caption("※ Google Gemini AI가 당신의 기분과 고민에 맞춰 딱 맞는 야식을 추천합니다.")

# -----------------------------------------------------------------
# 3️⃣ [Left Sidebar] 좌측 사이드바: 내 정보 및 기분 선택
# -----------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 내 정보 설정")
    user_name = st.text_input("사용자 이름:", placeholder="예: 김인공")
    mood = st.selectbox(
        "오늘의 기분 상태를 선택하세요:", 
        ["😊 행복함", "😭 우울함", "🤯 스트레스 받음", "🥱 피곤함"]
    )

# -----------------------------------------------------------------
# 4️⃣ [Main Input Zone] 메인 화면: 고민 작성
# -----------------------------------------------------------------
st.subheader("📝 현재 고민이나 상황을 들려주세요")
user_story = st.text_area(
    "어떤 상황인가요? 자유롭게 적어주세요:", 
    placeholder="예: 내일 수학 시험인데 잠 깨는 매콤한 게 당겨!"
)

# -----------------------------------------------------------------
# 5️⃣ [Action & Output Zone] Gemini API 호출 및 2단 결과 출력
# -----------------------------------------------------------------
if st.button("✨ AI 맞춤 추천받기"):
    if user_story:
        # AI 로딩 모래시계 (st.spinner)
        display_name = user_name if user_name else '학생'
        with st.spinner(f"Gemini AI가 {display_name}님의 고민을 분석하고 있습니다... 🤖"):
            
            # System Prompt (페르소나 지정) + User 입력값 조합
            prompt_content = f"""
            당신은 고등학교 2학년 학생의 마음을 잘 이해하는 친절한 야식 큐레이터 '야식요정 AI'입니다.
            
            사용자 이름: {display_name}
            오늘의 기분: {mood}
            현재 고민/상황: {user_story}
            
            위 정보를 바탕으로 다음 2가지를 작성해 주세요. 
            반드시 제공된 JSON 스키마 구조에 맞춰 응답해야 합니다.
            1. food_recommendation: 맞춤 추천 야식 메뉴 1개와 그 이유
            2. health_tip: 칼로리 조절 또는 건강을 위한 섭취 꿀팁 1가지와 따뜻한 응원 메시지
            """
            
            # 구조화된 출력을 위해 JSON Pydantic 모델 정의 대신 구조 정의 (Gemini 2.0/1.5 방식)
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt_content,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema={
                        "type": "OBJECT",
                        "properties": {
                            "food_recommendation": {"type": "STRING"},
                            "health_tip": {"type": "STRING"}
                        },
                        "required": ["food_recommendation", "health_tip"]
                    }
                )
            )
            
            # JSON 결과 파싱
            import json
            try:
                result = json.loads(response.text)
                food_res = result.get("food_recommendation", "추천 메뉴를 가져오지 못했습니다.")
                tip_res = result.get("health_tip", "꿀팁을 가져오지 못했습니다.")
            except Exception as e:
                food_res = response.text
                tip_res = "결과 파싱 중 오류가 발생했습니다."

        # 2단 칼럼 레이아웃으로 결과 분할 출력 (st.columns)
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("🎉 Gemini AI 추천 야식")
            st.write(food_res)
            
        with col2:
            st.info("💡 섭취 꿀팁 & 응원 메시지")
            st.write(tip_res)
            
    else:
        st.warning("⚠️ 고민 내용을 먼저 작성해 주세요!")

