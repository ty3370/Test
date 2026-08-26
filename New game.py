import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(
    page_title="물리학자 서바이벌",
    page_icon="⚛️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 0.2rem;
        padding-bottom: 0rem;
        padding-left: 0.2rem;
        padding-right: 0.2rem;
        max-width: 520px;
    }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 이미지 Base64 변환 헬퍼
# ----------------------------------------------------
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            ext = path.split(".")[-1].lower()
            mime = "image/png" if ext == "png" else "image/jpeg"
            return f"data:{mime};base64,{data}"
    return ""

img_warrior = get_image_base64("assets/warrior.png") # 뉴턴
img_archer  = get_image_base64("assets/archer.png")  # 아인슈타인
img_mage    = get_image_base64("assets/mage.png")    # 퀴리
img_enemy   = get_image_base64("assets/enemy.png")
img_boss    = get_image_base64("assets/boss.png")
img_bora    = get_image_base64("assets/bora.png")    # 보라고 마크

game_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * {{
    box-sizing: border-box;
    user-select: none;
    -webkit-user-select: none;
    touch-action: none;
  }}
  body {{
    margin: 0;
    padding: 0;
    background: #0f172a;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: 'Segoe UI', AppleSDGothicNeo-Regular, sans-serif;
    color: #fff;
    overflow: hidden;
  }}
  #gameWrapper {{
    position: relative;
    width: 100%;
    max-width: 480px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  canvas {{
    display: block;
    background: #cbd5e1;
    border: 3px solid #64748b;
    border-radius: 14px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.4);
    width: 100%;
    aspect-ratio: 420 / 580;
    cursor: default;
  }}
  #touchControls {{
    position: relative;
    width: 100%;
    height: 145px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 6px;
  }}
  #moveTouchArea {{
    position: relative;
    width: 96%;
    height: 135px;
    background: rgba(30, 41, 59, 0.45);
    border: 2px dashed rgba(148, 163, 184, 0.35);
    border-radius: 18px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }}
  #moveGuide {{
    display: flex;
    flex-direction: column;
    align-items: center;
    pointer-events: none;
    color: rgba(226, 232, 240, 0.7);
    transition: opacity 0.2s ease;
  }}
  .guide-arrows {{
    font-size: 22px;
    letter-spacing: 5px;
    color: #38bdf8;
    margin-bottom: 3px;
  }}
  .guide-label {{
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
  }}
  #joystickZone {{
    position: absolute;
    width: 110px;
    height: 110px;
    background: rgba(255, 255, 255, 0.2);
    border: 3px solid rgba(255, 255, 255, 0.6);
    border-radius: 50%;
    box-shadow: 0 0 16px rgba(56, 189, 248, 0.35);
    display: none;
    pointer-events: none;
    transform: translate(-50%, -50%);
  }}
  #joystickKnob {{
    position: absolute;
    top: 50%;
    left: 50%;
    width: 50px;
    height: 50px;
    margin-top: -25px;
    margin-left: -25px;
    background: radial-gradient(circle, #ffffff 40%, #94a3b8 100%);
    border-radius: 50%;
    pointer-events: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }}
</style>
</head>
<body>

<div id="gameWrapper">
  <canvas id="gameCanvas" width="420" height="580"></canvas>
  
  <div id="touchControls">
    <div id="moveTouchArea">
      <div id="moveGuide">
        <div class="guide-arrows">▲ ▼ ◀ ▶</div>
        <div class="guide-label">터치 & 드래그로 이동 (공격은 자동!)</div>
      </div>
      <div id="joystickZone">
        <div id="joystickKnob"></div>
      </div>
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const isMobileDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

// PC 환경 속도 보정 계수 (1.35배 가속)
const pcSpeedBoost = isMobileDevice ? 1.0 : 1.35;

// --- 이미지 로드 ---
const IMAGES = {{
  WARRIOR: new Image(),
  ARCHER: new Image(),
  MAGE: new Image(),
  ENEMY: new Image(),
  BOSS: new Image(),
  BORA: new Image()
}};

IMAGES.WARRIOR.src = "{img_warrior}";
IMAGES.ARCHER.src = "{img_archer}";
IMAGES.MAGE.src = "{img_mage}";
IMAGES.ENEMY.src = "{img_enemy}";
IMAGES.BOSS.src = "{img_boss}";
IMAGES.BORA.src = "{img_bora}";

function drawEntityWithFlip(img, x, y, radius, fallbackColor, facingLeft = false) {{
  ctx.save();
  ctx.translate(x, y);
  if (facingLeft) ctx.scale(-1, 1);

  if (img && img.src && img.complete && img.naturalWidth !== 0) {{
    const size = radius * 2.5;
    ctx.drawImage(img, -size / 2, -size / 2, size, size);
  }} else {{
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, Math.PI * 2);
    ctx.fillStyle = fallbackColor;
    ctx.shadowBlur = 6;
    ctx.shadowColor = fallbackColor;
    ctx.fill();
    ctx.shadowBlur = 0;
  }}
  ctx.restore();
}}

