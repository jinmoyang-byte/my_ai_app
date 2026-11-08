    import streamlit as st
    
    # 1. Header Zone
    st.title("🍕 시험 기간 맞춤 큐레이터 '야식요정 AI'")
    st.caption("※ 밤 10시 이후, 당신의 기분과 칼로리 상태에 따라 딱 맞는 야식을 추천합니다.")
    
    # 2. Sidebar Zone
    with st.sidebar:
        st.header("⚙️ 내 정보 설정")
        user_name = st.text_input("사용자 이름:", placeholder="예: 김인공")
        mood = st.selectbox(
            "오늘의 기분 상태를 선택하세요:",
            ["😊 행복함", "😭 우울함", "🤯 스트레스 받음", "🥱 피곤함"]
        )
    
    # 3. Main Input Zone
    st.subheader("📝 현재 고민이나 상황을 들려주세요")
    user_story = st.text_area("어떤 상황인가요? 자유롭게 적어주세요:", placeholder="예: 내일 수학 시험인데 잠 깨는 매콤한 게 당겨!")
    
    # 4. Action & Output Zone
    if st.button("✨ AI 맞춤 추천받기"):
        if user_story:
            with st.spinner(f"AI가 {user_name if user_name else '사용자'}님의 고민을 분석 중입니다... 🤖"):
                col1, col2 = st.columns(2)
                with col1:
                    st.success("🎉 AI 추천 야식")
                    st.write("👉 **매콤한 떡볶이 & 쿨피스**")
                with col2:
                    st.info("💡 칼로리 섭취 꿀팁")
                    st.write("👉 국물 소스는 조금만 찍어 드시고 물을 자주 드세요!")
        else:
            st.warning("⚠️ 고민 내용을 먼저 작성해 주세요!")
