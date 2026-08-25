import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="모바일 액션 RPG",
    page_icon="⚔️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 모바일 화면에 맞춘 레이아웃 스타일 주입
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
        max-width: 500px;
    }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * {
    box-sizing: border-box;
    user-select: none;
    -webkit-user-select: none;
    touch-action: none;
  }
  body {
    margin: 0;
    padding: 0;
    background: #0f111a;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: 'Segoe UI', AppleSDGothicNeo-Regular, sans-serif;
    color: #fff;
    overflow: hidden;
  }
  #gameWrapper {
    position: relative;
    width: 100%;
    max-width: 440px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  canvas {
    display: block;
    background: #181b22;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    width: 100%;
    aspect-ratio: 4 / 3.8;
  }
  /* 모바일 가상 컨트롤러 영역 */
  #touchControls {
    width: 100%;
    height: 140px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    margin-top: 8px;
  }
  #joystickZone {
    position: relative;
    width: 110px;
    height: 110px;
    background: rgba(255, 255, 255, 0.08);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 50%;
  }
  #joystickKnob {
    position: absolute;
    top: 30px;
    left: 30px;
    width: 50px;
    height: 50px;
    background: rgba(255, 255, 255, 0.5);
    border-radius: 50%;
    pointer-events: none;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
  }
  #attackBtn {
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ef4444, #b91c1c);
    border: 3px solid #fca5a5;
    color: white;
    font-size: 18px;
    font-weight: bold;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 4px 14px rgba(239, 68, 68, 0.5);
    active: scale(0.95);
  }
  #attackBtn:active {
    transform: scale(0.92);
    background: linear-gradient(135deg, #dc2626, #991b1b);
  }
</style>
</head>
<body>

<div id="gameWrapper">
  <canvas id="gameCanvas" width="400" height="380"></canvas>
  
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

// --- 직업 정의 ---
const CLASSES = {
  WARRIOR: {
    id: "WARRIOR",
    name: "검사",
    desc: "근접 베기 / 강력한 공격력과 방어력",
    icon: "🗡️",
    color: "#3b82f6",
    maxHp: 180,
    atk: 45,
    def: 0.5, // 받는 피해 50%
    speed: 3.2,
    range: 65, // 근접 베기 반경
    cooldown: 20
  },
  ARCHER: {
    id: "ARCHER",
    name: "궁수",
    desc: "원거리 화살 / 긴 사거리, 약한 방어력",
    icon: "🏹",
    color: "#10b981",
    maxHp: 90,
    atk: 30,
    def: 1.0, // 받는 피해 100%
    speed: 3.8,
    range: 350,
    cooldown: 18
  },
  MAGE: {
    id: "MAGE",
    name: "마법사",
    desc: "범위 폭발 마법구 / 중간 사거리, 약한 방어력",
    icon: "🔮",
    color: "#a855f7",
    maxHp: 80,
    atk: 35,
    def: 1.1, // 받는 피해 110%
    speed: 3.3,
    range: 160, // 날아가는 거리
    explosionRadius: 65, // 착탄 폭발 범위
    cooldown: 28
  }
};

let selectedClass = null;
let gameState = "SELECT"; // "SELECT", "PLAYING", "GAMEOVER"

// --- 플레이어 및 엔티티 ---
const player = {
  x: 200,
  y: 190,
  radius: 14,
  facingAngle: 0,
  hp: 100,
  maxHp: 100,
  atk: 30,
  def: 1.0,
  speed: 3.5,
  attackCooldown: 0
};

let joystick = { active: false, startX: 0, startY: 0, dx: 0, dy: 0 };
let score = 0;
let level = 1;
let exp = 0;
let expToNext = 60;

let attacks = [];       // 화살, 마법구, 검기 이펙트
let enemies = [];
let particles = [];
let damageTexts = [];
let slashEffects = [];  // 검사용 베기 이펙트

// --- 조작 이벤트 바인딩 (조이스틱 & 공격) ---
const joyZone = document.getElementById("joystickZone");
const joyKnob = document.getElementById("joystickKnob");
const attackBtn = document.getElementById("attackBtn");

joyZone.addEventListener("touchstart", e => {
  e.preventDefault();
  const touch = e.touches[0];
  const rect = joyZone.getBoundingClientRect();
  joystick.active = true;
  joystick.startX = rect.left + rect.width / 2;
  joystick.startY = rect.top + rect.height / 2;
  updateJoystick(touch.clientX, touch.clientY);
}, { passive: false });

