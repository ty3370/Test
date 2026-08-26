import streamlit as st
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(
    page_title="2D 액션 RPG",
    page_icon="⚔️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        max-width: 520px;
    }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 이미지 파일을 Base64 데이터 URI로 변환하는 헬퍼 함수
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
    background: #0f111a;
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
    background: #181b22;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    width: 100%;
    aspect-ratio: 4 / 3.6;
    cursor: crosshair;
  }}
  #touchControls {{
    width: 100%;
    height: 125px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    margin-top: 6px;
  }}
  #joystickZone {{
    position: relative;
    width: 100px;
    height: 100px;
    background: rgba(255, 255, 255, 0.08);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 50%;
  }}
  #joystickKnob {{
    position: absolute;
    top: 27px;
    left: 27px;
    width: 46px;
    height: 46px;
    background: rgba(255, 255, 255, 0.5);
    border-radius: 50%;
    pointer-events: none;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
  }}
  #attackBtn {{
    width: 85px;
    height: 85px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ef4444, #b91c1c);
    border: 3px solid #fca5a5;
    color: white;
    font-size: 16px;
    font-weight: bold;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 4px 14px rgba(239, 68, 68, 0.5);
    cursor: pointer;
  }}
  #attackBtn:active {{
    transform: scale(0.92);
    background: linear-gradient(135deg, #dc2626, #991b1b);
  }}
</style>
</head>
<body>

<div id="gameWrapper">
  <canvas id="gameCanvas" width="440" height="380"></canvas>
  
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

// 좌우 반전(Flip) 지원 렌더링 함수 (기본 이미지가 오른쪽을 바라봄)
function drawEntityWithFlip(img, x, y, radius, fallbackColor, facingLeft = false, aimingAngle = null) {{
  ctx.save();
  ctx.translate(x, y);

  if (facingLeft) {{
    ctx.scale(-1, 1); // 왼쪽으로 이동/조준 시 좌우 대칭 반전
  }}

  if (img && img.src && img.complete && img.naturalWidth !== 0) {{
    const size = radius * 2.4;
    ctx.drawImage(img, -size / 2, -size / 2, size, size);
  }} else {{
    // 이미지 누락 시 기본 도형
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, Math.PI * 2);
    ctx.fillStyle = fallbackColor;
    ctx.shadowBlur = 8;
    ctx.shadowColor = fallbackColor;
    ctx.fill();
    ctx.shadowBlur = 0;
  }}
  ctx.restore();

  // 조준선(포인터) 렌더링
  if (aimingAngle !== null) {{
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x + Math.cos(aimingAngle) * (radius + 6), y + Math.sin(aimingAngle) * (radius + 6));
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 3;
    ctx.stroke();
  }}
}}

// --- 직업 설정 ---
const CLASSES = {{
  WARRIOR: {{
    id: "WARRIOR",
    name: "검사",
    desc: "근접 베기 / 강력한 공격력과 방어력",
    icon: "🗡️",
    color: "#3b82f6",
    maxHp: 180,
    atk: 45,
    def: 0.5,
    speed: 3.3,
    range: 70,
    cooldown: 18
  }},
  ARCHER: {{
    id: "ARCHER",
    name: "궁수",
    desc: "원거리 화살 / 긴 사거리, 약한 방어력",
    icon: "🏹",
    color: "#eab308",
    maxHp: 90,
    atk: 30,
    def: 1.0,
    speed: 3.8,
    range: 360,
    cooldown: 16
  }},
  MAGE: {{
    id: "MAGE",
    name: "마법사",
    desc: "초록빛 폭발 마법구 / 광역 데미지, 약한 방어력",
    icon: "🔮",
    color: "#10b981", // 에메랄드 초록색
    maxHp: 85,
    atk: 35,
    def: 1.1,
    speed: 3.3,
    range: 170,
    explosionRadius: 65,
    cooldown: 25
  }}
}};

let selectedClass = null;
let gameState = "SELECT";

const player = {{
  x: 220,
  y: 190,
  radius: 15,
  facingAngle: 0,
  facingLeft: false, // 좌우 시선 플래그
  hp: 100,
  maxHp: 100,
  atk: 30,
  def: 1.0,
  speed: 3.5,
  attackCooldown: 0
}};

const keys = {{}};
let mouse = {{ x: 220, y: 190 }};
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

// --- PC 입력 이벤트 ---
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
    // 마우스가 플레이어 좌측에 있으면 좌우 반전
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

