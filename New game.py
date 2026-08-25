import streamlit as st
import random
import time

st.set_page_config(page_title="Streamlit 텍스트 RPG", page_icon="⚔️", layout="wide")

# ----------------------------------------------------
# 1. 게임 상태 초기화
# ----------------------------------------------------
def init_game():
    if "player" not in st.session_state:
        st.session_state.player = {
            "name": "모험가",
            "level": 1,
            "hp": 100,
            "max_hp": 100,
            "atk": 15,
            "gold": 50,
            "exp": 0,
            "exp_to_level": 50,
            "potions": 3
        }
    if "monster" not in st.session_state:
        st.session_state.monster = None
    if "logs" not in st.session_state:
        st.session_state.logs = ["🏰 게임을 시작했습니다. 모험을 떠나보세요!"]
    if "game_state" not in st.session_state:
        st.session_state.game_state = "town"  # town, dungeon, battle, game_over

def add_log(message):
    st.session_state.logs.insert(0, f"[{time.strftime('%H:%M:%S')}] {message}")
    if len(st.session_state.logs) > 30:
        st.session_state.logs.pop()

def check_level_up():
    p = st.session_state.player
    while p["exp"] >= p["exp_to_level"]:
        p["exp"] -= p["exp_to_level"]
        p["level"] += 1
        p["max_hp"] += 20
        p["hp"] = p["max_hp"]
        p["atk"] += 5
        p["exp_to_level"] = int(p["exp_to_level"] * 1.5)
        add_log(f"🎉 레벨 업! 레벨 {p['level']}이 되었습니다! (최대 HP +20, 공격력 +5)")

# ----------------------------------------------------
# 2. 몬스터 풀
# ----------------------------------------------------
MONSTERS = [
    {"name": "슬라임", "hp": 30, "atk": 5, "exp": 15, "gold": 10, "icon": "🟢"},
    {"name": "고블린", "hp": 50, "atk": 10, "exp": 30, "gold": 25, "icon": "👺"},
    {"name": "스켈레톤", "hp": 80, "atk": 15, "exp": 50, "gold": 40, "icon": "💀"},
    {"name": "오크 전사", "hp": 120, "atk": 22, "exp": 85, "gold": 70, "icon": "👹"},
    {"name": "드래곤", "hp": 250, "atk": 35, "exp": 200, "gold": 200, "icon": "🐲"}
]