window.addEventListener("touchmove", e => {
  if (!joystick.active) return;
  const touch = e.touches[0];
  updateJoystick(touch.clientX, touch.clientY);
}, { passive: false });

window.addEventListener("touchend", e => {
  if (joystick.active) {
    joystick.active = false;
    joystick.dx = 0;
    joystick.dy = 0;
    joyKnob.style.transform = `translate(0px, 0px)`;
  }
});

function updateJoystick(currentX, currentY) {
  let diffX = currentX - joystick.startX;
  let diffY = currentY - joystick.startY;
  let dist = Math.hypot(diffX, diffY);
  const maxR = 35;

  if (dist > maxR) {
    diffX = (diffX / dist) * maxR;
    diffY = (diffY / dist) * maxR;
  }

  joystick.dx = diffX / maxR;
  joystick.dy = diffY / maxR;
  joyKnob.style.transform = `translate(${diffX}px, ${diffY}px)`;

  if (Math.hypot(diffX, diffY) > 5) {
    player.facingAngle = Math.atan2(diffY, diffX);
  }
}

// 터치 공격 버튼 이벤트
attackBtn.addEventListener("touchstart", e => {
  e.preventDefault();
  performAttack();
}, { passive: false });

// PC 키보드/마우스 호환용
window.addEventListener("keydown", e => {
  if (gameState === "GAMEOVER" && e.key.toLowerCase() === "r") resetGame();
  if (e.code === "Space") performAttack();
});

// 캔버스 터치 (직업 선택 & 재시작 처리)
canvas.addEventListener("touchstart", handleCanvasTouch, { passive: false });
canvas.addEventListener("mousedown", handleCanvasTouch);

function handleCanvasTouch(e) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  
  let clientX = e.touches ? e.touches[0].clientX : e.clientX;
  let clientY = e.touches ? e.touches[0].clientY : e.clientY;
  const x = (clientX - rect.left) * scaleX;
  const y = (clientY - rect.top) * scaleY;

  if (gameState === "SELECT") {
    // 직업 선택 카드 클릭 좌표 판정
    const cardH = 75;
    const startY = 85;
    const gap = 15;

    const classes = [CLASSES.WARRIOR, CLASSES.ARCHER, CLASSES.MAGE];
    classes.forEach((cls, i) => {
      const top = startY + i * (cardH + gap);
      if (x >= 25 && x <= canvas.width - 25 && y >= top && y <= top + cardH) {
        initPlayerWithClass(cls);
      }
    });
  } else if (gameState === "GAMEOVER") {
    resetGame();
  }
}

// --- 캐릭터 직업 초기화 ---
function initPlayerWithClass(cls) {
  selectedClass = cls;
  player.x = canvas.width / 2;
  player.y = canvas.height / 2;
  player.maxHp = cls.maxHp;
  player.hp = cls.maxHp;
  player.atk = cls.atk;
  player.def = cls.def;
  player.speed = cls.speed;
  player.facingAngle = 0;
  player.attackCooldown = 0;
  gameState = "PLAYING";
}

// --- 공격 실행 로직 ---
function performAttack() {
  if (gameState !== "PLAYING" || player.attackCooldown > 0) return;
  player.attackCooldown = selectedClass.cooldown;

  // 가장 가까운 적을 조준하거나 바라보는 방향으로 발사
  let targetAngle = player.facingAngle;
  let nearestDist = 9999;
  let nearestEnemy = null;

  enemies.forEach(e => {
    let d = Math.hypot(e.x - player.x, e.y - player.y);
    if (d < nearestDist && d < 220) {
      nearestDist = d;
      nearestEnemy = e;
    }
  });

  if (nearestEnemy) {
    targetAngle = Math.atan2(nearestEnemy.y - player.y, nearestEnemy.x - player.x);
    player.facingAngle = targetAngle;
  }

  if (selectedClass.id === "WARRIOR") {
    // 검사: 전방 부채꼴 근접 베기
    slashEffects.push({
      x: player.x,
      y: player.y,
      angle: targetAngle,
      range: selectedClass.range,
      life: 10
    });

    enemies.forEach((e, idx) => {
      let d = Math.hypot(e.x - player.x, e.y - player.y);
      if (d <= selectedClass.range + e.radius) {
        let enemyAngle = Math.atan2(e.y - player.y, e.x - player.x);
        let angleDiff = Math.abs(targetAngle - enemyAngle);
        if (angleDiff > Math.PI) angleDiff = 2 * Math.PI - angleDiff;

        if (angleDiff < Math.PI / 2.2) {
          applyDamage(e, player.atk * (0.9 + Math.random() * 0.3), idx);
          createHitParticles(e.x, e.y, "#60a5fa");
        }
      }
    });

  } else if (selectedClass.id === "ARCHER") {
    // 궁수: 고속 관통/원거리 화살
    attacks.push({
      type: "ARROW",
      x: player.x,
      y: player.y,
      vx: Math.cos(targetAngle) * 8.5,
      vy: Math.sin(targetAngle) * 8.5,
      damage: player.atk,
      travelled: 0,
      maxDist: selectedClass.range,
      radius: 4
    });

  } else if (selectedClass.id === "MAGE") {
    // 마법사: 비행 후 폭발 마법탄
    attacks.push({
      type: "FIREBALL",
      x: player.x,
      y: player.y,
      vx: Math.cos(targetAngle) * 4.8,
      vy: Math.sin(targetAngle) * 4.8,
      damage: player.atk,
      travelled: 0,
      maxDist: selectedClass.range,
      radius: 7,
      explosionRadius: selectedClass.explosionRadius
    });
  }
}

