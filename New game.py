import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(
    page_title="물리학자 던전 서바이벌",
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
    cursor: crosshair;
  }}
  #touchControls {{
    position: relative;
    width: 100%;
    height: 155px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 6px;
  }}
  #moveTouchArea {{
    position: absolute;
    left: 8px;
    top: 8px;
    width: 58%;
    height: 140px;
    background: rgba(30, 41, 59, 0.5);
    border: 2px dashed rgba(148, 163, 184, 0.45);
    border-radius: 18px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 10;
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
    font-size: 20px;
    letter-spacing: 4px;
    color: #38bdf8;
    margin-bottom: 2px;
  }}
  .guide-label {{
    font-size: 12px;
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
  #attackBtn {{
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    width: 115px;
    height: 115px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
    border: 4px solid #fecaca;
    color: white;
    font-size: 19px;
    font-weight: 900;
    letter-spacing: 1px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.6);
    cursor: pointer;
    z-index: 20;
  }}
  #attackBtn:active {{
    transform: translateY(-50%) scale(0.92);
    background: linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%);
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
        <div class="guide-label">터치 & 드래그로 이동</div>
      </div>
      <div id="joystickZone">
        <div id="joystickKnob"></div>
      </div>
    </div>
    <button id="attackBtn">ATTACK</button>
  </div>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// 환경 감지 (모바일 기기 여부)
const isMobileDevice = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

// --- 이미지 로드 ---
const IMAGES = {{
  WARRIOR: new Image(),
  ARCHER: new Image(),
  MAGE: new Image(),
  ENEMY: new Image(),
  BOSS: new Image()
}};

IMAGES.WARRIOR.src = "{img_warrior}";
IMAGES.ARCHER.src = "{img_archer}";
IMAGES.MAGE.src = "{img_mage}";
IMAGES.ENEMY.src = "{img_enemy}";
IMAGES.BOSS.src = "{img_boss}";

