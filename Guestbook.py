from datetime import datetime, timezone
import json
from types import SimpleNamespace
import uuid
from zoneinfo import ZoneInfo
import pymysql
import streamlit as st
from openai import OpenAI

MAX_NAME_LENGTH = 30
MAX_MESSAGE_LENGTH = 500

MODERATION_MODEL = "gpt-6-luna"

# 기존 qna_unique_v3 테이블에서 방명록 데이터를 구분하기 위한 고정 태그
GB_SUBJECT = "방명록"
GB_TOPIC = "전체"


def utc_now():
    return datetime.now(timezone.utc)


def parse_timestamp(value):
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def connect_to_db():
    return pymysql.connect(
        host=st.secrets["DB_HOST"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_DATABASE"],
        charset="utf8mb4",
        autocommit=True,
    )


def get_entries():
    db = connect_to_db()
    try:
        with db.cursor() as cur:
            sql = (
                "SELECT code, name, chat FROM qna_unique_v3 "
                "WHERE subject=%s AND topic=%s"
            )
            cur.execute(sql, (GB_SUBJECT, GB_TOPIC))
            rows = cur.fetchall()

            entries = []
            for code, author_name, chat_json in rows:
                try:
                    data = json.loads(chat_json) if chat_json else {}
                except json.JSONDecodeError:
                    continue

                entries.append({
                    "code": code,
                    "name": author_name,
                    "message": data.get("message", ""),
                    "created_at": data.get("created_at", ""),
                })

            return sorted(entries, key=lambda x: x.get("created_at", ""), reverse=True)
    finally:
        db.close()


def save_entry(name, message):
    db = connect_to_db()
    try:
        with db.cursor() as cur:
            entry_id = uuid.uuid4().hex
            payload = json.dumps(
                {
                    "message": message,
                    "created_at": utc_now().isoformat(),
                },
                ensure_ascii=False,
            )
            ts = datetime.now(ZoneInfo("Asia/Seoul"))

            sql = (
                "INSERT INTO qna_unique_v3 "
                "(number, name, code, subject, topic, chat, time) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )
            cur.execute(
                sql,
                ("GUESTBOOK", name, entry_id, GB_SUBJECT, GB_TOPIC, payload, ts),
            )
    finally:
        db.close()


def delete_entry(entry_code):
    """관리자 모드에서 특정 방명록 글 1개를 DB에서 즉시 삭제"""
    db = connect_to_db()
    try:
        with db.cursor() as cur:
            sql = (
                "DELETE FROM qna_unique_v3 "
                "WHERE subject=%s AND topic=%s AND code=%s"
            )
            cur.execute(sql, (GB_SUBJECT, GB_TOPIC, entry_code))
    finally:
        db.close()


def moderate_text(name, message):
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "관리자가 OpenAI API 키를 설정하지 않았습니다. 잠시 후 다시 이용해 주세요."
        )

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "당신은 학교 공개 방명록의 엄격한 콘텐츠 검열관입니다.\n"
        "사용자가 입력한 닉네임과 메시지를 분석해 공개 방명록에 부적절한지 판단하세요.\n\n"
        "[차단 기준 (하나라도 해당하면 flagged: true)]\n"
        "1. 한국어·외국어 욕설, 비속어, 패드립, 성적인 표현, 혐오·차별 발언\n"
        "2. 초성 욕설(예: ㅅㅂ, ㅂㅅ, ㅈㄹ 등), 숫자/특수문자/야민정음으로 교묘하게 변형한 욕설 및 은어\n"
        "3. 특정 학생·교사·타인을 실명이나 별명으로 비방, 조롱, 따돌림, 저격하는 내용\n"
        "4. 폭력, 자해, 불법 행위 조장 또는 도배성 무의미한 문자열\n"
        "5. 전화번호, 집 주소, 개인 SNS 계정 등 타인이나 본인의 민감한 개인정보 노출\n\n"
        "[허용 기준 (flagged: false)]\n"
        "- 건전한 응원, 인사, 학습 다짐, 일상적인 유머 등 학생이 공개 게시판에 남기기에 적절한 글\n\n"
        '반드시 다음 JSON 형식으로만 답하세요: {"flagged": true 또는 false}'
    )

    resp = client.chat.completions.create(
        model=MODERATION_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"닉네임: {name}\n메시지: {message}"},
        ],
    )

    raw_content = resp.choices[0].message.content or "{}"
    parsed = json.loads(raw_content)

    return SimpleNamespace(flagged=bool(parsed.get("flagged", True)))


