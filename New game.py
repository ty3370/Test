import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="2D 실시간 액션 RPG", page_icon="⚔️", layout="centered")

st.markdown("<h2 style='text-align: center;'>⚔️ 2D 탑뷰 실시간 던전 서바이벌 RPG</h2>", unsafe_allow_html=True)
st.caption("조작법: [W, A, S, D] 또는 [방향키] 이동 | [마우스 클릭 / Space] 마법구 발사 | [R] 재시작")

# 캔버스 및 JavaScript 기반 게임 엔진
game_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {
    margin: 0;
    padding: 0;
    background: #0f111a;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #fff;
    overflow: hidden;
  }
  #gameContainer {
    position: relative;
    border: 3px solid #3b4252;
    border-radius: 8px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  }
  canvas {
    display: block;
    background: #1a1c23;
  }
</style>
</head>
<body>

<div id="gameContainer">
  <canvas id="gameCanvas" width="700" height="500"></canvas>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// --- 게임 상태 ---
let keys = {};
let mouse = { x: 0, y: 0 };
let gameOver = false;
let score = 0;
let level = 1;
let exp = 0;
let expToNext = 100;

// --- 플레이어 ---
const player = {
  x: canvas.width / 2,
  y: canvas.height / 2,
  radius: 16,
  speed: 3.5,
  hp: 100,
  maxHp: 100,
  atk: 25,
  color: "#4ade80"
};

let projectiles = [];
let enemies = [];
let particles = [];
let damageTexts = [];

// --- 입력 이벤트 리스너 ---
window.addEventListener("keydown", e => {
  keys[e.key.toLowerCase()] = true;
  if (e.code === "Space") shootProjectile(mouse.x, mouse.y);
  if (e.key.toLowerCase() === "r" && gameOver) resetGame();
});

window.addEventListener("keyup", e => {
  keys[e.key.toLowerCase()] = false;
});

canvas.addEventListener("mousemove", e => {
  const rect = canvas.getBoundingClientRect();
  mouse.x = e.clientX - rect.left;
  mouse.y = e.clientY - rect.top;
});

canvas.addEventListener("mousedown", e => {
  if (gameOver) {
    resetGame();
    return;
  }
  shootProjectile(mouse.x, mouse.y);
});

// --- 투사체 발사 ---
function shootProjectile(targetX, targetY) {
  const angle = Math.atan2(targetY - player.y, targetX - player.x);
  const speed = 7;
  projectiles.push({
    x: player.x,
    y: player.y,
    vx: Math.cos(angle) * speed,
    vy: Math.sin(angle) * speed,
    radius: 5,
    damage: player.atk,
    color: "#60a5fa"
  });
}

// --- 적 생성기 ---
let enemySpawnTimer = 0;
function spawnEnemy() {
  let x, y;
  if (Math.random() < 0.5) {
    x = Math.random() < 0.5 ? 0 - 20 : canvas.width + 20;
    y = Math.random() * canvas.height;
  } else {
    x = Math.random() * canvas.width;
    y = Math.random() < 0.5 ? 0 - 20 : canvas.height + 20;
  }

  // 레벨에 따라 적 종류 결정
  const isBoss = Math.random() < 0.05 + (level * 0.02);
  enemies.push({
    x: x,
    y: y,
    radius: isBoss ? 24 : 12,
    speed: isBoss ? 1.0 : (1.5 + Math.random() * 0.8),
    hp: isBoss ? 150 * (1 + level * 0.3) : 30 * (1 + level * 0.2),
    maxHp: isBoss ? 150 * (1 + level * 0.3) : 30 * (1 + level * 0.2),
    damage: isBoss ? 20 : 8,
    isBoss: isBoss,
    color: isBoss ? "#ef4444" : "#f87171"
  });
}

// --- 파티클 & 대미지 플로팅 텍스트 ---
function createHitParticles(x, y, color) {
  for (let i = 0; i < 6; i++) {
    particles.push({
      x: x,
      y: y,
      vx: (Math.random() - 0.5) * 4,
      vy: (Math.random() - 0.5) * 4,
      life: 20,
      color: color
    });
  }
}

function addDamageText(x, y, text, color) {
  damageTexts.push({ x, y, text, color, life: 30 });
}