const labProps = [
  {{ x: 60, y: 70, type: "flask", color: "#38bdf8" }},
  {{ x: 360, y: 80, type: "beaker", color: "#4ade80" }},
  {{ x: 70, y: 280, type: "beaker", color: "#f472b6" }},
  {{ x: 350, y: 320, type: "flask", color: "#a855f7" }},
  {{ x: 65, y: 500, type: "flask", color: "#38bdf8" }},
  {{ x: 355, y: 510, type: "beaker", color: "#4ade80" }}
];

function drawLabBackground() {{
  ctx.fillStyle = "#e2e8f0";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "#cbd5e1";
  ctx.lineWidth = 1.5;
  for (let x = 0; x < canvas.width; x += 38) {{
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
  }}
  for (let y = 0; y < canvas.height; y += 38) {{
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
  }}

  // 맵 중앙에 bora.png 배치
  if (IMAGES.BORA && IMAGES.BORA.src && IMAGES.BORA.complete && IMAGES.BORA.naturalWidth !== 0) {{
    const bSize = 170;
    ctx.save();
    ctx.globalAlpha = 0.45;
    ctx.drawImage(IMAGES.BORA, canvas.width / 2 - bSize / 2, canvas.height / 2 - bSize / 2, bSize, bSize);
    ctx.restore();
  }}

  ctx.strokeStyle = "#94a3b8";
  ctx.lineWidth = 2;
  ctx.strokeRect(25, 25, canvas.width - 50, canvas.height - 50);

  labProps.forEach(prop => {{
    ctx.save();
    ctx.translate(prop.x, prop.y);
    if (prop.type === "flask") {{
      ctx.beginPath();
      ctx.moveTo(-9, 9); ctx.lineTo(9, 9); ctx.lineTo(3.5, -3); ctx.lineTo(3.5, -10);
      ctx.lineTo(-3.5, -10); ctx.lineTo(-3.5, -3); ctx.closePath();
      ctx.fillStyle = prop.color;
      ctx.globalAlpha = 0.55;
      ctx.fill();
      ctx.globalAlpha = 1.0;
      ctx.strokeStyle = "#475569";
      ctx.lineWidth = 2;
      ctx.stroke();
    }} else if (prop.type === "beaker") {{
      ctx.beginPath();
      ctx.rect(-8, -9, 16, 18);
      ctx.fillStyle = prop.color;
      ctx.globalAlpha = 0.5;
      ctx.fill();
      ctx.globalAlpha = 1.0;
      ctx.strokeStyle = "#475569";
      ctx.lineWidth = 2;
      ctx.stroke();
    }}
    ctx.restore();
  }});
}}

// --- 클래스 정의 ---
const CLASSES = {{
  WARRIOR: {{
    id: "WARRIOR",
    name: "아이작 뉴턴",
    title: "만유인력과 운동 법칙",
    desc: "사과 참격 / 사과 나무 휘두르기(근접, 방어력 우수)",
    icon: "🍎",
    color: "#dc2626",
    maxHp: 160,
    atk: 55,
    def: 0.75,
    speed: 2.8,
    range: 95,
    cooldown: 90
  }},
  ARCHER: {{
    id: "ARCHER",
    name: "알베르트 아인슈타인",
    title: "상대성 이론과 광자",
    desc: "광자 화살 / 적 및 벽에 최대 1회 튕기며 연속 타격",
    icon: "⚡",
    color: "#d97706",
    maxHp: 100,
    atk: 42,
    def: 0.95,
    speed: 3.3,
    range: 480,
    cooldown: 90
  }},
  MAGE: {{
    id: "MAGE",
    name: "마리 퀴리",
    title: "방사능과 라듐 연구",
    desc: "방사성 물질 지뢰 / 밟거나 시간 경과 시 광역 폭발",
    icon: "🧪",
    color: "#059669",
    maxHp: 95,
    atk: 65,
    def: 1.05,
    speed: 2.8,
    mineRadius: 13,       // 초기 지뢰 접촉/감지 반경
    explosionRadius: 100, // 초기 폭발 반경
    cooldown: 90
  }}
}};

let selectedClass = null;
let gameState = "SELECT";
let selectUnlockTime = 0;

const player = {{
  x: 210,
  y: 290,
  radius: 16,
  facingAngle: 0,
  facingLeft: false,
  hp: 100,
  maxHp: 100,
  atk: 30,
  def: 1.0,
  speed: 2.8,
  range: 95,
  mineRadius: 13,
  explosionRadius: 100,
  bounces: 1,
  baseCooldown: 90,
  attackCooldown: 90
}};

const keys = {{}};
let joystick = {{
  active: false,
  touchId: null,
  startX: 0,
  startY: 0,
  dx: 0,
  dy: 0
}};

let score = 0;
let level = 1;
let exp = 0;
let expToNext = 50;

let attacks = [];
let mines = [];
let enemies = [];
let particles = [];
let damageTexts = [];
let slashEffects = [];

