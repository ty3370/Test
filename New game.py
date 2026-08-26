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
  /* 하단 컨트롤 패널 */
  #touchControls {{
    position: relative;
    width: 100%;
    height: 155px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 6px;
  }}
  /* 좌측 절반 전체를 차지하는 유연한 이동 터치 영역 */
  #moveTouchArea {{
    position: absolute;
    left: 0;
    top: 0;
    width: 60%;
    height: 100%;
    z-index: 10;
  }}
  /* 동적 플로팅 조이스틱 (터치 시 해당 위치로 이동) */
  #joystickZone {{
    position: absolute;
    width: 120px;
    height: 120px;
    background: rgba(255, 255, 255, 0.18);
    border: 3px solid rgba(255, 255, 255, 0.5);
    border-radius: 50%;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
    display: none; /* 터치 전 숨김 */
    pointer-events: none;
    transform: translate(-50%, -50%);
  }}
  #joystickKnob {{
    position: absolute;
    top: 50%;
    left: 50%;
    width: 54px;
    height: 54px;
    margin-top: -27px;
    margin-left: -27px;
    background: radial-gradient(circle, #ffffff 35%, #94a3b8 100%);
    border-radius: 50%;
    pointer-events: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }}
  /* 우측 공격 버튼 */
  #attackBtn {{
    position: absolute;
    right: 20px;
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

// --- 이미지 스프라이트 로드 ---
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

// --- 과학실 배경 요소 ---
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

// --- 클래스 정의 ---
const CLASSES = {{
  WARRIOR: {{
    id: "WARRIOR",
    name: "아이작 뉴턴",
    title: "중력과 만유인력",
    desc: "사과 참격 / 강력한 질량(공격·방어력 최고)",
    icon: "🍎",
    color: "#2563eb",
    maxHp: 190,
    atk: 46,
    def: 0.5,
    speed: 3.3,
    range: 75,
    cooldown: 18
  }},
  ARCHER: {{
    id: "ARCHER",
    name: "알베르트 아인슈타인",
    title: "상대성 이론과 광자",
    desc: "빛의 화살 / 초고속 원거리 광선 공격",
    icon: "⚡",
    color: "#d97706",
    maxHp: 90,
    atk: 32,
    def: 1.0,
    speed: 3.8,
    range: 480,
    cooldown: 16
  }},
  MAGE: {{
    id: "MAGE",
    name: "마리 퀴리",
    title: "방사능과 라듐 연구",
    desc: "라듐 구체 / 광역 방사성 폭발 데미지",
    icon: "🧪",
    color: "#059669",
    maxHp: 85,
    atk: 36,
    def: 1.1,
    speed: 3.3,
    range: 220,
    explosionRadius: 75,
    cooldown: 25
  }}
}};

let selectedClass = null;
let gameState = "SELECT";

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
  speed: 3.5,
  attackCooldown: 0
}};

const keys = {{}};
let mouse = {{ x: 210, y: 290 }};

// 플로팅 조이스틱 상태
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
let enemies = [];
let particles = [];
let damageTexts = [];
let slashEffects = [];

// --- PC 이벤트 바인딩 ---
window.addEventListener("keydown", e => {{
  keys[e.key.toLowerCase()] = true;
  if (gameState === "GAMEOVER" && e.key.toLowerCase() === "r") resetGame();
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
  if (gameState === "SELECT") handleClassSelectClick(coords.x, coords.y);
  else if (gameState === "PLAYING") {{
    player.facingAngle = Math.atan2(coords.y - player.y, coords.x - player.x);
    player.facingLeft = (coords.x < player.x);
    performAttack(player.facingAngle);
  }} else if (gameState === "GAMEOVER") resetGame();
}});

// ==========================================
// 스마트폰 플로팅(동적) 조이스틱 시스템
// ==========================================
const moveTouchArea = document.getElementById("moveTouchArea");
const joyZone = document.getElementById("joystickZone");
const joyKnob = document.getElementById("joystickKnob");
const attackBtn = document.getElementById("attackBtn");

// 1. 좌측 화면 아무 데나 터치하면 그 위치에 조이스틱 중심 생성
moveTouchArea.addEventListener("touchstart", e => {{
  e.preventDefault();
  if (joystick.active) return;

  const touch = e.changedTouches[0];
  const areaRect = moveTouchArea.getBoundingClientRect();
  
  joystick.active = true;
  joystick.touchId = touch.identifier;
  joystick.startX = touch.clientX;
  joystick.startY = touch.clientY;

  // 조이스틱 UI를 터치한 좌표로 순간 이동 후 표시
  const relativeX = touch.clientX - areaRect.left;
  const relativeY = touch.clientY - areaRect.top;
  joyZone.style.left = `${{relativeX}}px`;
  joyZone.style.top = `${{relativeY}}px`;
  joyZone.style.display = "block";
  joyKnob.style.transform = "translate(0px, 0px)";

  updateFloatingJoystick(touch.clientX, touch.clientY);
}}, {{ passive: false }});