function drawEntityWithFlip(img, x, y, radius, fallbackColor, facingLeft = false) {{
  ctx.save();
  ctx.translate(x, y);

  if (facingLeft) {{
    ctx.scale(-1, 1);
  }}

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

// --- 클래스 밸런스 설정 ---
const CLASSES = {{
  WARRIOR: {{
    id: "WARRIOR",
    name: "아이작 뉴턴",
    title: "만유인력과 운동 법칙",
    desc: "사과 참격 / 사과 나무 휘두르기(근접, 방어력 우수)",
    icon: "🍎",
    color: "#dc2626",
    maxHp: 150,
    atk: 45,
    def: 0.8,
    speed: 2.6,
    range: 75,
    cooldown: 18
  }},
  ARCHER: {{
    id: "ARCHER",
    name: "알베르트 아인슈타인",
    title: "상대성 이론과 광자",
    desc: "광자 화살 / 적 및 벽에 최대 1회 튕기며 연속 타격",
    icon: "⚡",
    color: "#d97706",
    maxHp: 90,
    atk: 32,
    def: 1.0,
    speed: 3.1,
    range: 480,
    cooldown: 16
  }},
  MAGE: {{
    id: "MAGE",
    name: "마리 퀴리",
    title: "방사능과 라듐 연구",
    desc: "방사성 물질 지뢰 / 밟거나 시간 경과 시 광역 폭발",
    icon: "🧪",
    color: "#059669",
    maxHp: 85,
    atk: 48,
    def: 1.1,
    speed: 2.6,
    explosionRadius: 85,
    cooldown: 22
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
  speed: 2.6,
  attackCooldown: 0
}};

const keys = {{}};
let mouse = {{ x: 210, y: 290 }};

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
let expToNext = 60;

let attacks = [];
let mines = [];
let enemies = [];
let particles = [];
let damageTexts = [];
let slashEffects = [];

// --- PC 키보드 & 마우스 이벤트 ---
window.addEventListener("keydown", e => {{
  keys[e.key.toLowerCase()] = true;
  if (gameState === "GAMEOVER" && e.key.toLowerCase() === "r") {{
    resetGame();
  }}
  if (e.code === "Space") performAttack();
}});
window.addEventListener("keyup", e => {{ keys[e.key.toLowerCase()] = false; }});

function getCanvasCoords(clientX, clientY) {{
  const rect = canvas.getBoundingClientRect();
  return {{
    x: (clientX - rect.left) * (canvas.width / rect.width),
    y: (clientY - rect.top) * (canvas.height / rect.height)
  }};
}}

canvas.addEventListener("mousemove", e => {{
  const coords = getCanvasCoords(e.clientX, e.clientY);
  mouse.x = coords.x;
  mouse.y = coords.y;
  if (gameState === "PLAYING") {{
    player.facingAngle = Math.atan2(mouse.y - player.y, mouse.x - player.x);
    player.facingLeft = (mouse.x < player.x);
  }}
}});

canvas.addEventListener("mousedown", e => {{
  const coords = getCanvasCoords(e.clientX, e.clientY);
  if (gameState === "SELECT") {{
    if (Date.now() > selectUnlockTime) {{
      handleClassSelectClick(coords.x, coords.y);
    }}
  }} else if (gameState === "PLAYING") {{
    player.facingAngle = Math.atan2(coords.y - player.y, coords.x - player.x);
    player.facingLeft = (coords.x < player.x);
    performAttack(player.facingAngle);
  }} else if (gameState === "GAMEOVER") {{
    resetGame();
  }}
}});

// --- 모바일 플로팅 조이스틱 ---
const moveTouchArea = document.getElementById("moveTouchArea");
const moveGuide = document.getElementById("moveGuide");
const joyZone = document.getElementById("joystickZone");
const joyKnob = document.getElementById("joystickKnob");
const attackBtn = document.getElementById("attackBtn");

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

attackBtn.addEventListener("touchstart", e => {{ e.preventDefault(); performAttack(); }}, {{ passive: false }});
attackBtn.addEventListener("click", () => performAttack());

canvas.addEventListener("touchstart", e => {{
  const coords = getCanvasCoords(e.touches[0].clientX, e.touches[0].clientY);
  if (gameState === "SELECT") {{
    if (Date.now() > selectUnlockTime) {{
      handleClassSelectClick(coords.x, coords.y);
    }}
  }} else if (gameState === "GAMEOVER") {{
    resetGame();
  }}
}}, {{ passive: false }});

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
  player.facingAngle = 0;
  player.facingLeft = false;
  player.attackCooldown = 0;
  gameState = "PLAYING";
}}

// --- 공격 판정 ---
function performAttack(forcedAngle = null) {{
  if (gameState !== "PLAYING" || player.attackCooldown > 0) return;
  player.attackCooldown = selectedClass.cooldown;

  let targetAngle = forcedAngle !== null ? forcedAngle : player.facingAngle;

  if (forcedAngle === null && !keys[' ']) {{
    let nearestDist = 9999;
    let nearestEnemy = null;
    enemies.forEach(e => {{
      let d = Math.hypot(e.x - player.x, e.y - player.y);
      if (d < nearestDist && d < 300) {{
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
      angle: targetAngle,
      range: selectedClass.range,
      life: 10
    }});

    enemies.forEach((e, idx) => {{
      let d = Math.hypot(e.x - player.x, e.y - player.y);
      if (d <= selectedClass.range + e.radius) {{
        let enemyAngle = Math.atan2(e.y - player.y, e.x - player.x);
        let diff = Math.abs(targetAngle - enemyAngle);
        if (diff > Math.PI) diff = 2 * Math.PI - diff;
        if (diff < Math.PI / 2.2) {{
          applyDamage(e, player.atk * (0.9 + Math.random() * 0.3), idx);
          createHitParticles(e.x, e.y, "#ef4444");
        }}
      }}
    }});
  }} else if (selectedClass.id === "ARCHER") {{
    attacks.push({{
      type: "BOUNCE_ARROW",
      x: player.x,
      y: player.y,
      vx: Math.cos(targetAngle) * 8.5,
      vy: Math.sin(targetAngle) * 8.5,
      damage: player.atk,
      travelled: 0,
      maxDist: selectedClass.range,
      radius: 4,
      bouncesLeft: 1,
      lastHitEnemyId: null
    }});
  }} else if (selectedClass.id === "MAGE") {{
    mines.push({{
      x: player.x,
      y: player.y,
      radius: 12,
      damage: player.atk,
      explosionRadius: selectedClass.explosionRadius,
      timer: 180,
      pulse: 0
    }});
    createHitParticles(player.x, player.y, "#34d399");
  }}
}}

function applyDamage(enemy, amount, enemyIdx) {{
  enemy.hp -= amount;
  addDamageText(enemy.x, enemy.y - 12, Math.round(amount), "#dc2626");

  if (enemy.hp <= 0) {{
    let expGained = enemy.isBoss ? 70 : 25;
    exp += expGained;
    score += enemy.isBoss ? 250 : 80;
    createHitParticles(enemy.x, enemy.y, "#ef4444");
    enemies.splice(enemyIdx, 1);

    if (exp >= expToNext) {{
      exp -= expToNext;
      level++;
      expToNext = Math.round(expToNext * 1.35);
      player.maxHp += (selectedClass.id === "WARRIOR" ? 18 : 12);
      player.hp = player.maxHp;
      player.atk += (selectedClass.id === "WARRIOR" ? 7 : 5);
      addDamageText(player.x, player.y - 25, "LEVEL UP! 🌟", "#16a34a");
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
  damageTexts.push({{ x, y, text, color, life: 25 }});
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
    hp: isBoss ? 170 * (1 + level * 0.25) : 35 * (1 + level * 0.18),
    maxHp: isBoss ? 170 * (1 + level * 0.25) : 35 * (1 + level * 0.18),
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
  expToNext = 60;
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
    ctx.fillText("⚛️ 위대한 물리학자 선택", canvas.width / 2, 60);

    ctx.fillStyle = "#94a3b8";
    ctx.font = "13px sans-serif";
    ctx.fillText("실험실을 구할 학자를 터치하세요", canvas.width / 2, 95);

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

  // 2. 인게임 루프
  if (gameState === "PLAYING") {{
    if (player.attackCooldown > 0) player.attackCooldown--;

    let moveX = 0, moveY = 0;

    if (keys['w'] || keys['arrowup']) moveY -= 1;
    if (keys['s'] || keys['arrowdown']) moveY += 1;
    if (keys['a'] || keys['arrowleft']) moveX -= 1;
    if (keys['d'] || keys['arrowright']) moveX += 1;

    if (moveX !== 0 || moveY !== 0) {{
      let len = Math.hypot(moveX, moveY);
      player.x += (moveX / len) * player.speed;
      player.y += (moveY / len) * player.speed;
      if (moveX !== 0) player.facingLeft = (moveX < 0);
    }} else if (joystick.active && (joystick.dx !== 0 || joystick.dy !== 0)) {{
      const mobileSpeed = player.speed * 0.68;
      player.x += joystick.dx * mobileSpeed;
      player.y += joystick.dy * mobileSpeed;
    }}

    player.x = Math.max(player.radius, Math.min(canvas.width - player.radius, player.x));
    player.y = Math.max(player.radius, Math.min(canvas.height - player.radius, player.y));

    spawnTimer++;
    if (spawnTimer > Math.max(25, 70 - level * 4)) {{
      spawnEnemy();
      spawnTimer = 0;
    }}

    // 투사체 처리
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

      if (atk.travelled >= atk.maxDist) {{
        attacks.splice(i, 1);
      }}
    }}

    // 퀴리 라듐 지뢰 업데이트
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

    // 몬스터 AI & 속도 적용 (PC 환경에서만 1.45배 가속)
    const enemySpeedMultiplier = isMobileDevice ? 1.0 : 1.45;

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

  // 1. 뉴턴 참격
  for (let i = slashEffects.length - 1; i >= 0; i--) {{
    let s = slashEffects[i];
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.range, s.angle - Math.PI / 3, s.angle + Math.PI / 3);
    ctx.strokeStyle = `rgba(239, 68, 68, ${{s.life / 10}})`;
    ctx.lineWidth = 8;
    ctx.shadowBlur = 12;
    ctx.shadowColor = "#f87171";
    ctx.stroke();
    ctx.shadowBlur = 0;
    s.life--;
    if (s.life <= 0) slashEffects.splice(i, 1);
  }}

  // 2. 라듐 지뢰
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

  // 3. 광자 투사체
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

  ctx.fillStyle = "#cbd5e1";
  ctx.fillRect(0, 0, canvas.width, 4);
  ctx.fillStyle = "#d97706";
  ctx.fillRect(0, 0, canvas.width * (exp / expToNext), 4);

  ctx.font = "bold 14px sans-serif";
  ctx.fillStyle = "#0f172a";
  ctx.textAlign = "right";
  ctx.fillText(`Lv.${{level}} | ${{score}}점`, canvas.width - 12, 24);

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

  requestAnimationFrame(gameLoop);
}}

requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

components.html(game_html, height=755)