// --- PC 키보드 ---
window.addEventListener("keydown", e => {{
  keys[e.key.toLowerCase()] = true;
  if ((gameState === "GAMEOVER" || gameState === "CLEAR") && e.key.toLowerCase() === "r") {{
    resetGame();
  }}
}});
window.addEventListener("keyup", e => {{ keys[e.key.toLowerCase()] = false; }});

function getCanvasCoords(clientX, clientY) {{
  const rect = canvas.getBoundingClientRect();
  return {{
    x: (clientX - rect.left) * (canvas.width / rect.width),
    y: (clientY - rect.top) * (canvas.height / rect.height)
  }};
}}

function handleInteraction(coords) {{
  if (gameState === "SELECT") {{
    if (Date.now() > selectUnlockTime) handleClassSelectClick(coords.x, coords.y);
  }} else if (gameState === "UPGRADE") {{
    handleUpgradeSelectClick(coords.x, coords.y);
  }} else if (gameState === "GAMEOVER" || gameState === "CLEAR") {{
    resetGame();
  }}
}}

canvas.addEventListener("mousedown", e => handleInteraction(getCanvasCoords(e.clientX, e.clientY)));
canvas.addEventListener("touchstart", e => {{
  handleInteraction(getCanvasCoords(e.touches[0].clientX, e.touches[0].clientY));
}}, {{ passive: false }});

// --- 모바일 플로팅 조이스틱 ---
const moveTouchArea = document.getElementById("moveTouchArea");
const moveGuide = document.getElementById("moveGuide");
const joyZone = document.getElementById("joystickZone");
const joyKnob = document.getElementById("joystickKnob");

moveTouchArea.addEventListener("touchstart", e => {{
  e.preventDefault();
  if (joystick.active) return;

  const touch = e.changedTouches[0];
  const areaRect = moveTouchArea.getBoundingClientRect();
  
  joystick.active = true;
  joystick.touchId = touch.identifier;
  joystick.startX = touch.clientX;
  joystick.startY = touch.clientY;

  moveGuide.style.opacity = "0";
  
  const relativeX = touch.clientX - areaRect.left;
  const relativeY = touch.clientY - areaRect.top;
  joyZone.style.left = `${{relativeX}}px`;
  joyZone.style.top = `${{relativeY}}px`;
  joyZone.style.display = "block";
  joyKnob.style.transform = "translate(0px, 0px)";

  updateFloatingJoystick(touch.clientX, touch.clientY);
}}, {{ passive: false }});

window.addEventListener("touchmove", e => {{
  if (!joystick.active) return;
  for (let i = 0; i < e.touches.length; i++) {{
    if (e.touches[i].identifier === joystick.touchId) {{
      updateFloatingJoystick(e.touches[i].clientX, e.touches[i].clientY);
      break;
    }}
  }}
}}, {{ passive: false }});

function endTouch(e) {{
  if (!joystick.active) return;
  for (let i = 0; i < e.changedTouches.length; i++) {{
    if (e.changedTouches[i].identifier === joystick.touchId) {{
      joystick.active = false;
      joystick.touchId = null;
      joystick.dx = 0;
      joystick.dy = 0;
      joyZone.style.display = "none";
      moveGuide.style.opacity = "1";
      break;
    }}
  }}
}}

window.addEventListener("touchend", endTouch);
window.addEventListener("touchcancel", endTouch);

function updateFloatingJoystick(clientX, clientY) {{
  let diffX = clientX - joystick.startX;
  let diffY = clientY - joystick.startY;
  let dist = Math.hypot(diffX, diffY);
  const maxR = 48;

  let visualX = diffX;
  let visualY = diffY;
  if (dist > maxR) {{
    visualX = (diffX / dist) * maxR;
    visualY = (diffY / dist) * maxR;
  }}
  joyKnob.style.transform = `translate(${{visualX}}px, ${{visualY}}px)`;

  if (dist > 6) {{
    const angle = Math.atan2(diffY, diffX);
    joystick.dx = Math.cos(angle);
    joystick.dy = Math.sin(angle);
    player.facingAngle = angle;
    player.facingLeft = (diffX < 0);
  }} else {{
    joystick.dx = 0;
    joystick.dy = 0;
  }}
}}

function handleClassSelectClick(x, y) {{
  const classes = [CLASSES.WARRIOR, CLASSES.ARCHER, CLASSES.MAGE];
  classes.forEach((cls, i) => {{
    const top = 140 + i * 130;
    if (x >= 25 && x <= canvas.width - 25 && y >= top && y <= top + 115) {{
      initPlayerWithClass(cls);
    }}
  }});
}}

function initPlayerWithClass(cls) {{
  selectedClass = cls;
  player.x = canvas.width / 2;
  player.y = canvas.height / 2;
  player.maxHp = cls.maxHp;
  player.hp = cls.maxHp;
  player.atk = cls.atk;
  player.def = cls.def;
  player.speed = cls.speed;
  player.range = cls.range || 95;
  player.mineRadius = cls.mineRadius || 13;
  player.explosionRadius = cls.explosionRadius || 100;
  player.bounces = 1;
  player.baseCooldown = isMobileDevice ? Math.round(cls.cooldown * 1.35) : cls.cooldown;
  player.attackCooldown = 0;
  player.facingAngle = 0;
  player.facingLeft = false;
  gameState = "PLAYING";
}}