st.set_page_config(
    page_title="온라인 방명록",
    page_icon="📝",
    layout="centered",
)

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

st.title("📝 온라인 방명록")
st.caption("따뜻한 인사를 남겨 주세요.")

if st.session_state["is_admin"]:
    col_banner, col_exit = st.columns([4, 1])
    with col_banner:
        st.info("🔑 **관리자 모드**가 활성화되었습니다. 각 게시글을 개별 삭제할 수 있습니다.")
    with col_exit:
        if st.button("종료", use_container_width=True):
            st.session_state["is_admin"] = False
            st.rerun()

with st.form("guestbook_form", clear_on_submit=True):
    name = st.text_input("닉네임", max_chars=MAX_NAME_LENGTH, placeholder="닉네임")
    message = st.text_area(
        "방명록 메시지",
        max_chars=MAX_MESSAGE_LENGTH,
        height=130,
        placeholder="방명록에 남길 말을 작성해 주세요.",
    )
    submitted = st.form_submit_button("검열 후 등록", type="primary", use_container_width=True)

if submitted:
    clean_name = name.strip()
    clean_message = message.strip()
    admin_pw = st.secrets.get("ADMIN_PASSWORD", "")

    if admin_pw and (clean_name == admin_pw or clean_message == admin_pw):
        st.session_state["is_admin"] = True
        st.rerun()
    elif not clean_name or not clean_message:
        st.warning("닉네임과 메시지를 모두 입력해 주세요.")
    elif len(clean_name) > MAX_NAME_LENGTH or len(clean_message) > MAX_MESSAGE_LENGTH:
        st.warning("입력 글자 수 제한을 확인해 주세요.")
    else:
        try:
            with st.spinner("AI가 메시지를 확인하고 있습니다..."):
                moderation = moderate_text(clean_name, clean_message)

            if moderation.flagged:
                st.error("부적절할 수 있는 표현이 감지되어 글을 등록하지 않았습니다. 표현을 바꿔 다시 작성해 주세요.")
            else:
                save_entry(clean_name, clean_message)
                st.success("방명록이 등록되었습니다!")
                st.rerun()
        except Exception as exc:
            st.error(f"검열 또는 등록 과정에서 문제가 발생했습니다: {exc}")

st.divider()
st.subheader("방명록")

try:
    entries = get_entries()
except Exception as exc:
    st.error(f"방명록을 불러오는 중 DB 오류가 발생했습니다: {exc}")
    entries = []

if not entries:
    st.info("아직 등록된 방명록이 없습니다. 첫 번째 인사를 남겨 보세요!")
else:
    st.caption(f"현재 공개된 글 {len(entries)}개")
    for entry in entries:
        created = parse_timestamp(entry.get("created_at"))
        if created:
            local_created = created.astimezone()
            date_label = local_created.strftime("%Y-%m-%d %H:%M")
        else:
            date_label = "작성 시간 정보 없음"

        with st.container(border=True):
            if st.session_state["is_admin"]:
                col_head, col_del = st.columns([5, 1])
                with col_head:
                    st.markdown(f"**{entry.get('name', '익명')}**")
                    st.caption(date_label)
                with col_del:
                    if st.button("삭제", key=f"del_{entry['code']}", use_container_width=True):
                        delete_entry(entry["code"])
                        st.rerun()
            else:
                st.markdown(f"**{entry.get('name', '익명')}**")
                st.caption(date_label)

            st.write(entry.get("message", ""))

st.caption("안내: 공개 방명록이므로 개인 연락처, 주소 등 민감한 개인정보는 남기지 마세요.")
