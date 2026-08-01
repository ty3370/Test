import os
import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 칭찬 생성기",
    page_icon="👏",
    layout="centered"
)

# Secrets에서 API 키 불러오기
openai_api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("🔑 OPENAI_API_KEY가 설정되지 않았습니다. Streamlit Secrets를 확인해 주세요.")
    st.stop()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=openai_api_key)

# 앱 타이틀
st.title("👏 AI 칭찬 생성기")
st.subheader("칭찬받고 싶은 내용이나 오늘 한 일을 입력해 보세요!")
st.write("작은 일도 좋아요. AI가 정성스러운 칭찬과 격려를 보내드립니다.")

st.divider()

# 사용자 입력 Form
with st.form("praise_form"):
    user_input = st.text_area(
        "어떤 칭찬을 받고 싶나요?",
        placeholder="예: 오늘 일찍 일어나서 운동을 갔다 왔어 / 프로젝트 보고서를 잘 끝냈어",
        height=120
    )
    
    tone = st.selectbox(
        "칭찬 스타일을 선택하세요",
        ["따뜻하고 다정한 스타일", "열정적이고 극찬하는 스타일", "유쾌하고 위트 있는 스타일", "담백하고 진정성 있는 스타일"]
    )
    
    submitted = st.form_submit_button("칭찬받기 ✨", use_container_width=True)

# 결과 생성 Logic
if submitted:
    if not user_input.strip():
        st.warning("내용을 입력해 주세요!")
    else:
        with st.spinner("AI가 당신을 위한 칭찬을 작성 중입니다... 💌"):
            try:
                system_prompt = f"""
                당신은 따뜻하고 공감 능력이 뛰어난 칭찬 전문가입니다. 
                사용자가 작성한 내용을 바탕으로 진심 어린 칭찬과 격려를 해주세요.
                선택된 칭찬 스타일: {tone}
                답변은 한국어로 작성하고, 가독성 좋게 적절한 이모지를 사용하세요.
                """

                response = client.chat.completions.create(
                    model="gpt-5.5-nano",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                )

                praise_text = response.choices[0].message.content

                st.success("칭찬이 도착했습니다!")
                st.markdown("---")
                st.markdown(praise_text)
                st.markdown("---")

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