// 5레벨 단위 특성 선택
function handleUpgradeSelectClick(x, y) {{
  const options = [
    {{ id: "ATK", title: "⚔️ 공격력 증가", desc: "공격력 +60% 증가" }},
    {{ id: "DEF", title: "🛡️ 방어력 증가", desc: "받는 피해 -30% 감소" }},
    {{ id: "SPD", title: "⚡ 공격 속도 증가", desc: "공격 주기 35% 단축" }}
  ];

  options.forEach((opt, i) => {{
    const top = 180 + i * 110;
    if (x >= 35 && x <= canvas.width - 35 && y >= top && y <= top + 90) {{
      if (opt.id === "ATK") {{
        player.atk = Math.round(player.atk * 1.6);
        addDamageText(player.x, player.y - 25, "ATK +60%! ⚔️", "#ef4444");
      }} else if (opt.id === "DEF") {{
        player.def = Math.max(0.2, player.def * 0.7);
        addDamageText(player.x, player.y - 25, "DEF +30%! 🛡️", "#3b82f6");
      }} else if (opt.id === "SPD") {{
        player.baseCooldown = Math.max(12, Math.round(player.baseCooldown * 0.65));
        const currentSec = (player.baseCooldown / 60).toFixed(2);
        addDamageText(player.x, player.y - 25, `공격 주기 ${{currentSec}}초로 단축! ⚡`, "#eab308");
      }}
      gameState = "PLAYING";
    }}
  }});
}}

// --- 자동 공격 로직 ---
function autoAttack() {{
  if (gameState !== "PLAYING") return;

  if (player.attackCooldown > 0) {{
    player.attackCooldown--;
    return;
  }}

  player.attackCooldown = player.baseCooldown;

  let targetAngle = player.facingAngle;
  if (enemies.length > 0) {{
    let nearestDist = 9999;
    let nearestEnemy = null;
    enemies.forEach(e => {{
      let d = Math.hypot(e.x - player.x, e.y - player.y);
      if (d < nearestDist) {{
        nearestDist = d;
        nearestEnemy = e;
      }}
    }});
    if (nearestEnemy) {{
      targetAngle = Math.atan2(nearestEnemy.y - player.y, nearestEnemy.x - player.x);
      player.facingAngle = targetAngle;
      player.facingLeft = (nearestEnemy.x < player.x);
    }}
  }}

  if (selectedClass.id === "WARRIOR") {{
    slashEffects.push({{
      x: player.x,
      y: player.y,
      baseAngle: targetAngle,
      range: player.range,
      progress: 0,
      life: Math.round(14 / pcSpeedBoost),
      maxLife: Math.round(14 / pcSpeedBoost),
      hitEnemies: new Set()
    }});
  }} else if (selectedClass.id === "ARCHER") {{
    attacks.push({{
      type: "BOUNCE_ARROW",
      x: player.x,
      y: player.y,
      vx: Math.cos(targetAngle) * (8.8 * pcSpeedBoost),
      vy: Math.sin(targetAngle) * (8.8 * pcSpeedBoost),
      damage: player.atk,
      travelled: 0,
      maxDist: selectedClass.range,
      radius: 4,
      bouncesLeft: player.bounces,
      lastHitEnemyId: null
    }});
  }} else if (selectedClass.id === "MAGE") {{
    mines.push({{
      x: player.x,
      y: player.y,
      radius: player.mineRadius, // 레벨업에 따라 증가된 지뢰 감지 반경
      damage: player.atk,
      explosionRadius: player.explosionRadius,
      timer: 140,
      pulse: 0
    }});
    createHitParticles(player.x, player.y, "#34d399");
  }}
}}

// 레벨업 시 체력 증가 및 3의 배수 레벨 성장 효과
function applyDamage(enemy, amount, enemyIdx) {{
  enemy.hp -= amount;
  addDamageText(enemy.x, enemy.y - 12, Math.round(amount), "#dc2626");

  if (enemy.hp <= 0) {{
    let expGained = enemy.isBoss ? 75 : 25;
    exp += expGained;
    score += enemy.isBoss ? 250 : 80;
    createHitParticles(enemy.x, enemy.y, "#ef4444");
    enemies.splice(enemyIdx, 1);

    if (exp >= expToNext) {{
      exp -= expToNext;
      level++;
      expToNext = Math.round(expToNext * 1.30);

      // 3의 배수 레벨마다 캐릭터별 특수 강화 (퀴리: 폭발 범위 + 지뢰 원 자체 범위 증가)
      if (level % 3 === 0) {{
        if (selectedClass.id === "WARRIOR") {{
          player.range += 6;
          addDamageText(player.x, player.y - 45, "공격 범위 증가! 🍎", "#dc2626");
        }} else if (selectedClass.id === "MAGE") {{
          player.mineRadius += 2;      // 지뢰 원 자체 접촉/감지 범위 증가
          player.explosionRadius += 7; // 지뢰 폭발 범위 증가
          addDamageText(player.x, player.y - 45, "공격 범위 증가! 🧪", "#059669");
        }} else if (selectedClass.id === "ARCHER") {{
          player.bounces += 1;
          addDamageText(player.x, player.y - 45, "굴절 횟수 +1회! ⚡", "#d97706");
        }}
      }}

      // 레벨 30 도달 시 클리어
      if (level >= 30) {{
        gameState = "CLEAR";
        return;
      }}

      if (level % 5 === 0) {{
        player.maxHp += 50;
        player.hp = player.maxHp;
        gameState = "UPGRADE";
      }} else {{
        player.maxHp += 55;
        player.hp = player.maxHp;
        addDamageText(player.x, player.y - 25, `Lv.${{level}} 체력 회복! (+30 HP) 💖`, "#16a34a");
      }}
    }}
  }}
}}

