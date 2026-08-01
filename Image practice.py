import os
import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io

# 페이지 기본 설정
st.set_page_config(
    page_title="AI Multi-Modal Hub",
    page_icon="🎨",
    layout="centered"
)

# Secrets 및 환경변수에서 API 키 불러오기
openai_api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("🔑 OPENAI_API_KEY가 설정되지 않았습니다. Streamlit Secrets를 확인해 주세요.")
    st.stop()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=openai_api_key)

st.title("🎨 AI 멀티모달 스튜디오")
st.caption("GPT-5.4-Nano 기반 인식 & GPT-Image-2 기반 생성/편집")

# 서비스 선택 탭
tab1, tab2, tab3 = st.tabs(["👁️ 이미지/텍스트 분석", "🖼️ 이미지 생성", "✏️ 이미지 편집"])

# Helper function: 이미지 파일을 base64로 변환 (Vision 모델 전송용)
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')


# ==========================================
# TAB 1: 이미지 및 텍스트 인식 (gpt-5.4-nano)
# ==========================================
with tab1:
    st.header("이미지 및 텍스트 인식 (gpt-5.4-nano)")
    
    uploaded_file = st.file_uploader("분석할 이미지를 업로드하세요 (선택 사항)", type=["jpg", "jpeg", "png", "webp"])
    prompt_text = st.text_area("질문이나 요청 사항을 입력하세요:", placeholder="예: 이 사진 속에 있는 글자를 읽어주고 내용을 설명해줘.")
    
    if st.button("분석 실행 🚀", key="analyze_btn"):
        if not prompt_text.strip() and not uploaded_file:
            st.warning("텍스트 입력이나 이미지 업로드 중 하나 이상을 입력해 주세요.")
        else:
            with st.spinner("gpt-5.4-nano 모델이 분석 중입니다..."):
                try:
                    messages_content = []
                    
                    if prompt_text.strip():
                        messages_content.append({"type": "text", "text": prompt_text})
                    
                    if uploaded_file:
                        image_bytes = uploaded_file.read()
                        base64_image = encode_image(image_bytes)
                        mime_type = uploaded_file.type
                        messages_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        })
                    
                    # gpt-5.4-nano 모델 호출
                    response = client.chat.completions.create(
                        model="gpt-5.4-nano",
                        messages=[
                            {
                                "role": "user",
                                "content": messages_content
                            }
                        ]
                    )
                    
                    st.success("분석 완료!")
                    st.markdown(response.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")


# ==========================================
# TAB 2: 이미지 생성 (gpt-image-2)
# ==========================================
with tab2:
    st.header("이미지 생성 (gpt-image-2)")
    
    gen_prompt = st.text_area("생성할 이미지에 대한 설명(프롬프트):", placeholder="예: 사이버펑크 스타일의 미래 도시 야경, 고화질")
    
    if st.button("이미지 생성 ✨", key="generate_btn"):
        if not gen_prompt.strip():
            st.warning("프롬프트를 입력해 주세요.")
        else:
            with st.spinner("gpt-image-2 모델이 이미지를 생성 중입니다..."):
                try:
                    # gpt-image-2 모델 호출 (Generations)
                    result = client.images.generate(
                        model="gpt-image-2",
                        prompt=gen_prompt,
                        n=1,
                    )
                    
                    image_url = result.data[0].url
                    st.image(image_url, caption="생성된 이미지", use_container_width=True)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")


# ==========================================
# TAB 3: 이미지 편집 (gpt-image-2)
# ==========================================
with tab3:
    st.header("이미지 편집 및 인페인팅 (gpt-image-2)")
    
    source_image = st.file_uploader("원본 이미지를 업로드하세요 (PNG 권장)", type=["png", "jpg", "jpeg"], key="edit_source")
    mask_image = st.file_uploader("마스크(수정할 영역) 이미지를 업로드하세요 (선택 사항)", type=["png"], key="edit_mask")
    edit_prompt = st.text_input("어떻게 수정할지 입력하세요:", placeholder="예: 배경에 무지개를 추가해줘")
    
    if st.button("이미지 편집 🖌️", key="edit_btn"):
        if not source_image or not edit_prompt.strip():
            st.warning("원본 이미지와 수정 요청 사항을 모두 입력해 주세요.")
        else:
            with st.spinner("gpt-image-2 모델이 이미지를 편집 중입니다..."):
                try:
                    source_bytes = source_image.read()
                    
                    # Mask 여부에 따른 API 호출 분기
                    if mask_image:
                        mask_bytes = mask_image.read()
                        result = client.images.edit(
                            model="gpt-image-2",
                            image=source_bytes,
                            mask=mask_bytes,
                            prompt=edit_prompt,
                            n=1,
                        )
                    else:
                        result = client.images.edit(
                            model="gpt-image-2",
                            image=source_bytes,
                            prompt=edit_prompt,
                            n=1,
                        )
                        
                    edited_url = result.data[0].url
                    st.image(edited_url, caption="편집된 이미지", use_container_width=True)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
