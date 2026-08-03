import streamlit as st
import requests
from datetime import datetime

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="보라고등학교 급식 정보",
    page_icon="🍱",
    layout="centered"
)

# --- 상수 설정 (NEIS API 정보) ---
ATPT_OFCDC_SC_CODE = "J10"      # 경기도교육청 코드
SD_SCHUL_CODE = "7530882"        # 보라고등학교 학교코드
API_URL = "https://open.neis.go.kr/hub/mealServiceDietInfo"

# --- 데이터 로드 함수 (캐싱 적용) ---
@st.cache_data(ttl=3600)  # 1시간 동안 결과 캐싱
def fetch_meal_data(date_str):
    params = {
        "KEY": "",  # 인증키 없이 공공데이터 오픈API 기본 호출 가능 (필요시 개인 KEY 입력)
        "Type": "json",
        "pIndex": 1,
        "pSize": 100,
        "ATPT_OFCDC_SC_CODE": ATPT_OFCDC_SC_CODE,
        "SD_SCHUL_CODE": SD_SCHUL_CODE,
        "MLSV_YMD": date_str
    }
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        data = response.json()
        
        # NEIS API 응답 정상 여부 확인
        if "mealServiceDietInfo" in data:
            return data["mealServiceDietInfo"][1]["row"]
        else:
            return None
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None

# --- UI 레이아웃 ---
st.title("🍱 보라고등학교 급식 메뉴")
st.write("나이스(NEIS) 오픈 API 기반 실시간 급식 정보 서비스입니다.")

st.divider()

# 날짜 선택
selected_date = st.date_input("조회할 날짜를 선택하세요", datetime.now())
date_str = selected_date.strftime("%Y%m%d")

# 급식 데이터 가져오기
meal_rows = fetch_meal_data(date_str)

if meal_rows:
    st.success(f"📅 **{selected_date.strftime('%Y년 %m월 %d일')}** 급식 정보")
    
    # 중식, 석식 구분 출력
    for row in meal_rows:
        meal_name = row.get("MTRIL_SC_NM", "식사")  # 식사 구분 (중식/석식)
        dish_info = row.get("DDISH_NM", "").replace("<br/>", "\n")
        cal_info = row.get("CAL_INFO", "정보 없음")
        ntr_info = row.get("NTR_INFO", "").replace("<br/>", ", ")
        
        # 숫자 및 요리명 가독성 개선
        with st.expander(f"🍽️ **{meal_name}** ({cal_info})", expanded=True):
            st.markdown("##### 📌 식단 메뉴")
            st.text(dish_info)
            
            st.markdown("---")
            st.caption(f"**영양 정보:** {ntr_info if ntr_info else '정보 없음'}")
            st.caption("※ 메뉴 이름 뒤의 숫자는 알레르기 유발 물질 표시 번호입니다.")

else:
    st.info(f"💡 {selected_date.strftime('%Y-%m-%d')}에는 등록된 급식 정보가 없거나 휴교/주말일 수 있습니다.")

# --- 푸터 ---
st.divider()
st.caption("데이터 출처: 교육부 나이스(NEIS) 대국민오픈API")