function createHitParticles(x, y, color) {{
  for (let i = 0; i < 6; i++) {{
    particles.push({{
      x, y,
      vx: (Math.random() - 0.5) * 5,
      vy: (Math.random() - 0.5) * 5,
      life: 16,
      color
    }});
  }}
}}

function addDamageText(x, y, text, color) {{
  damageTexts.push({{ x, y, text, color, life: 28 }});
}}

let spawnTimer = 0;
let enemyIdCounter = 1;
function spawnEnemy() {{
  let x, y;
  if (Math.random() < 0.5) {{
    x = Math.random() < 0.5 ? -15 : canvas.width + 15;
    y = Math.random() * canvas.height;
  }} else {{
    x = Math.random() * canvas.width;
    y = Math.random() < 0.5 ? -15 : canvas.height + 15;
  }}

  const isBoss = Math.random() < 0.05 + (level * 0.015);
  enemies.push({{
    id: enemyIdCounter++,
    x, y,
    radius: isBoss ? 24 : 13,
    speed: isBoss ? 0.9 : (1.2 + Math.random() * 0.5),
    hp: isBoss ? 160 * (1 + level * 0.22) : 32 * (1 + level * 0.16),
    maxHp: isBoss ? 160 * (1 + level * 0.22) : 32 * (1 + level * 0.16),
    damage: isBoss ? 18 : 9,
    isBoss: isBoss,
    facingLeft: false,
    img: isBoss ? IMAGES.BOSS : IMAGES.ENEMY,
    color: isBoss ? "#e11d48" : "#f43f5e"
  }});
}}

function resetGame() {{
  gameState = "SELECT";
  selectUnlockTime = Date.now() + 500;
  selectedClass = null;
  score = 0;
  level = 1;
  exp = 0;
  expToNext = 50;
  enemies = [];
  attacks = [];
  mines = [];
  particles = [];
  damageTexts = [];
  slashEffects = [];
}}

