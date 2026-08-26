import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(
    page_title="2D 액션 RPG - 과학실 던전",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 모바일 전체화면 반응형 스타일 주입
st.markdown("""
<style>
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0rem;
        padding-left: 0.2rem;
        padding-right: 0.2rem;
        max-width: 600px;
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

img_warrior = get_image_base64("assets/warrior.png")
img_archer  = get_image_base64("assets/archer.png")
img_mage    = get_image_base64("assets/mage.png")
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
    background: #1e293b;
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
    max-width: 560px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  canvas {{
    display: block;
    background: #cbd5e1;
    border: 3px solid #64748b;
    border-radius: 14px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.35);
    width: 100%;
    aspect-ratio: 4 / 3.4;
    cursor: crosshair;
  }}
  /* 스마트폰 전용 초대형 컨트롤러 */
  #touchControls {{
    width: 100%;
    height: 160px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 24px;
    margin-top: 8px;
  }}
  #joystickZone {{
    position: relative;
    width: 130px;
    height: 130px;
    background: rgba(255, 255, 255, 0.15);
    border: 3px solid rgba(255, 255, 255, 0.45);
    border-radius: 50%;
    box-shadow: inset 0 2px 10px rgba(0,0,0,0.25);
  }}
  #joystickKnob {{
    position: absolute;
    top: 35px;
    left: 35px;
    width: 60px;
    height: 60px;
    background: radial-gradient(circle, #ffffff 40%, #94a3b8 100%);
    border-radius: 50%;
    pointer-events: none;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }}
  #attackBtn {{
    width: 115px;
    height: 115px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
    border: 4px solid #fecaca;
    color: white;
    font-size: 20px;
    font-weight: 900;
    letter-spacing: 1px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.6);
    cursor: pointer;
  }}
  #attackBtn:active {{
    transform: scale(0.92);
    background: linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%);
  }}
</style>
</head>
<body>

<div id="gameWrapper">
  <canvas id="gameCanvas" width="480" height="400"></canvas>
  
  <div id="touchControls">
    <div id="joystickZone">
      <div id="joystickKnob"></div>
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

// 좌우 반전 지원 이미지 렌더링 함수 (조준선 완전 제거)
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
    // 이미지 파일 미존재 시 대비
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

// --- 과학실 배경 장식물 (플라스크, 비커, 시험관 등) ---
const labProps = [
  {{ x: 60, y: 70, type: "flask", color: "#38bdf8" }},
  {{ x: 420, y: 80, type: "beaker", color: "#4ade80" }},
  {{ x: 70, y: 340, type: "beaker", color: "#f472b6" }},
  {{ x: 410, y: 330, type: "flask", color: "#a855f7" }},
  {{ x: 240, y: 50, type: "gridDesk", color: "#94a3b8" }}
];

function drawLabBackground() {{
  // 1. 밝은 연구실 타일 바닥
  ctx.fillStyle = "#e2e8f0";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 2. 실험실 격자선
  ctx.strokeStyle = "#cbd5e1";
  ctx.lineWidth = 1.5;
  for (let x = 0; x < canvas.width; x += 40) {{
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
  }}
  for (let y = 0; y < canvas.height; y += 40) {{
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
  }}

  // 3. 실험대 / 타일 문양 디테일
  ctx.strokeStyle = "#94a3b8";
  ctx.lineWidth = 2;
  ctx.strokeRect(30, 30, canvas.width - 60, canvas.height - 60);

  // 4. 과학실 소품 (플라스크, 비커 등) 그리기
  labProps.forEach(prop => {{
    ctx.save();
    ctx.translate(prop.x, prop.y);
    if (prop.type === "flask") {{
      // 플라스크 밑바닥 & 시약
      ctx.beginPath();
      ctx.moveTo(-10, 10);
      ctx.lineTo(10, 10);
      ctx.lineTo(4, -4);
      ctx.lineTo(4, -12);
      ctx.lineTo(-4, -12);
      ctx.lineTo(-4, -4);
      ctx.closePath();
      ctx.fillStyle = prop.color;
      ctx.globalAlpha = 0.55;
      ctx.fill();
      ctx.globalAlpha = 1.0;
      ctx.strokeStyle = "#475569";
      ctx.lineWidth = 2;
      ctx.stroke();
    }} else if (prop.type === "beaker") {{
      // 비커
      ctx.beginPath();
      ctx.rect(-9, -10, 18, 20);
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

// --- 직업 정의 ---
const CLASSES = {{
  WARRIOR: {{
    id: "WARRIOR",
    name: "검사",
    desc: "근접 베기 / 강력한 공격력과 방어력",
    icon: "🗡️",
    color: "#2563eb",
    maxHp: 190,
    atk: 45,
    def: 0.5,
    speed: 3.3,
    range: 75,
    cooldown: 18
  }},
  ARCHER: {{
    id: "ARCHER",
    name: "궁수",
    desc: "원거리 화살 / 긴 사거리, 약한 방어력",
    icon: "🏹",
    color: "#d97706",
    maxHp: 90,
    atk: 32,
    def: 1.0,
    speed: 3.8,
    range: 380,
    cooldown: 16
  }},
  MAGE: {{
    id: "MAGE",
    name: "마법사",
    desc: "초록빛 화학 폭발구 / 광역 데미지",
    icon: "🧪",
    color: "#059669", // 실험실 에메랄드 그린
    maxHp: 85,
    atk: 36,
    def: 1.1,
    speed: 3.3,
    range: 175,
    explosionRadius: 70,
    cooldown: 25
  }}
}};

let selectedClass = null;
let gameState = "SELECT";

const player = {{
  x: 240,
  y: 200,
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
let mouse = {{ x: 240, y: 200 }};
let joystick = {{ active: false, startX: 0, startY: 0, dx: 0, dy: 0 }};

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

// --- 모바일 터치 이벤트 바인딩 (대형 조이스틱) ---
const joyZone = document.getElementById("joystickZone");
const joyKnob = document.getElementById("joystickKnob");
const attackBtn = document.getElementById("attackBtn");

joyZone.addEventListener("touchstart", e => {{
  e.preventDefault();
  const touch = e.touches[0];
  const rect = joyZone.getBoundingClientRect();
  joystick.active = true;
  joystick.startX = rect.left + rect.width / 2;
  joystick.startY = rect.top + rect.height / 2;
  updateJoystick(touch.clientX, touch.clientY);
}}, {{ passive: false }});

window.addEventListener("touchmove", e => {{
  if (!joystick.active) return;
  updateJoystick(e.touches[0].clientX, e.touches[0].clientY);
}}, {{ passive: false }});

window.addEventListener("touchend", () => {{
  if (joystick.active) {{
    joystick.active = false;
    joystick.dx = 0;
    joystick.dy = 0;
    joyKnob.style.transform = "translate(0px, 0px)";
  }}
}});

function updateJoystick(currentX, currentY) {{
  let diffX = currentX - joystick.startX;
  let diffY = currentY - joystick.startY;
  let dist = Math.hypot(diffX, diffY);
  const maxR = 45;

  if (dist > maxR) {{
    diffX = (diffX / dist) * maxR;
    diffY = (diffY / dist) * maxR;
  }}

  joystick.dx = diffX / maxR;
  joystick.dy = diffY / maxR;
  joyKnob.style.transform = `translate(${{diffX}}px, ${{diffY}}px)`;

  if (Math.hypot(diffX, diffY) > 5) {{
    player.facingAngle = Math.atan2(diffY, diffX);
    player.facingLeft = (diffX < 0);
  }}
}}

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
    const top = 80 + i * 95;
    if (x >= 25 && x <= canvas.width - 25 && y >= top && y <= top + 80) {{
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
      if (d < nearestDist && d < 260) {{
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
      vx: Math.cos(targetAngle) * 8.8,
      vy: Math.sin(targetAngle) * 8.8,
      damage: player.atk,
      travelled: 0,
      maxDist: selectedClass.range,
      radius: 4
    }});
  }} else if (selectedClass.id === "MAGE") {{
    // 마법사: 화학 시약 녹색 오브
    attacks.push({{
      type: "GREEN_ORB",
      x: player.x,
      y: player.y,
      vx: Math.cos(targetAngle) * 5.2,
      vy: Math.sin(targetAngle) * 5.2,
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
    radius: isBoss ? 23 : 13,
    speed: isBoss ? 1.0 : (1.4 + Math.random() * 0.6),
    hp: isBoss ? 160 * (1 + level * 0.25) : 35 * (1 + level * 0.18),
    maxHp: isBoss ? 160 * (1 + level * 0.25) : 35 * (1 + level * 0.18),
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

// --- 메인 루프 ---
function gameLoop() {{
  // 1. 과학실 배경 그리기
  drawLabBackground();

  // 클래스 선택 모드
  if (gameState === "SELECT") {{
    ctx.fillStyle = "rgba(15, 23, 42, 0.75)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#ffffff";
    ctx.font = "bold 22px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("🧪 연구원(클래스)을 선택하세요", canvas.width / 2, 48);

    const classes = [CLASSES.WARRIOR, CLASSES.ARCHER, CLASSES.MAGE];
    classes.forEach((cls, i) => {{
      const top = 80 + i * 95;
      ctx.fillStyle = "#ffffff";
      ctx.strokeStyle = cls.color;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.roundRect(25, top, canvas.width - 50, 80, 12);
      ctx.fill();
      ctx.stroke();

      const img = IMAGES[cls.id];
      if (img && img.src && img.complete && img.naturalWidth !== 0) {{
        ctx.drawImage(img, 40, top + 15, 50, 50);
      }} else {{
        ctx.font = "28px sans-serif";
        ctx.fillText(cls.icon, 55, top + 48);
      }}

      ctx.textAlign = "left";
      ctx.font = "bold 17px sans-serif";
      ctx.fillStyle = cls.color;
      ctx.fillText(cls.name, 105, top + 34);

      ctx.font = "12px sans-serif";
      ctx.fillStyle = "#475569";
      ctx.fillText(cls.desc, 105, top + 58);
    }});

    requestAnimationFrame(gameLoop);
    return;
  }}

  // 인게임 플레이 루프
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

    if (joystick.active) {{
      player.x += joystick.dx * player.speed;
      player.y += joystick.dy * player.speed;
      if (Math.abs(joystick.dx) > 0.1) player.facingLeft = (joystick.dx < 0);
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

  // 1. 검기
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

  // 2. 투사체
  attacks.forEach(atk => {{
    ctx.beginPath();
    ctx.arc(atk.x, atk.y, atk.radius, 0, Math.PI * 2);
    ctx.fillStyle = atk.type === "ARROW" ? "#d97706" : "#059669";
    ctx.shadowBlur = 8;
    ctx.shadowColor = ctx.fillStyle;
    ctx.fill();
    ctx.shadowBlur = 0;
  }});

  // 3. 적
  enemies.forEach(e => {{
    drawEntityWithFlip(e.img, e.x, e.y, e.radius, e.color, e.facingLeft);

    const bw = e.radius * 2;
    ctx.fillStyle = "#94a3b8";
    ctx.fillRect(e.x - e.radius, e.y - e.radius - 8, bw, 4);
    ctx.fillStyle = "#e11d48";
    ctx.fillRect(e.x - e.radius, e.y - e.radius - 8, bw * (e.hp / e.maxHp), 4);
  }});

  // 4. 파티클
  for (let i = particles.length - 1; i >= 0; i--) {{
    let pt = particles[i];
    pt.x += pt.vx;
    pt.y += pt.vy;
    pt.life--;
    ctx.fillStyle = pt.color;
    ctx.fillRect(pt.x, pt.y, 3, 3);
    if (pt.life <= 0) particles.splice(i, 1);
  }}

  // 5. 데미지 텍스트
  for (let i = damageTexts.length - 1; i >= 0; i--) {{
    let dt = damageTexts[i];
    dt.y -= 0.6;
    dt.life--;
    ctx.font = "bold 13px sans-serif";
    ctx.fillStyle = dt.color;
    ctx.fillText(dt.text, dt.x - 8, dt.y);
    if (dt.life <= 0) damageTexts.splice(i, 1);
  }}

  // 6. 플레이어 (조준선 없이 캐릭터 이미지만 깔끔하게 렌더링)
  if (selectedClass) {{
    const playerImg = IMAGES[selectedClass.id];
    drawEntityWithFlip(playerImg, player.x, player.y, player.radius, selectedClass.color, player.facingLeft);
  }}

  // 7. 선명한 상단 HUD
  // HP Bar
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

  // 상단 EXP Bar
  ctx.fillStyle = "#cbd5e1";
  ctx.fillRect(0, 0, canvas.width, 4);
  ctx.fillStyle = "#d97706";
  ctx.fillRect(0, 0, canvas.width * (exp / expToNext), 4);

  // 레벨 & 스코어
  ctx.font = "bold 14px sans-serif";
  ctx.fillStyle = "#0f172a";
  ctx.textAlign = "right";
  ctx.fillText(`Lv.${{level}} | ${{score}}점`, canvas.width - 12, 24);

  // 게임 오버
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

components.html(game_html, height=590)