// --- 모바일 터치 이벤트 ---
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
  const maxR = 32;

  if (dist > maxR) {{
    diffX = (diffX / dist) * maxR;
    diffY = (diffY / dist) * maxR;
  }}

  joystick.dx = diffX / maxR;
  joystick.dy = diffY / maxR;
  joyKnob.style.transform = `translate(${{diffX}}px, ${{diffY}}px)`;

  if (Math.hypot(diffX, diffY) > 4) {{
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
    const top = 75 + i * 90;
    if (x >= 25 && x <= canvas.width - 25 && y >= top && y <= top + 75) {{
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
      if (d < nearestDist && d < 240) {{
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
          createHitParticles(e.x, e.y, "#60a5fa");
        }}
      }}
    }});
  }} else if (selectedClass.id === "ARCHER") {{
    attacks.push({{
      type: "ARROW",
      x: player.x,
      y: player.y,
      vx: Math.cos(targetAngle) * 8.5,
      vy: Math.sin(targetAngle) * 8.5,
      damage: player.atk,
      travelled: 0,
      maxDist: selectedClass.range,
      radius: 4
    }});
  }} else if (selectedClass.id === "MAGE") {{
    // 마법사: 초록색 매직볼트
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
  addDamageText(enemy.x, enemy.y - 10, Math.round(amount), "#fff");

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
      addDamageText(player.x, player.y - 25, "LEVEL UP! ✨", "#facc15");
    }}
  }}
}}

