import datetime
import requests
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="보라고등학교 오늘의 급식",
    page_icon="🍱",
    layout="centered",
)

# NEIS Open API 설정
ATPT_OFCDC_SC_CODE = "J10"
SD_SCHUL_CODE = "7530882"


def get_meal_info(date_str):
    """NEIS API를 호출하여 해당 날짜의 급식 정보를 가져옵니다."""
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    params = {
        "KEY": "",  # 기본 인증키 사용 (필요시 NEIS에서 발급받은 API KEY 입력)
        "Type": "json",
        "pIndex": 1,
        "pSize": 10,
        "ATPT_OFCDC_SC_CODE": ATPT_OFCDC_SC_CODE,
        "SD_SCHUL_CODE": SD_SCHUL_CODE,
        "MLSV_YMD": date_str,
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if "mealServiceDietInfo" in data:
            meal_data = data["mealServiceDietInfo"][1]["row"]
            return meal_data
        return None
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return None


# --- UI 레이아웃 ---
st.title("🍱 보라고등학교 급식 안내")
st.caption("NEIS 교육행정정보시스템 Open API 연동")

# 날짜 선택 사이드바/메인
selected_date = st.date_input("날짜를 선택하세요", datetime.date.today())
date_str = selected_date.strftime("%Y%m%d")

st.divider()

# 선택한 날짜 표시
formatted_date_title = selected_date.strftime("%Y년 %m월 %d일")
st.subheader(f"📅 {formatted_date_title} 급식 메뉴")

# 급식 데이터 조회
meal_info = get_meal_info(date_str)

if meal_info:
    for item in meal_info:
        meal_type = item.get("MMEAL_SC_NM", "급식")
        # <br/> 태그를 줄바꿈으로 변환 및 알레르기 번호 제거(선택사항)
        dishes = item.get("DDISH_NM", "").replace("<br/>", "\n")

        # 알레르기 번호(예: (1.2.3))를 단순하게 보고 싶다면 아래 정규식 처리 가능
        # import re
        # dishes = re.sub(r"\([0-9.]+\)", "", dishes)

        cal_info = item.get("CAL_INFO", "정보 없음")

        with st.container():
            st.markdown(f"#### 🍽️ {meal_type}")
            st.code(dishes, language=None)
            st.caption(f"🔥 칼로리: {cal_info}")
            st.write("")
else:
    st.info("💡 해당 날짜에는 등록된 급식 정보가 없습니다. (주말, 공휴일 또는 방학)")

# 하단 안내
st.divider()
st.caption("※ 알레르기 정보는 학교 홈페이지 또는 식단표의 원본 번호를 참고하세요.")