// --- 게임 리셋 ---
function resetGame() {
  player.x = canvas.width / 2;
  player.y = canvas.height / 2;
  player.hp = 100;
  player.maxHp = 100;
  player.atk = 25;
  player.speed = 3.5;
  level = 1;
  exp = 0;
  expToNext = 100;
  score = 0;
  projectiles = [];
  enemies = [];
  particles = [];
  damageTexts = [];
  gameOver = false;
}

// --- 메인 업데이트 & 렌더링 루프 ---
function gameLoop() {
  // 배경 클리어
  ctx.fillStyle = "#111827";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 던전 타일 격자 패턴
  ctx.strokeStyle = "#1f2937";
  ctx.lineWidth = 1;
  for (let x = 0; x < canvas.width; x += 40) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }
  for (let y = 0; y < canvas.height; y += 40) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
  }

  if (!gameOver) {
    // 1. 플레이어 이동
    if (keys['w'] || keys['arrowup']) player.y -= player.speed;
    if (keys['s'] || keys['arrowdown']) player.y += player.speed;
    if (keys['a'] || keys['arrowleft']) player.x -= player.speed;
    if (keys['d'] || keys['arrowright']) player.x += player.speed;

    // 화면 밖 경계 처리
    player.x = Math.max(player.radius, Math.min(canvas.width - player.radius, player.x));
    player.y = Math.max(player.radius, Math.min(canvas.height - player.radius, player.y));

    // 2. 적 스폰
    enemySpawnTimer++;
    if (enemySpawnTimer > Math.max(30, 80 - level * 5)) {
      spawnEnemy();
      enemySpawnTimer = 0;
    }

    // 3. 투사체 업데이트
    for (let i = projectiles.length - 1; i >= 0; i--) {
      let p = projectiles[i];
      p.x += p.vx;
      p.y += p.vy;

      // 화면 밖 제거
      if (p.x < 0 || p.x > canvas.width || p.y < 0 || p.y > canvas.height) {
        projectiles.splice(i, 1);
        continue;
      }

      // 몬스터 피격 판정
      for (let j = enemies.length - 1; j >= 0; j--) {
        let e = enemies[j];
        let dist = Math.hypot(p.x - e.x, p.y - e.y);
        if (dist < p.radius + e.radius) {
          e.hp -= p.damage;
          createHitParticles(p.x, p.y, "#93c5fd");
          addDamageText(e.x, e.y - 10, Math.round(p.damage), "#ffffff");
          projectiles.splice(i, 1);

          // 몬스터 사망
          if (e.hp <= 0) {
            let expGained = e.isBoss ? 80 : 25;
            exp += expGained;
            score += e.isBoss ? 300 : 100;
            createHitParticles(e.x, e.y, "#f87171");
            enemies.splice(j, 1);

            // 레벨업 체크
            if (exp >= expToNext) {
              exp -= expToNext;
              level++;
              expToNext = Math.round(expToNext * 1.4);
              player.maxHp += 15;
              player.hp = player.maxHp;
              player.atk += 6;
              addDamageText(player.x, player.y - 25, "LEVEL UP! 🌟", "#facc15");
            }
          }
          break;
        }
      }
    }

    // 4. 적 AI (플레이어 추적)
    for (let i = enemies.length - 1; i >= 0; i--) {
      let e = enemies[i];
      let angle = Math.atan2(player.y - e.y, player.x - e.x);
      e.x += Math.cos(angle) * e.speed;
      e.y += Math.sin(angle) * e.speed;

      // 플레이어 충돌 대미지
      let dist = Math.hypot(player.x - e.x, player.y - e.y);
      if (dist < player.radius + e.radius) {
        player.hp -= e.damage * 0.05; // 지속 피해
        if (Math.random() < 0.1) {
          createHitParticles(player.x, player.y, "#ef4444");
        }
        if (player.hp <= 0) {
          player.hp = 0;
          gameOver = true;
        }
      }
    }
  }

  // --- 렌더링 파트 ---
  // 1. 투사체 그리기
  projectiles.forEach(p => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
    ctx.fillStyle = p.color;
    ctx.shadowBlur = 8;
    ctx.shadowColor = p.color;
    ctx.fill();
    ctx.shadowBlur = 0;
  });

  // 2. 적 그리기 & 체력 바
  enemies.forEach(e => {
    ctx.beginPath();
    ctx.arc(e.x, e.y, e.radius, 0, Math.PI * 2);
    ctx.fillStyle = e.color;
    ctx.fill();

    // 체력바
    const barW = e.radius * 2;
    const barH = 4;
    ctx.fillStyle = "#374151";
    ctx.fillRect(e.x - e.radius, e.y - e.radius - 8, barW, barH);
    ctx.fillStyle = "#ef4444";
    ctx.fillRect(e.x - e.radius, e.y - e.radius - 8, barW * (e.hp / e.maxHp), barH);
  });

  // 3. 파티클 업데이트 및 그리기
  for (let i = particles.length - 1; i >= 0; i--) {
    let pt = particles[i];
    pt.x += pt.vx;
    pt.y += pt.vy;
    pt.life--;
    ctx.fillStyle = pt.color;
    ctx.fillRect(pt.x, pt.y, 2, 2);
    if (pt.life <= 0) particles.splice(i, 1);
  }

  // 4. 대미지 텍스트
  for (let i = damageTexts.length - 1; i >= 0; i--) {
    let dt = damageTexts[i];
    dt.y -= 0.6;
    dt.life--;
    ctx.font = "bold 12px sans-serif";
    ctx.fillStyle = dt.color;
    ctx.fillText(dt.text, dt.x - 10, dt.y);
    if (dt.life <= 0) damageTexts.splice(i, 1);
  }

  // 5. 플레이어 그리기
  ctx.beginPath();
  ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
  ctx.fillStyle = player.color;
  ctx.shadowBlur = 10;
  ctx.shadowColor = player.color;
  ctx.fill();
  ctx.shadowBlur = 0;

  // 플레이어 시선 방향 표시
  const aimAngle = Math.atan2(mouse.y - player.y, mouse.x - player.x);
  ctx.beginPath();
  ctx.moveTo(player.x, player.y);
  ctx.lineTo(player.x + Math.cos(aimAngle) * (player.radius + 6), player.y + Math.sin(aimAngle) * (player.radius + 6));
  ctx.strokeStyle = "#ffffff";
  ctx.lineWidth = 3;
  ctx.stroke();

  // --- UI HUD ---
  // HP 바 (좌상단)
  ctx.fillStyle = "#1e293b";
  ctx.fillRect(15, 15, 160, 16);
  ctx.fillStyle = "#22c55e";
  ctx.fillRect(15, 15, 160 * (player.hp / player.maxHp), 16);
  ctx.strokeStyle = "#475569";
  ctx.strokeRect(15, 15, 160, 16);
  ctx.fillStyle = "#ffffff";
  ctx.font = "bold 11px sans-serif";
  ctx.fillText(`HP: ${Math.ceil(player.hp)} / ${player.maxHp}`, 20, 27);

  // EXP 바 (상단 전체)
  ctx.fillStyle = "#1e293b";
  ctx.fillRect(0, 0, canvas.width, 5);
  ctx.fillStyle = "#eab308";
  ctx.fillRect(0, 0, canvas.width * (exp / expToNext), 5);

  // 점수 / 레벨 표시 (우상단)
  ctx.font = "bold 14px sans-serif";
  ctx.fillStyle = "#f8fafc";
  ctx.textAlign = "right";
  ctx.fillText(`Lv. ${level} | Score: ${score}`, canvas.width - 20, 27);
  ctx.textAlign = "left";

  // 게임 오버 오버레이
  if (gameOver) {
    ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = "#ef4444";
    ctx.font = "bold 36px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("YOU DIED", canvas.width / 2, canvas.height / 2 - 20);

    ctx.fillStyle = "#ffffff";
    ctx.font = "16px sans-serif";
    ctx.fillText(`최종 점수: ${score}점 (레벨 ${level})`, canvas.width / 2, canvas.height / 2 + 20);
    ctx.fillText("화면을 클릭하거나 [R] 키를 눌러 재시작", canvas.width / 2, canvas.height / 2 + 50);
    ctx.textAlign = "left";
  }

  requestAnimationFrame(gameLoop);
}

// 루프 시작
requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

# HTML 컴포넌트 렌더링
components.html(game_html, height=530)

st.markdown("---")
with st.expander("💡 게임 특징 및 업그레이드 요소"):
    st.markdown("""
    - **60 FPS 실시간 렌더링**: Canvas 2D 기반으로 Streamlit 새로고침 지연 없이 부드럽게 작동합니다.
    - **레벨업 시스템**: 몬스터를 처치하여 경험치바를 채우면 공격력과 최대 체력이 상승하고 풀피로 회복됩니다.
    - **보스 몬스터**: 일정 확률로 거대 보스 몬스터가 출현하며 처치 시 더 많은 점수와 경험치를 획득합니다.
    """)