// --- 메인 게임 루프 ---
function gameLoop() {{
  drawLabBackground();

  // 1. 학자 선택 화면
  if (gameState === "SELECT") {{
    ctx.fillStyle = "rgba(15, 23, 42, 0.82)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 23px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("⚛️ 물리학자 선택", canvas.width / 2, 60);

    ctx.fillStyle = "#94a3b8";
    ctx.font = "13px sans-serif";
    ctx.fillText("보라고등학교 실험실을 구할 물리학자를 터치하세요", canvas.width / 2, 95);

    const classes = [CLASSES.WARRIOR, CLASSES.ARCHER, CLASSES.MAGE];
    classes.forEach((cls, i) => {{
      const top = 140 + i * 130;
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = cls.color;
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      ctx.roundRect(25, top, canvas.width - 50, 115, 14);
      ctx.fill();
      ctx.stroke();

      const img = IMAGES[cls.id];
      if (img && img.src && img.complete && img.naturalWidth !== 0) {{
        ctx.drawImage(img, 40, top + 22, 70, 70);
      }} else {{
        ctx.font = "38px sans-serif";
        ctx.fillText(cls.icon, 70, top + 68);
      }}

      ctx.textAlign = "left";
      ctx.font = "bold 18px sans-serif";
      ctx.fillStyle = cls.color;
      ctx.fillText(cls.name, 125, top + 38);

      ctx.font = "bold 12px sans-serif";
      ctx.fillStyle = "#0284c7";
      ctx.fillText(cls.title, 125, top + 58);

      ctx.font = "11.5px sans-serif";
      ctx.fillStyle = "#475569";
      ctx.fillText(cls.desc, 125, top + 82);
    }});

    requestAnimationFrame(gameLoop);
    return;
  }}

  // 2. 특성 선택 팝업 (5레벨 단위)
  if (gameState === "UPGRADE") {{
    ctx.fillStyle = "rgba(15, 23, 42, 0.88)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#facc15";
    ctx.font = "bold 24px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(`🎉 Lv.${{level}} 달성! 특성 선택`, canvas.width / 2, 80);

    ctx.fillStyle = "#94a3b8";
    ctx.font = "13px sans-serif";
    ctx.fillText("강화할 능력을 선택하세요", canvas.width / 2, 115);

    const curSec = (player.baseCooldown / 60).toFixed(2);
    const options = [
      {{ id: "ATK", title: "⚔️ 공격력 증가", desc: "공격력 +60% 증가 (현재: " + player.atk + ")", color: "#ef4444" }},
      {{ id: "DEF", title: "🛡️ 방어력 증가", desc: "받는 피해 -30% 감소", color: "#3b82f6" }},
      {{ id: "SPD", title: "⚡ 공격 속도 증가", desc: "공격 주기 35% 단축 (현재: " + curSec + "초)", color: "#eab308" }}
    ];

    options.forEach((opt, i) => {{
      const top = 180 + i * 110;
      ctx.fillStyle = "#1e293b";
      ctx.strokeStyle = opt.color;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.roundRect(35, top, canvas.width - 70, 90, 12);
      ctx.fill();
      ctx.stroke();

      ctx.textAlign = "left";
      ctx.font = "bold 17px sans-serif";
      ctx.fillStyle = opt.color;
      ctx.fillText(opt.title, 55, top + 35);

      ctx.font = "12.5px sans-serif";
      ctx.fillStyle = "#e2e8f0";
      ctx.fillText(opt.desc, 55, top + 64);
    }});

    requestAnimationFrame(gameLoop);
    return;
  }}

  // 3. 인게임 루프
  if (gameState === "PLAYING") {{
    autoAttack();

    let moveX = 0, moveY = 0;
    if (keys['w'] || keys['arrowup']) moveY -= 1;
    if (keys['s'] || keys['arrowdown']) moveY += 1;
    if (keys['a'] || keys['arrowleft']) moveX -= 1;
    if (keys['d'] || keys['arrowright']) moveX += 1;

    // PC 이동 속도 (pcSpeedBoost 가속 적용)
    if (moveX !== 0 || moveY !== 0) {{
      let len = Math.hypot(moveX, moveY);
      const effectiveSpeed = player.speed * pcSpeedBoost;
      player.x += (moveX / len) * effectiveSpeed;
      player.y += (moveY / len) * effectiveSpeed;
      if (moveX !== 0) player.facingLeft = (moveX < 0);
    }} else if (joystick.active && (joystick.dx !== 0 || joystick.dy !== 0)) {{
      const mobileSpeed = player.speed * 0.70;
      player.x += joystick.dx * mobileSpeed;
      player.y += joystick.dy * mobileSpeed;
    }}

    player.x = Math.max(player.radius, Math.min(canvas.width - player.radius, player.x));
    player.y = Math.max(player.radius, Math.min(canvas.height - player.radius, player.y));

    spawnTimer++;
    if (spawnTimer > Math.max(22, 70 - level * 3)) {{
      spawnEnemy();
      spawnTimer = 0;
    }}

    // 아인슈타인 투사체
    for (let i = attacks.length - 1; i >= 0; i--) {{
      let atk = attacks[i];
      atk.x += atk.vx;
      atk.y += atk.vy;
      atk.travelled += Math.hypot(atk.vx, atk.vy);

      let bouncedWall = false;
      if (atk.x <= atk.radius || atk.x >= canvas.width - atk.radius) {{
        atk.vx = -atk.vx;
        bouncedWall = true;
      }}
      if (atk.y <= atk.radius || atk.y >= canvas.height - atk.radius) {{
        atk.vy = -atk.vy;
        bouncedWall = true;
      }}
      if (bouncedWall) {{
        atk.bouncesLeft--;
        createHitParticles(atk.x, atk.y, "#fef08a");
        if (atk.bouncesLeft < 0) {{
          attacks.splice(i, 1);
          continue;
        }}
      }}

      let hitEnemy = false;
      for (let j = enemies.length - 1; j >= 0; j--) {{
        let e = enemies[j];
        if (atk.lastHitEnemyId !== e.id && Math.hypot(atk.x - e.x, atk.y - e.y) < atk.radius + e.radius) {{
          applyDamage(e, atk.damage, j);
          createHitParticles(atk.x, atk.y, "#f59e0b");
          atk.lastHitEnemyId = e.id;
          atk.bouncesLeft--;
          hitEnemy = true;

          if (atk.bouncesLeft >= 0) {{
            let nextEnemy = null;
            let minDist = 9999;
            enemies.forEach(other => {{
              if (other.id !== e.id) {{
                let d = Math.hypot(other.x - atk.x, other.y - atk.y);
                if (d < minDist) {{
                  minDist = d;
                  nextEnemy = other;
                }}
              }}
            }});

            const speed = Math.hypot(atk.vx, atk.vy);
            if (nextEnemy) {{
              let angle = Math.atan2(nextEnemy.y - atk.y, nextEnemy.x - atk.x);
              atk.vx = Math.cos(angle) * speed;
              atk.vy = Math.sin(angle) * speed;
            }} else {{
              let randAngle = Math.random() * Math.PI * 2;
              atk.vx = Math.cos(randAngle) * speed;
              atk.vy = Math.sin(randAngle) * speed;
            }}
          }} else {{
            attacks.splice(i, 1);
          }}
          break;
        }}
      }}

      if (hitEnemy) continue;
      if (atk.travelled >= atk.maxDist) attacks.splice(i, 1);
    }}

    // 뉴턴 회전 참격
    for (let i = slashEffects.length - 1; i >= 0; i--) {{
      let s = slashEffects[i];
      s.life--;
      s.progress = 1 - (s.life / s.maxLife);

      const currentSlashAngle = s.baseAngle - Math.PI / 2.5 + (s.progress * Math.PI * 0.8);

      enemies.forEach((e, idx) => {{
        if (!s.hitEnemies.has(e.id)) {{
          let d = Math.hypot(e.x - s.x, e.y - s.y);
          if (d <= s.range + e.radius) {{
            let eAngle = Math.atan2(e.y - s.y, e.x - s.x);
            let diff = Math.abs(currentSlashAngle - eAngle);
            if (diff > Math.PI) diff = 2 * Math.PI - diff;

            if (diff < 0.6) {{
              s.hitEnemies.add(e.id);
              applyDamage(e, player.atk * (0.9 + Math.random() * 0.25), idx);
              createHitParticles(e.x, e.y, "#ef4444");
            }}
          }}
        }}
      }});

      if (s.life <= 0) slashEffects.splice(i, 1);
    }}

    // 퀴리 라듐 지뢰
    for (let i = mines.length - 1; i >= 0; i--) {{
      let m = mines[i];
      m.timer--;
      m.pulse += 0.1;

      let shouldExplode = false;
      if (m.timer <= 0) {{
        shouldExplode = true;
      }} else {{
        for (let j = 0; j < enemies.length; j++) {{
          let e = enemies[j];
          if (Math.hypot(m.x - e.x, m.y - e.y) < m.radius + e.radius) {{
            shouldExplode = true;
            break;
          }}
        }}
      }}

      if (shouldExplode) {{
        triggerGreenExplosion(m.x, m.y, m.explosionRadius, m.damage);
        mines.splice(i, 1);
      }}
    }}

    // 몬스터 AI & 속도 (PC 환경 1.4배 쾌적 가속)
    const enemySpeedMultiplier = isMobileDevice ? 1.0 : 1.40;
    for (let i = enemies.length - 1; i >= 0; i--) {{
      let e = enemies[i];
      let angle = Math.atan2(player.y - e.y, player.x - e.x);
      const moveDist = e.speed * enemySpeedMultiplier;
      e.x += Math.cos(angle) * moveDist;
      e.y += Math.sin(angle) * moveDist;

      e.facingLeft = (player.x < e.x);

      if (Math.hypot(player.x - e.x, player.y - e.y) < player.radius + e.radius) {{
        player.hp -= (e.damage * selectedClass.def) * 0.05;
        if (player.hp <= 0) {{
          player.hp = 0;
          gameState = "GAMEOVER";
        }}
      }}
    }}
  }}

  function triggerGreenExplosion(x, y, radius, damage) {{
    createHitParticles(x, y, "#10b981");
    for (let i = 0; i < 18; i++) {{
      particles.push({{
        x, y,
        vx: (Math.random() - 0.5) * 9,
        vy: (Math.random() - 0.5) * 9,
        life: 24,
        color: Math.random() < 0.5 ? "#059669" : "#34d399"
      }});
    }}
    enemies.forEach((e, idx) => {{
      if (Math.hypot(e.x - x, e.y - y) <= radius + e.radius) {{
        applyDamage(e, damage, idx);
      }}
    }});
  }}

  // 1. 뉴턴 참격 렌더링
  slashEffects.forEach(s => {{
    const startAngle = s.baseAngle - Math.PI / 2.5;
    const currentAngle = startAngle + (s.progress * Math.PI * 0.85);

    ctx.save();
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.range, startAngle, currentAngle);
    ctx.strokeStyle = "rgba(239, 68, 68, 0.85)";
    ctx.lineWidth = 10;
    ctx.shadowBlur = 15;
    ctx.shadowColor = "#fca5a5";
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(s.x, s.y, s.range - 6, startAngle, currentAngle);
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 3;
    ctx.stroke();
    ctx.restore();
  }});

  // 2. 라듐 지뢰 (증가된 접촉/감지 원형 크기 반영)
  mines.forEach(m => {{
    const pulseScale = 1 + Math.sin(m.pulse) * 0.2;
    ctx.beginPath();
    ctx.arc(m.x, m.y, m.radius * pulseScale * 1.6, 0, Math.PI * 2);
    ctx.strokeStyle = "rgba(16, 185, 129, 0.4)";
    ctx.lineWidth = 1.5;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(m.x, m.y, m.radius * pulseScale, 0, Math.PI * 2);
    ctx.fillStyle = "#10b981";
    ctx.shadowBlur = 12;
    ctx.shadowColor = "#34d399";
    ctx.fill();
    ctx.shadowBlur = 0;

    ctx.beginPath();
    ctx.arc(m.x, m.y, 4, 0, Math.PI * 2);
    ctx.fillStyle = "#ffffff";
    ctx.fill();
  }});

  // 3. 광자 화살
  attacks.forEach(atk => {{
    ctx.beginPath();
    ctx.arc(atk.x, atk.y, atk.radius + (atk.bouncesLeft > 0 ? 1 : 0), 0, Math.PI * 2);
    ctx.fillStyle = "#facc15";
    ctx.shadowBlur = 10;
    ctx.shadowColor = "#fef08a";
    ctx.fill();
    ctx.shadowBlur = 0;
  }});

  // 4. 적
  enemies.forEach(e => {{
    drawEntityWithFlip(e.img, e.x, e.y, e.radius, e.color, e.facingLeft);

    const bw = e.radius * 2;
    ctx.fillStyle = "#94a3b8";
    ctx.fillRect(e.x - e.radius, e.y - e.radius - 8, bw, 4);
    ctx.fillStyle = "#e11d48";
    ctx.fillRect(e.x - e.radius, e.y - e.radius - 8, bw * (e.hp / e.maxHp), 4);
  }});

  // 5. 파티클
  for (let i = particles.length - 1; i >= 0; i--) {{
    let pt = particles[i];
    pt.x += pt.vx;
    pt.y += pt.vy;
    pt.life--;
    ctx.fillStyle = pt.color;
    ctx.fillRect(pt.x, pt.y, 3, 3);
    if (pt.life <= 0) particles.splice(i, 1);
  }}

  // 6. 데미지 텍스트
  for (let i = damageTexts.length - 1; i >= 0; i--) {{
    let dt = damageTexts[i];
    dt.y -= 0.6;
    dt.life--;
    ctx.font = "bold 13px sans-serif";
    ctx.fillStyle = dt.color;
    ctx.fillText(dt.text, dt.x - 8, dt.y);
    if (dt.life <= 0) damageTexts.splice(i, 1);
  }}

  // 7. 플레이어
  if (selectedClass) {{
    const playerImg = IMAGES[selectedClass.id];
    drawEntityWithFlip(playerImg, player.x, player.y, player.radius, selectedClass.color, player.facingLeft);
  }}

  // 8. HUD
  ctx.fillStyle = "#334155";
  ctx.fillRect(10, 10, 130, 18);
  ctx.fillStyle = "#16a34a";
  ctx.fillRect(10, 10, 130 * (player.hp / player.maxHp), 18);
  ctx.strokeStyle = "#0f172a";
  ctx.lineWidth = 1.5;
  ctx.strokeRect(10, 10, 130, 18);
  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 11px sans-serif";
  ctx.textAlign = "left";
  ctx.fillText(`HP ${{Math.ceil(player.hp)}} / ${{player.maxHp}}`, 16, 23);

  // EXP Bar
  ctx.fillStyle = "#cbd5e1";
  ctx.fillRect(0, 0, canvas.width, 5);
  ctx.fillStyle = "#d97706";
  ctx.fillRect(0, 0, canvas.width * (exp / expToNext), 5);

  ctx.font = "bold 14px sans-serif";
  ctx.fillStyle = "#0f172a";
  ctx.textAlign = "right";
  ctx.fillText(`Lv.${{level}} / 30 | ${{score}}점`, canvas.width - 12, 24);

  // 9. 게임오버 화면
  if (gameState === "GAMEOVER") {{
    ctx.fillStyle = "rgba(15, 23, 42, 0.88)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#ef4444";
    ctx.font = "bold 34px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("EXPERIMENT FAILED", canvas.width / 2, canvas.height / 2 - 20);

    ctx.fillStyle = "#ffffff";
    ctx.font = "15px sans-serif";
    ctx.fillText(`최종 점수: ${{score}}점 (Lv.${{level}})`, canvas.width / 2, canvas.height / 2 + 18);

    ctx.fillStyle = "#38bdf8";
    ctx.fillText("화면을 터치하거나 [R] 키로 다시 시작", canvas.width / 2, canvas.height / 2 + 55);
  }}

  // 10. 게임 클리어 화면 (Lv.30 클리어)
  if (gameState === "CLEAR") {{
    ctx.fillStyle = "rgba(15, 23, 42, 0.9)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#22c55e";
    ctx.font = "bold 34px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("EXPERIMENT SUCCESS!", canvas.width / 2, canvas.height / 2 - 30);

    ctx.fillStyle = "#facc15";
    ctx.font = "bold 20px sans-serif";
    ctx.fillText("🏆 물리학의 위대한 승리 (Lv.30 도달) 🏆", canvas.width / 2, canvas.height / 2 + 10);

    ctx.fillStyle = "#ffffff";
    ctx.font = "16px sans-serif";
    ctx.fillText(`최종 실험 점수: ${{score}}점`, canvas.width / 2, canvas.height / 2 + 45);

    ctx.fillStyle = "#38bdf8";
    ctx.font = "14px sans-serif";
    ctx.fillText("화면을 터치하거나 [R] 키로 새로운 실험 시작", canvas.width / 2, canvas.height / 2 + 85);
  }}

  requestAnimationFrame(gameLoop);
}}

requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

components.html(game_html, height=750)
