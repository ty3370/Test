from datetime import datetime, timedelta, timezone
import json
import uuid
from zoneinfo import ZoneInfo
import pymysql
import streamlit as st
from openai import OpenAI

RETENTION = timedelta(days=3)
MAX_NAME_LENGTH = 30
MAX_MESSAGE_LENGTH = 500

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


def get_entries_and_cleanup():
    cutoff = utc_now() - RETENTION
    db = connect_to_db()
    try:
        with db.cursor() as cur:
            # 1) 방명록 데이터 전체 조회 (글 1개 = 1행)
            sql = (
                "SELECT code, name, chat FROM qna_unique_v3 "
                "WHERE subject=%s AND topic=%s"
            )
            cur.execute(sql, (GB_SUBJECT, GB_TOPIC))
            rows = cur.fetchall()

            kept = []
            expired_codes = []

            for code, author_name, chat_json in rows:
                try:
                    data = json.loads(chat_json) if chat_json else {}
                except json.JSONDecodeError:
                    expired_codes.append(code)
                    continue

                created = parse_timestamp(data.get("created_at"))
                if created is not None and created > cutoff:
                    kept.append({
                        "name": author_name,
                        "message": data.get("message", ""),
                        "created_at": data.get("created_at", ""),
                    })
                else:
                    expired_codes.append(code)

            # 2) 3일이 지난 만료된 글만 DB에서 개별 행 삭제
            if expired_codes:
                placeholders = ", ".join(["%s"] * len(expired_codes))
                del_sql = (
                    f"DELETE FROM qna_unique_v3 "
                    f"WHERE subject=%s AND topic=%s AND code IN ({placeholders})"
                )
                cur.execute(del_sql, [GB_SUBJECT, GB_TOPIC, *expired_codes])

            return sorted(kept, key=lambda x: x.get("created_at", ""), reverse=True)
    finally:
        db.close()


def save_entry(name, message):
    db = connect_to_db()
    try:
        with db.cursor() as cur:
            # 글마다 고유한 UUID를 code에 부여하여 충돌 없이 새 행(Row)으로 추가
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


def moderate_text(name, message):
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            "관리자가 OpenAI API 키를 설정하지 않았습니다. 잠시 후 다시 이용해 주세요."
        )

    client = OpenAI(api_key=api_key)
    result = client.moderations.create(
        model="omni-moderation-latest",
        input=f"Nickname: {name}\nGuestbook message: {message}",
    )
    return result.results[0]


st.set_page_config(
    page_title="온라인 방명록",
    page_icon="📝",
    layout="centered",
)

st.title("📝 온라인 방명록")
st.caption("따뜻한 인사를 남겨 주세요. 등록된 글은 3일 후 자동으로 정리됩니다.")

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

    if not clean_name or not clean_message:
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
    entries = get_entries_and_cleanup()
except Exception as exc:
    st.error(f"방명록을 불러오는 중 DB 오류가 발생했습니다: {exc}")
    entries = []

if not entries:
    st.info("아직 등록된 방명록이 없습니다. 첫 번째 인사를 남겨 보세요!")
else:
    st.caption(f"현재 공개된 글 {len(entries)}개 · 작성 후 3일이 지나면 자동 삭제")
    for entry in entries:
        created = parse_timestamp(entry.get("created_at"))
        if created:
            local_created = created.astimezone()
            date_label = local_created.strftime("%Y-%m-%d %H:%M")
        else:
            date_label = "작성 시간 정보 없음"

        with st.container(border=True):
            st.markdown(f"**{entry.get('name', '익명')}**")
            st.caption(date_label)
            st.write(entry.get("message", ""))

st.caption("안내: 공개 방명록이므로 개인 연락처, 주소 등 민감한 개인정보는 남기지 마세요.")