def spawn_monster():
    p_lvl = st.session_state.player["level"]
    # 플레이어 레벨에 맞춰 몬스터 선택 범위 확장
    max_idx = min(len(MONSTERS), 1 + (p_lvl // 2))
    base_monster = random.choice(MONSTERS[:max_idx])
    
    st.session_state.monster = {
        "name": base_monster["name"],
        "icon": base_monster["icon"],
        "hp": base_monster["hp"],
        "max_hp": base_monster["hp"],
        "atk": base_monster["atk"],
        "exp": base_monster["exp"],
        "gold": base_monster["gold"]
    }
    st.session_state.game_state = "battle"
    add_log(f"⚔️ 야생의 {st.session_state.monster['name']}{base_monster['icon']}이(가) 나타났습니다!")

# ----------------------------------------------------
# 3. UI 렌더링
# ----------------------------------------------------
init_game()
p = st.session_state.player

st.title("⚔️ 던전 크롤러 RPG")

# 상단: 플레이어 상태 바
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
with col_stat1:
    st.metric("레벨", f"Lv. {p['level']}")
    hp_ratio = max(0.0, min(1.0, p['hp'] / p['max_hp']))
    st.progress(hp_ratio, text=f"HP: {p['hp']} / {p['max_hp']}")
with col_stat2:
    st.metric("공격력", f"{p['atk']} ⚔️")
with col_stat3:
    st.metric("소지금", f"{p['gold']} 💰")
with col_stat4:
    st.metric("포션", f"{p['potions']} 개 🧪")
    exp_ratio = max(0.0, min(1.0, p['exp'] / p['exp_to_level']))
    st.progress(exp_ratio, text=f"EXP: {p['exp']} / {p['exp_to_level']}")

st.divider()

# 메인 콘텐츠 분할 (좌측: 게임 화면, 우측: 활동 로그)
col_main, col_log = st.columns([2, 1])

with col_main:
    # 1. 게임 오버
    if st.session_state.game_state == "game_over":
        st.error("💀 체력이 0이 되었습니다. 모험이 끝났습니다...")
        if st.button("🔄 처음부터 다시 시작"):
            st.session_state.clear()
            st.rerun()

    # 2. 마을 (Town)
    elif st.session_state.game_state == "town":
        st.subheader("🏘️ 평화로운 마을")
        st.write("던전으로 탐험을 떠나거나, 여관에서 휴식을 취하고 상점을 방문할 수 있습니다.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🌲 던전으로 입장", use_container_width=True):
                spawn_monster()
                st.rerun()
        with c2:
            if st.button("🏨 여관에서 휴식 (무료)", use_container_width=True):
                p["hp"] = p["max_hp"]
                add_log("🛌 여관에서 푹 쉬어 체력을 모두 회복했습니다.")
                st.rerun()
        with c3:
            if st.button("🧪 물약 구매 (20 💰)", use_container_width=True):
                if p["gold"] >= 20:
                    p["gold"] -= 20
                    p["potions"] += 1
                    add_log("🛒 물약을 구매했습니다. (소지금 -20 G)")
                else:
                    st.warning("골드가 부족합니다!")
                st.rerun()

    # 3. 전투 화면 (Battle)
    elif st.session_state.game_state == "battle":
        m = st.session_state.monster
        st.subheader(f"{m['icon']} 전투 중: {m['name']}")
        
        m_hp_ratio = max(0.0, min(1.0, m['hp'] / m['max_hp']))
        st.progress(m_hp_ratio, text=f"몬스터 HP: {m['hp']} / {m['max_hp']}")
        st.caption(f"공격력: {m['atk']} | 보상: {m['exp']} EXP, {m['gold']} 💰")

        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        with btn_col1:
            if st.button("⚔️ 공격", use_container_width=True):
                # 플레이어 턴
                dmg = random.randint(int(p["atk"] * 0.8), int(p["atk"] * 1.2))
                is_crit = random.random() < 0.2
                if is_crit:
                    dmg = int(dmg * 1.5)
                    add_log(f"💥 치명타! {m['name']}에게 {dmg}의 피해를 입혔습니다!")
                else:
                    add_log(f"🗡️ {m['name']}에게 {dmg}의 피해를 입혔습니다.")
                m["hp"] -= dmg

                # 몬스터 처치 확인
                if m["hp"] <= 0:
                    add_log(f"🏆 {m['name']}을(를) 처치했습니다! (+{m['exp']} EXP, +{m['gold']} G)")
                    p["exp"] += m["exp"]
                    p["gold"] += m["gold"]
                    check_level_up()
                    st.session_state.monster = None
                    st.session_state.game_state = "town"
                    st.rerun()

                # 몬스터 턴
                m_dmg = random.randint(int(m["atk"] * 0.7), int(m["atk"] * 1.3))
                p["hp"] -= m_dmg
                add_log(f"🩸 {m['name']}의 반격! {m_dmg}의 피해를 입었습니다.")

                if p["hp"] <= 0:
                    p["hp"] = 0
                    st.session_state.game_state = "game_over"
                st.rerun()

        with btn_col2:
            if st.button(f"🧪 물약 사용 ({p['potions']}개)", use_container_width=True):
                if p["potions"] > 0:
                    if p["hp"] == p["max_hp"]:
                        st.info("이미 체력이 가득 차 있습니다.")
                    else:
                        heal = int(p["max_hp"] * 0.5)
                        p["hp"] = min(p["max_hp"], p["hp"] + heal)
                        p["potions"] -= 1
                        add_log(f"🧪 물약을 마셔 HP {heal}을 회복했습니다.")
                        
                        # 몬스터 턴
                        m_dmg = random.randint(int(m["atk"] * 0.7), int(m["atk"] * 1.3))
                        p["hp"] -= m_dmg
                        add_log(f"🩸 빈틈을 타 {m['name']}이(가) 공격했습니다! ({m_dmg} 피해)")
                        if p["hp"] <= 0:
                            p["hp"] = 0
                            st.session_state.game_state = "game_over"
                        st.rerun()
                else:
                    st.warning("물약이 없습니다!")

        with btn_col3:
            if st.button("🏃 도망치기", use_container_width=True):
                if random.random() < 0.6:
                    add_log("💨 성공적으로 도망쳤습니다!")
                    st.session_state.monster = None
                    st.session_state.game_state = "town"
                else:
                    add_log("❌ 도망치지 못했습니다!")
                    m_dmg = random.randint(int(m["atk"] * 0.7), int(m["atk"] * 1.3))
                    p["hp"] -= m_dmg
                    add_log(f"🩸 {m['name']}에게 뒤를 잡혔습니다! ({m_dmg} 피해)")
                    if p["hp"] <= 0:
                        p["hp"] = 0
                        st.session_state.game_state = "game_over"
                st.rerun()

with col_log:
    st.subheader("📜 모험 일지")
    log_text = "\n".join(st.session_state.logs)
    st.text_area("Log", value=log_text, height=350, disabled=True, label_visibility="collapsed")