// 2. 화면 전역에서 터치 이동 감지 (화면 밖으로 손가락이 나가도 유지)
window.addEventListener("touchmove", e => {{
  if (!joystick.active) return;
  for (let i = 0; i < e.touches.length; i++) {{
    if (e.touches[i].identifier === joystick.touchId) {{
      updateFloatingJoystick(e.touches[i].clientX, e.touches[i].clientY);
      break;
    }}
  }}
}}, {{ passive: false }});

// 3. 터치 종료 시 조이스틱 숨김 및 정지
function endTouch(e) {{
  if (!joystick.active) return;
  for (let i = 0; i < e.changedTouches.length; i++) {{
    if (e.changedTouches[i].identifier === joystick.touchId) {{
      joystick.active = false;
      joystick.touchId = null;
      joystick.dx = 0;
      joystick.dy = 0;
      joyZone.style.display = "none";
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
  const maxR = 48; // 최대 당김 반경

  if (dist > maxR) {{
    diffX = (diffX / dist) * maxR;
    diffY = (diffY / dist) * maxR;
  }}

  // 조이스틱 노브 이동
  joyKnob.style.transform = `translate(${{diffX}}px, ${{diffY}}px)`;

  // 플레이어 이동 벡터 정규화
  joystick.dx = diffX / maxR;
  joystick.dy = diffY / maxR;

  if (dist > 5) {{
    player.facingAngle = Math.atan2(diffY, diffX);
    player.facingLeft = (diffX < 0);
  }}
}}

// 공격 버튼
attackBtn.addEventListener("touchstart", e => {{ e.preventDefault(); performAttack(); }}, {{ passive: false }});
attackBtn.addEventListener("click", () => performAttack());

canvas.addEventListener("touchstart", e => {{
  const coords = getCanvasCoords(e.touches[0].clientX, e.touches[0].clientY);
  if (gameState === "SELECT") handleClassSelectClick(coords.x, coords.y);
  else if (gameState === "GAMEOVER") resetGame();
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
          createHitParticles(e.x, e.y, "#38bdf8");
        }}
      }}
    }});
  }} else if (selectedClass.id === "ARCHER") {{
    attacks.push({{
      type: "ARROW",
      x: player.x,
      y: player.y,
      vx: Math.cos(targetAngle) * 9.2,
      vy: Math.sin(targetAngle) * 9.2,
      damage: player.atk,
      travelled: 0,
      maxDist: selectedClass.range,
      radius: 4
    }});
  }} else if (selectedClass.id === "MAGE") {{
    attacks.push({{
      type: "GREEN_ORB",
      x: player.x,
      y: player.y,
      vx: Math.cos(targetAngle) * 5.4,
      vy: Math.sin(targetAngle) * 5.4,
      damage: player.atk,
      travelled: 0,
      maxDist: selectedClass.range,
      radius: 8,
      explosionRadius: selectedClass.explosionRadius
    }});
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
      player.maxHp += (selectedClass.id === "WARRIOR" ? 25 : 12);
      player.hp = player.maxHp;
      player.atk += (selectedClass.id === "WARRIOR" ? 8 : 5);
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
    x, y,
    radius: isBoss ? 24 : 13,
    speed: isBoss ? 1.0 : (1.4 + Math.random() * 0.6),
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
  selectedClass = null;
  score = 0;
  level = 1;
  exp = 0;
  expToNext = 60;
  enemies = [];
  attacks = [];
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
    }}

    // 플로팅 조이스틱 이동
    if (joystick.active) {{
      player.x += joystick.dx * player.speed;
      player.y += joystick.dy * player.speed;
      if (Math.abs(joystick.dx) > 0.05) player.facingLeft = (joystick.dx < 0);
    }}

    player.x = Math.max(player.radius, Math.min(canvas.width - player.radius, player.x));
    player.y = Math.max(player.radius, Math.min(canvas.height - player.radius, player.y));

    spawnTimer++;
    if (spawnTimer > Math.max(25, 70 - level * 4)) {{
      spawnEnemy();
      spawnTimer = 0;
    }}

    for (let i = attacks.length - 1; i >= 0; i--) {{
      let atk = attacks[i];
      atk.x += atk.vx;
      atk.y += atk.vy;
      atk.travelled += Math.hypot(atk.vx, atk.vy);

      if (atk.travelled >= atk.maxDist || atk.x < 0 || atk.x > canvas.width || atk.y < 0 || atk.y > canvas.height) {{
        if (atk.type === "GREEN_ORB") triggerGreenExplosion(atk.x, atk.y, atk.explosionRadius, atk.damage);
        attacks.splice(i, 1);
        continue;
      }}

      for (let j = enemies.length - 1; j >= 0; j--) {{
        let e = enemies[j];
        if (Math.hypot(atk.x - e.x, atk.y - e.y) < atk.radius + e.radius) {{
          if (atk.type === "ARROW") {{
            applyDamage(e, atk.damage, j);
            createHitParticles(atk.x, atk.y, "#f59e0b");
            attacks.splice(i, 1);
            break;
          }} else if (atk.type === "GREEN_ORB") {{
            triggerGreenExplosion(atk.x, atk.y, atk.explosionRadius, atk.damage);
            attacks.splice(i, 1);
            break;
          }}
        }}
      }}
    }}

    for (let i = enemies.length - 1; i >= 0; i--) {{
      let e = enemies[i];
      let angle = Math.atan2(player.y - e.y, player.x - e.x);
      e.x += Math.cos(angle) * e.speed;
      e.y += Math.sin(angle) * e.speed;

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
    for (let i = 0; i < 15; i++) {{
      particles.push({{
        x, y,
        vx: (Math.random() - 0.5) * 8,
        vy: (Math.random() - 0.5) * 8,
        life: 22,
        color: Math.random() < 0.5 ? "#059669" : "#34d399"
      }});
    }}
    enemies.forEach((e, idx) => {{
      if (Math.hypot(e.x - x, e.y - y) <= radius + e.radius) {{
        applyDamage(e, damage, idx);
      }}
    }});
  }}

  for (let i = slashEffects.length - 1; i >= 0; i--) {{
    let s = slashEffects[i];
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.range, s.angle - Math.PI / 3, s.angle + Math.PI / 3);
    ctx.strokeStyle = `rgba(37, 99, 235, ${{s.life / 10}})`;
    ctx.lineWidth = 7;
    ctx.stroke();
    s.life--;
    if (s.life <= 0) slashEffects.splice(i, 1);
  }}

  attacks.forEach(atk => {{
    ctx.beginPath();
    ctx.arc(atk.x, atk.y, atk.radius, 0, Math.PI * 2);
    ctx.fillStyle = atk.type === "ARROW" ? "#d97706" : "#059669";
    ctx.shadowBlur = 8;
    ctx.shadowColor = ctx.fillStyle;
    ctx.fill();
    ctx.shadowBlur = 0;
  }});

  enemies.forEach(e => {{
    drawEntityWithFlip(e.img, e.x, e.y, e.radius, e.color, e.facingLeft);

    const bw = e.radius * 2;
    ctx.fillStyle = "#94a3b8";
    ctx.fillRect(e.x - e.radius, e.y - e.radius - 8, bw, 4);
    ctx.fillStyle = "#e11d48";
    ctx.fillRect(e.x - e.radius, e.y - e.radius - 8, bw * (e.hp / e.maxHp), 4);
  }});

  for (let i = particles.length - 1; i >= 0; i--) {{
    let pt = particles[i];
    pt.x += pt.vx;
    pt.y += pt.vy;
    pt.life--;
    ctx.fillStyle = pt.color;
    ctx.fillRect(pt.x, pt.y, 3, 3);
    if (pt.life <= 0) particles.splice(i, 1);
  }}

  for (let i = damageTexts.length - 1; i >= 0; i--) {{
    let dt = damageTexts[i];
    dt.y -= 0.6;
    dt.life--;
    ctx.font = "bold 13px sans-serif";
    ctx.fillStyle = dt.color;
    ctx.fillText(dt.text, dt.x - 8, dt.y);
    if (dt.life <= 0) damageTexts.splice(i, 1);
  }}

  if (selectedClass) {{
    const playerImg = IMAGES[selectedClass.id];
    drawEntityWithFlip(playerImg, player.x, player.y, player.radius, selectedClass.color, player.facingLeft);
  }}

  // HUD
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

  if (gameState === "GAMEOVER") {{
    ctx.fillStyle = "rgba(15, 23, 42, 0.85)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#ef4444";
    ctx.font = "bold 34px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("EXPERIMENT FAILED", canvas.width / 2, canvas.height / 2 - 20);

    ctx.fillStyle = "#ffffff";
    ctx.font = "15px sans-serif";
    ctx.fillText(`최종 점수: ${{score}}점 (Lv.${{level}})`, canvas.width / 2, canvas.height / 2 + 18);
    ctx.fillText("화면을 터치하거나 [R] 키로 재시험", canvas.width / 2, canvas.height / 2 + 50);
  }}

  requestAnimationFrame(gameLoop);
}}

requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

components.html(game_html, height=755)