// 대미지 적용 및 몬스터 사망/경험치 처리
function applyDamage(enemy, amount, enemyIdx) {
  enemy.hp -= amount;
  addDamageText(enemy.x, enemy.y - 10, Math.round(amount), "#fff");

  if (enemy.hp <= 0) {
    let expGained = enemy.isBoss ? 70 : 25;
    exp += expGained;
    score += enemy.isBoss ? 250 : 80;
    createHitParticles(enemy.x, enemy.y, "#ef4444");
    enemies.splice(enemyIdx, 1);

    if (exp >= expToNext) {
      exp -= expToNext;
      level++;
      expToNext = Math.round(expToNext * 1.35);
      player.maxHp += (selectedClass.id === "WARRIOR" ? 25 : 12);
      player.hp = player.maxHp;
      player.atk += (selectedClass.id === "WARRIOR" ? 8 : 5);
      addDamageText(player.x, player.y - 25, "LEVEL UP! ✨", "#facc15");
    }
  }
}

// --- 파티클 & 플로팅 텍스트 ---
function createHitParticles(x, y, color) {
  for (let i = 0; i < 5; i++) {
    particles.push({
      x, y,
      vx: (Math.random() - 0.5) * 5,
      vy: (Math.random() - 0.5) * 5,
      life: 15,
      color
    });
  }
}

function addDamageText(x, y, text, color) {
  damageTexts.push({ x, y, text, color, life: 25 });
}

// --- 적 스폰 ---
let spawnTimer = 0;
function spawnEnemy() {
  let x, y;
  if (Math.random() < 0.5) {
    x = Math.random() < 0.5 ? -15 : canvas.width + 15;
    y = Math.random() * canvas.height;
  } else {
    x = Math.random() * canvas.width;
    y = Math.random() < 0.5 ? -15 : canvas.height + 15;
  }

  const isBoss = Math.random() < 0.05 + (level * 0.015);
  enemies.push({
    x, y,
    radius: isBoss ? 20 : 11,
    speed: isBoss ? 1.0 : (1.4 + Math.random() * 0.6),
    hp: isBoss ? 160 * (1 + level * 0.25) : 35 * (1 + level * 0.18),
    maxHp: isBoss ? 160 * (1 + level * 0.25) : 35 * (1 + level * 0.18),
    damage: isBoss ? 18 : 9,
    isBoss: isBoss,
    color: isBoss ? "#f43f5e" : "#fb7185"
  });
}

function resetGame() {
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
}