function createHitParticles(x, y, color) {{
  for (let i = 0; i < 5; i++) {{
    particles.push({{
      x, y,
      vx: (Math.random() - 0.5) * 5,
      vy: (Math.random() - 0.5) * 5,
      life: 15,
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
    radius: isBoss ? 22 : 13,
    speed: isBoss ? 1.0 : (1.4 + Math.random() * 0.6),
    hp: isBoss ? 160 * (1 + level * 0.25) : 35 * (1 + level * 0.18),
    maxHp: isBoss ? 160 * (1 + level * 0.25) : 35 * (1 + level * 0.18),
    damage: isBoss ? 18 : 9,
    isBoss: isBoss,
    facingLeft: false, // 몬스터 좌우 방향
    img: isBoss ? IMAGES.BOSS : IMAGES.ENEMY,
    color: isBoss ? "#f43f5e" : "#fb7185"
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
  ctx.fillStyle = "#111827";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "#1f293d";
  ctx.lineWidth = 1;
  for (let x = 0; x < canvas.width; x += 30) {{
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
  }}
  for (let y = 0; y < canvas.height; y += 30) {{
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
  }}

  if (gameState === "SELECT") {{
    ctx.fillStyle = "rgba(0,0,0,0.4)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#f8fafc";
    ctx.font = "bold 20px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("클래스를 선택하세요", canvas.width / 2, 45);

    const classes = [CLASSES.WARRIOR, CLASSES.ARCHER, CLASSES.MAGE];
    classes.forEach((cls, i) => {{
      const top = 75 + i * 90;
      ctx.fillStyle = "#1e293b";
      ctx.strokeStyle = cls.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(25, top, canvas.width - 50, 75, 10);
      ctx.fill();
      ctx.stroke();

      const img = IMAGES[cls.id];
      if (img && img.src && img.complete && img.naturalWidth !== 0) {{
        ctx.drawImage(img, 40, top + 15, 45, 45);
      }} else {{
        ctx.font = "24px sans-serif";
        ctx.fillText(cls.icon, 55, top + 45);
      }}

      ctx.textAlign = "left";
      ctx.font = "bold 16px sans-serif";
      ctx.fillStyle = cls.color;
      ctx.fillText(cls.name, 95, top + 32);

      ctx.font = "11px sans-serif";
      ctx.fillStyle = "#94a3b8";
      ctx.fillText(cls.desc, 95, top + 54);
    }});

    requestAnimationFrame(gameLoop);
    return;
  }}

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
      if (moveX !== 0) {{
        player.facingLeft = (moveX < 0);
      }}
    }}

    if (joystick.active) {{
      player.x += joystick.dx * player.speed;
      player.y += joystick.dy * player.speed;
      if (Math.abs(joystick.dx) > 0.1) {{
        player.facingLeft = (joystick.dx < 0);
      }}
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
            createHitParticles(atk.x, atk.y, "#facc15");
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

    // 몬스터 AI & 시선 방향 업데이트
    for (let i = enemies.length - 1; i >= 0; i--) {{
      let e = enemies[i];
      let angle = Math.atan2(player.y - e.y, player.x - e.x);
      e.x += Math.cos(angle) * e.speed;
      e.y += Math.sin(angle) * e.speed;

      // 플레이어를 향해 몬스터 좌우 시선 변경
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

  // 마법사 초록색 폭발 이펙트
  function triggerGreenExplosion(x, y, radius, damage) {{
    createHitParticles(x, y, "#34d399");
    for (let i = 0; i < 14; i++) {{
      particles.push({{
        x, y,
        vx: (Math.random() - 0.5) * 8,
        vy: (Math.random() - 0.5) * 8,
        life: 22,
        color: Math.random() < 0.5 ? "#10b981" : "#a7f3d0"
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
    ctx.strokeStyle = `rgba(147, 197, 253, ${{s.life / 10}})`;
    ctx.lineWidth = 6;
    ctx.stroke();
    s.life--;
    if (s.life <= 0) slashEffects.splice(i, 1);
  }}

  // 2. 투사체 (궁수: 골드 화살 / 마법사: 에메랄드 초록 구체)
  attacks.forEach(atk => {{
    ctx.beginPath();
    ctx.arc(atk.x, atk.y, atk.radius, 0, Math.PI * 2);
    ctx.fillStyle = atk.type === "ARROW" ? "#facc15" : "#10b981";
    ctx.shadowBlur = 10;
    ctx.shadowColor = atk.type === "ARROW" ? "#fef08a" : "#6ee7b7";
    ctx.fill();
    ctx.shadowBlur = 0;
  }});

  // 3. 적 (이동 방향에 따라 좌우 반전)
  enemies.forEach(e => {{
    drawEntityWithFlip(e.img, e.x, e.y, e.radius, e.color, e.facingLeft);

    const bw = e.radius * 2;
    ctx.fillStyle = "#334155";
    ctx.fillRect(e.x - e.radius, e.y - e.radius - 6, bw, 3);
    ctx.fillStyle = "#ef4444";
    ctx.fillRect(e.x - e.radius, e.y - e.radius - 6, bw * (e.hp / e.maxHp), 3);
  }});

  // 4. 파티클
  for (let i = particles.length - 1; i >= 0; i--) {{
    let pt = particles[i];
    pt.x += pt.vx;
    pt.y += pt.vy;
    pt.life--;
    ctx.fillStyle = pt.color;
    ctx.fillRect(pt.x, pt.y, 2.5, 2.5);
    if (pt.life <= 0) particles.splice(i, 1);
  }}

  // 5. 데미지 텍스트
  for (let i = damageTexts.length - 1; i >= 0; i--) {{
    let dt = damageTexts[i];
    dt.y -= 0.6;
    dt.life--;
    ctx.font = "bold 11px sans-serif";
    ctx.fillStyle = dt.color;
    ctx.fillText(dt.text, dt.x - 8, dt.y);
    if (dt.life <= 0) damageTexts.splice(i, 1);
  }}

  // 6. 플레이어 (이동/조준 방향에 맞춰 좌우 반전 및 조준선 표시)
  if (selectedClass) {{
    const playerImg = IMAGES[selectedClass.id];
    drawEntityWithFlip(playerImg, player.x, player.y, player.radius, selectedClass.color, player.facingLeft, player.facingAngle);
  }}

  // 7. HUD
  ctx.fillStyle = "#1e293b";
  ctx.fillRect(10, 10, 110, 14);
  ctx.fillStyle = "#22c55e";
  ctx.fillRect(10, 10, 110 * (player.hp / player.maxHp), 14);
  ctx.strokeStyle = "#475569";
  ctx.strokeRect(10, 10, 110, 14);
  ctx.fillStyle = "#fff";
  ctx.font = "bold 9px sans-serif";
  ctx.textAlign = "left";
  ctx.fillText(`HP ${{Math.ceil(player.hp)}}/${{player.maxHp}}`, 14, 21);

  ctx.fillStyle = "#1e293b";
  ctx.fillRect(0, 0, canvas.width, 3);
  ctx.fillStyle = "#eab308";
  ctx.fillRect(0, 0, canvas.width * (exp / expToNext), 3);

  ctx.font = "bold 12px sans-serif";
  ctx.fillStyle = "#f8fafc";
  ctx.textAlign = "right";
  ctx.fillText(`Lv.${{level}} | ${{score}}점`, canvas.width - 10, 22);

  if (gameState === "GAMEOVER") {{
    ctx.fillStyle = "rgba(0,0,0,0.8)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#ef4444";
    ctx.font = "bold 30px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 20);

    ctx.fillStyle = "#f8fafc";
    ctx.font = "14px sans-serif";
    ctx.fillText(`최종 점수: ${{score}}점 (Lv.${{level}})`, canvas.width / 2, canvas.height / 2 + 15);
    ctx.fillText("클릭/터치 또는 [R] 키로 재시작", canvas.width / 2, canvas.height / 2 + 45);
  }}

  requestAnimationFrame(gameLoop);
}}

requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

components.html(game_html, height=540)