// --- 게임 메인 루프 ---
function gameLoop() {
  ctx.fillStyle = "#111827";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 던전 타일 바닥
  ctx.strokeStyle = "#1f293d";
  ctx.lineWidth = 1;
  for (let x = 0; x < canvas.width; x += 30) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
  }
  for (let y = 0; y < canvas.height; y += 30) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
  }

  // ------------------------------------
  // 상태 1: 직업 선택 화면
  // ------------------------------------
  if (gameState === "SELECT") {
    ctx.fillStyle = "rgba(0,0,0,0.4)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#f8fafc";
    ctx.font = "bold 20px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("클래스를 선택하세요", canvas.width / 2, 45);

    const classes = [CLASSES.WARRIOR, CLASSES.ARCHER, CLASSES.MAGE];
    const cardH = 75;
    const startY = 75;
    const gap = 15;

    classes.forEach((cls, i) => {
      const top = startY + i * (cardH + gap);
      // 카드 배경
      ctx.fillStyle = "#1e293b";
      ctx.strokeStyle = cls.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.roundRect(25, top, canvas.width - 50, cardH, 10);
      ctx.fill();
      ctx.stroke();

      // 아이콘 & 이름
      ctx.textAlign = "left";
      ctx.font = "bold 16px sans-serif";
      ctx.fillStyle = cls.color;
      ctx.fillText(`${cls.icon} ${cls.name}`, 40, top + 28);

      // 설명
      ctx.font = "11px sans-serif";
      ctx.fillStyle = "#94a3b8";
      ctx.fillText(cls.desc, 40, top + 52);
    });

    requestAnimationFrame(gameLoop);
    return;
  }

  // ------------------------------------
  // 상태 2: 게임 플레이 업데이트
  // ------------------------------------
  if (gameState === "PLAYING") {
    if (player.attackCooldown > 0) player.attackCooldown--;

    // 플레이어 이동 (조이스틱)
    if (joystick.active) {
      player.x += joystick.dx * player.speed;
      player.y += joystick.dy * player.speed;
    }

    player.x = Math.max(player.radius, Math.min(canvas.width - player.radius, player.x));
    player.y = Math.max(player.radius, Math.min(canvas.height - player.radius, player.y));

    // 적 스폰
    spawnTimer++;
    if (spawnTimer > Math.max(25, 70 - level * 4)) {
      spawnEnemy();
      spawnTimer = 0;
    }

    // 투사체/공격 판정 처리
    for (let i = attacks.length - 1; i >= 0; i--) {
      let atk = attacks[i];
      atk.x += atk.vx;
      atk.y += atk.vy;
      let distMoved = Math.hypot(atk.vx, atk.vy);
      atk.travelled += distMoved;

      // 최대 사거리 도달 시
      if (atk.travelled >= atk.maxDist || atk.x < 0 || atk.x > canvas.width || atk.y < 0 || atk.y > canvas.height) {
        // 마법사 폭발
        if (atk.type === "FIREBALL") {
          triggerExplosion(atk.x, atk.y, atk.explosionRadius, atk.damage);
        }
        attacks.splice(i, 1);
        continue;
      }

      // 적 충돌 검사
      let hit = false;
      for (let j = enemies.length - 1; j >= 0; j--) {
        let e = enemies[j];
        if (Math.hypot(atk.x - e.x, atk.y - e.y) < atk.radius + e.radius) {
          if (atk.type === "ARROW") {
            applyDamage(e, atk.damage, j);
            createHitParticles(atk.x, atk.y, "#34d399");
            attacks.splice(i, 1);
            hit = true;
            break;
          } else if (atk.type === "FIREBALL") {
            triggerExplosion(atk.x, atk.y, atk.explosionRadius, atk.damage);
            attacks.splice(i, 1);
            hit = true;
            break;
          }
        }
      }
    }

    // 적 이동 & 플레이어 피격
    for (let i = enemies.length - 1; i >= 0; i--) {
      let e = enemies[i];
      let angle = Math.atan2(player.y - e.y, player.x - e.x);
      e.x += Math.cos(angle) * e.speed;
      e.y += Math.sin(angle) * e.speed;

      let d = Math.hypot(player.x - e.x, player.y - e.y);
      if (d < player.radius + e.radius) {
        // 방어력 적용 대미지
        player.hp -= (e.damage * selectedClass.def) * 0.05;
        if (player.hp <= 0) {
          player.hp = 0;
          gameState = "GAMEOVER";
        }
      }
    }
  }

  // 폭발 함수 (마법사)
  function triggerExplosion(x, y, radius, damage) {
    createHitParticles(x, y, "#c084fc");
    for (let i = 0; i < 10; i++) {
      particles.push({
        x, y,
        vx: (Math.random() - 0.5) * 8,
        vy: (Math.random() - 0.5) * 8,
        life: 20,
        color: "#f472b6"
      });
    }

    enemies.forEach((e, idx) => {
      if (Math.hypot(e.x - x, e.y - y) <= radius + e.radius) {
        applyDamage(e, damage, idx);
      }
    });
  }

  // --- 렌더링 ---
  // 1. 검사 베기 이펙트
  for (let i = slashEffects.length - 1; i >= 0; i--) {
    let s = slashEffects[i];
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.range, s.angle - Math.PI / 3, s.angle + Math.PI / 3);
    ctx.strokeStyle = `rgba(147, 197, 253, ${s.life / 10})`;
    ctx.lineWidth = 6;
    ctx.stroke();
    s.life--;
    if (s.life <= 0) slashEffects.splice(i, 1);
  }

  // 2. 발사체
  attacks.forEach(atk => {
    ctx.beginPath();
    ctx.arc(atk.x, atk.y, atk.radius, 0, Math.PI * 2);
    ctx.fillStyle = atk.type === "ARROW" ? "#34d399" : "#c084fc";
    ctx.shadowBlur = 8;
    ctx.shadowColor = ctx.fillStyle;
    ctx.fill();
    ctx.shadowBlur = 0;
  });

  // 3. 적
  enemies.forEach(e => {
    ctx.beginPath();
    ctx.arc(e.x, e.y, e.radius, 0, Math.PI * 2);
    ctx.fillStyle = e.color;
    ctx.fill();

    // 체력바
    const bw = e.radius * 2;
    ctx.fillStyle = "#334155";
    ctx.fillRect(e.x - e.radius, e.y - e.radius - 6, bw, 3);
    ctx.fillStyle = "#ef4444";
    ctx.fillRect(e.x - e.radius, e.y - e.radius - 6, bw * (e.hp / e.maxHp), 3);
  });

  // 4. 파티클
  for (let i = particles.length - 1; i >= 0; i--) {
    let pt = particles[i];
    pt.x += pt.vx;
    pt.y += pt.vy;
    pt.life--;
    ctx.fillStyle = pt.color;
    ctx.fillRect(pt.x, pt.y, 2, 2);
    if (pt.life <= 0) particles.splice(i, 1);
  }

  // 5. 대미지 텍스트
  for (let i = damageTexts.length - 1; i >= 0; i--) {
    let dt = damageTexts[i];
    dt.y -= 0.6;
    dt.life--;
    ctx.font = "bold 11px sans-serif";
    ctx.fillStyle = dt.color;
    ctx.fillText(dt.text, dt.x - 8, dt.y);
    if (dt.life <= 0) damageTexts.splice(i, 1);
  }

  // 6. 플레이어
  if (selectedClass) {
    ctx.beginPath();
    ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
    ctx.fillStyle = selectedClass.color;
    ctx.shadowBlur = 10;
    ctx.shadowColor = selectedClass.color;
    ctx.fill();
    ctx.shadowBlur = 0;

    // 조준선
    ctx.beginPath();
    ctx.moveTo(player.x, player.y);
    ctx.lineTo(player.x + Math.cos(player.facingAngle) * (player.radius + 6), player.y + Math.sin(player.facingAngle) * (player.radius + 6));
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 3;
    ctx.stroke();
  }

  // 7. 상단 HUD (HP / EXP / Score)
  // HP 바
  ctx.fillStyle = "#1e293b";
  ctx.fillRect(10, 10, 110, 14);
  ctx.fillStyle = "#22c55e";
  ctx.fillRect(10, 10, 110 * (player.hp / player.maxHp), 14);
  ctx.strokeStyle = "#475569";
  ctx.strokeRect(10, 10, 110, 14);
  ctx.fillStyle = "#fff";
  ctx.font = "bold 9px sans-serif";
  ctx.textAlign = "left";
  ctx.fillText(`HP ${Math.ceil(player.hp)}/${player.maxHp}`, 14, 21);

  // 상단 EXP Bar
  ctx.fillStyle = "#1e293b";
  ctx.fillRect(0, 0, canvas.width, 3);
  ctx.fillStyle = "#eab308";
  ctx.fillRect(0, 0, canvas.width * (exp / expToNext), 3);

  // 스코어 & 레벨
  ctx.font = "bold 12px sans-serif";
  ctx.fillStyle = "#f8fafc";
  ctx.textAlign = "right";
  ctx.fillText(`Lv.${level} | ${score}점`, canvas.width - 10, 22);

  // 게임 오버
  if (gameState === "GAMEOVER") {
    ctx.fillStyle = "rgba(0,0,0,0.8)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#ef4444";
    ctx.font = "bold 30px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("GAME OVER", canvas.width / 2, canvas.height / 2 - 20);

    ctx.fillStyle = "#f8fafc";
    ctx.font = "14px sans-serif";
    ctx.fillText(`최종 점수: ${score}점 (Lv.${level})`, canvas.width / 2, canvas.height / 2 + 15);
    ctx.fillText("화면을 터치하여 다시 시작", canvas.width / 2, canvas.height / 2 + 45);
  }

  requestAnimationFrame(gameLoop);
}

requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

components.html(game_html, height=560)
