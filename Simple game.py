import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="모바일 벽돌깨기",
    page_icon="📱",
    layout="centered"
)

st.markdown("""
    <style>
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-width: 450px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📱 스마트폰 벽돌깨기")
st.caption("손가락으로 화면을 좌우로 드래그하여 패들을 조작하세요!")

game_html = """
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <style>
    * {
      touch-action: none;
      user-select: none;
      -webkit-user-select: none;
      box-sizing: border-box;
    }
    body {
      margin: 0;
      padding: 0;
      background-color: #0e1117;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    canvas {
      background: #161b22;
      border: 2px solid #30363d;
      border-radius: 16px;
      box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.6);
      width: 95vw;
      max-width: 360px;
      height: auto;
      aspect-ratio: 360 / 520;
    }
  </style>
</head>
<body>

<canvas id="gameCanvas" width="360" height="520"></canvas>

<script>
  const canvas = document.getElementById("gameCanvas");
  const ctx = canvas.getContext("2d");

  // 게임 상태: 'START', 'PLAYING', 'STAGE_CLEAR', 'GAMEOVER', 'ALL_CLEAR'
  let gameState = 'START';

  // 스테이지 설정 (최대 10스테이지)
  let currentStage = 1;
  const maxStage = 10;

  // 볼 관리
  let ballRadius = 6;
  let balls = [];

  // 패들 속성
  const paddleHeight = 12;
  const paddleWidth = 85;
  let paddleX;

  // 벽돌 설정
  const brickColumnCount = 5;
  let brickRowCount = 3;
  const brickWidth = 56;
  const brickHeight = 18;
  const brickPadding = 8;
  const brickOffsetTop = 55;
  const brickOffsetLeft = 22;
  let bricks = [];
  let remainingBricks = 0;

  // 점수, 목숨, 콤보
  let score = 0;
  let lives = 3;
  let combo = 0;
  let comboDisplayTimer = 0;
  let lastComboCount = 0;

  // 아이템 & 프렌지 타이머
  let items = [];
  let frenzyTimer = 0;

  // 사망 후 리스폰 딜레이 타이머
  let respawnTimer = 0;

  // 내구도별 색상 팔레트
  const hpColors = {
    1: "#7EE787", // 1HP (그린)
    2: "#FFA657", // 2HP (오렌지)
    3: "#FF7B72", // 3HP (레드)
    4: "#D2A8FF"  // 4HP (퍼플)
  };

  function initStage(stage) {
    // 스테이지에 따라 행 수 조절 (3행 ~ 최대 6행)
    brickRowCount = Math.min(6, 2 + Math.ceil(stage / 2));
    bricks = [];
    remainingBricks = 0;

    for (let c = 0; c < brickColumnCount; c++) {
      bricks[c] = [];
      for (let r = 0; r < brickRowCount; r++) {
        let hp = 1;

        // 스테이지 난이도에 따른 벽돌 HP 설정
        if (stage >= 2 && stage <= 4) {
          if (r === 0 && Math.random() < 0.6) hp = 2;
        } else if (stage >= 5 && stage <= 7) {
          if (r === 0) hp = Math.random() < 0.5 ? 3 : 2;
          else if (r === 1 && Math.random() < 0.5) hp = 2;
        } else if (stage >= 8) {
          if (r === 0) hp = 4;
          else if (r === 1) hp = 3;
          else if (r === 2 && Math.random() < 0.6) hp = 2;
        }

        bricks[c][r] = { 
          x: 0, 
          y: 0, 
          status: hp, 
          maxHp: hp 
        };
        remainingBricks++;
      }
    }

    items = [];
    frenzyTimer = 0;
    combo = 0;
    resetBalls(false);
  }

  function resetBalls(withRespawnDelay = false) {
    paddleX = (canvas.width - paddleWidth) / 2;
    // 스테이지가 올라갈수록 기본 속도 소폭 증가
    const baseSpeed = 3.5 + (currentStage - 1) * 0.15;
    
    balls = [{
      x: canvas.width / 2,
      y: canvas.height - 40,
      dx: (Math.random() > 0.5 ? 1 : -1) * (baseSpeed * 0.7),
      dy: -baseSpeed
    }];

    if (withRespawnDelay) {
      respawnTimer = 1500; // 1.5초 대기 텀
    } else {
      respawnTimer = 0;
    }
  }

  function resetGame() {
    score = 0;
    lives = 3;
    currentStage = 1;
    initStage(currentStage);
  }

  function activateFrenzy() {
    frenzyTimer = 7000;
    const baseBall = balls[0] || { x: canvas.width / 2, y: canvas.height - 50 };
    balls = [];
    const totalCount = 27;
    const speed = 4.5;

    for (let i = 0; i < totalCount; i++) {
      const angle = (Math.PI * 2 / totalCount) * i;
      balls.push({
        x: baseBall.x,
        y: baseBall.y,
        dx: Math.cos(angle) * speed,
        dy: Math.sin(angle) * speed
      });
    }
  }

  function updatePaddlePosition(clientX) {
    const rect = canvas.getBoundingClientRect();
    const touchX = clientX - rect.left;
    const scale = canvas.width / rect.width;
    const gameX = touchX * scale;

    paddleX = gameX - paddleWidth / 2;
    if (paddleX < 0) paddleX = 0;
    if (paddleX > canvas.width - paddleWidth) paddleX = canvas.width - paddleWidth;
  }

  function handleActionStart(clientX) {
    if (gameState === 'START' || gameState === 'GAMEOVER' || gameState === 'ALL_CLEAR') {
      resetGame();
      gameState = 'PLAYING';
    } else if (gameState === 'STAGE_CLEAR') {
      currentStage++;
      initStage(currentStage);
      gameState = 'PLAYING';
    } else if (gameState === 'PLAYING') {
      updatePaddlePosition(clientX);
    }
  }

  canvas.addEventListener("touchstart", (e) => {
    e.preventDefault();
    handleActionStart(e.touches[0].clientX);
  }, { passive: false });

  canvas.addEventListener("touchmove", (e) => {
    e.preventDefault();
    if (gameState === 'PLAYING') updatePaddlePosition(e.touches[0].clientX);
  }, { passive: false });

  canvas.addEventListener("mousedown", (e) => {
    handleActionStart(e.clientX);
  });

  canvas.addEventListener("mousemove", (e) => {
    if (gameState === 'PLAYING') updatePaddlePosition(e.clientX);
  });

  function collisionDetection() {
    for (let c = 0; c < brickColumnCount; c++) {
      for (let r = 0; r < brickRowCount; r++) {
        const b = bricks[c][r];
        if (b.status > 0) {
          for (let i = 0; i < balls.length; i++) {
            const ball = balls[i];
            if (ball.x > b.x && ball.x < b.x + brickWidth && ball.y > b.y && ball.y < b.y + brickHeight) {
              ball.dy = -ball.dy;
              b.status--;

              // 콤보 및 점수 계산
              combo++;
              lastComboCount = combo;
              comboDisplayTimer = 40;
              score += 10 + (combo * 5);

              // 완전히 파괴되었을 때
              if (b.status === 0) {
                remainingBricks--;

                // 아이템 드롭
                if (Math.random() < 0.18) {
                  items.push({
                    x: b.x + brickWidth / 2,
                    y: b.y + brickHeight / 2,
                    dy: 2.2,
                    width: 34,
                    height: 18
                  });
                }

                // 스테이지 클리어 검사
                if (remainingBricks <= 0) {
                  if (currentStage >= maxStage) {
                    gameState = 'ALL_CLEAR';
                  } else {
                    gameState = 'STAGE_CLEAR';
                  }
                  return;
                }
              }
              break;
            }
          }
        }
      }
    }
  }

  function drawBalls() {
    for (let i = 0; i < balls.length; i++) {
      const ball = balls[i];
      ctx.beginPath();
      ctx.arc(ball.x, ball.y, ballRadius, 0, Math.PI * 2);
      ctx.fillStyle = frenzyTimer > 0 ? "#D2A8FF" : "#FF4B4B";
      ctx.fill();
      ctx.closePath();
    }
  }

  function drawPaddle() {
    ctx.beginPath();
    ctx.roundRect(paddleX, canvas.height - paddleHeight - 12, paddleWidth, paddleHeight, 6);
    ctx.fillStyle = "#58A6FF";
    ctx.fill();
    ctx.closePath();
  }

  function drawBricks() {
    for (let c = 0; c < brickColumnCount; c++) {
      for (let r = 0; r < brickRowCount; r++) {
        const b = bricks[c][r];
        if (b.status > 0) {
          const brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
          const brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
          b.x = brickX;
          b.y = brickY;

          // 체력에 따른 벽돌 렌더링
          ctx.beginPath();
          ctx.roundRect(brickX, brickY, brickWidth, brickHeight, 4);
          ctx.fillStyle = hpColors[b.status] || "#7EE787";
          ctx.fill();
          ctx.closePath();

          // HP가 2 이상이면 내구도 텍스트 표기
          if (b.status > 1) {
            ctx.font = "bold 10px sans-serif";
            ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(b.status, brickX + brickWidth / 2, brickY + brickHeight / 2 + 1);
          }
        }
      }
    }
    ctx.textAlign = "left";
    ctx.textBaseline = "alphabetic";
  }

  function drawItems() {
    for (let i = items.length - 1; i >= 0; i--) {
      const item = items[i];
      item.y += item.dy;

      // 보라색 캡슐
      ctx.beginPath();
      ctx.roundRect(item.x - item.width / 2, item.y - item.height / 2, item.width, item.height, 8);
      ctx.fillStyle = "#A371F7";
      ctx.fill();
      ctx.strokeStyle = "#FFFFFF";
      ctx.lineWidth = 1.5;
      ctx.stroke();
      ctx.closePath();

      // "2-7" 라벨
      ctx.font = "bold 11px sans-serif";
      ctx.fillStyle = "#FFFFFF";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("2-7", item.x, item.y + 1);

      // 패들 획득 판정
      const paddleY = canvas.height - paddleHeight - 12;
      if (item.y + item.height / 2 >= paddleY &&
          item.y - item.height / 2 <= paddleY + paddleHeight &&
          item.x >= paddleX && item.x <= paddleX + paddleWidth) {
        activateFrenzy();
        items.splice(i, 1);
      } else if (item.y > canvas.height) {
        items.splice(i, 1);
      }
    }
    ctx.textAlign = "left";
    ctx.textBaseline = "alphabetic";
  }

  function drawUI() {
    ctx.font = "bold 13px sans-serif";
    ctx.fillStyle = "#C9D1D9";
    ctx.fillText(`STAGE ${currentStage}/${maxStage}`, 15, 25);
    ctx.fillText(`점수: ${score}`, 115, 25);
    ctx.fillText(`❤️ ${lives}`, canvas.width - 55, 25);

    // 콤보 표시
    if (comboDisplayTimer > 0 && lastComboCount > 1) {
      ctx.font = "bold 16px sans-serif";
      ctx.fillStyle = "#FFA657";
      ctx.textAlign = "center";
      ctx.fillText(`🔥 ${lastComboCount} COMBO!`, canvas.width / 2, canvas.height / 2 + 50);
      ctx.textAlign = "left";
      comboDisplayTimer--;
    }

    // 27-Ball 지속시간 표시
    if (frenzyTimer > 0) {
      ctx.font = "bold 12px sans-serif";
      ctx.fillStyle = "#D2A8FF";
      ctx.fillText(`⚡ 27-BALL: ${(frenzyTimer / 1000).toFixed(1)}s`, 15, 45);
    }

    // 리스폰 카운트다운 오버레이
    if (respawnTimer > 0) {
      ctx.font = "bold 20px sans-serif";
      ctx.fillStyle = "#FFD33D";
      ctx.textAlign = "center";
      const count = Math.ceil(respawnTimer / 500);
      ctx.fillText(`READY... ${count}`, canvas.width / 2, canvas.height / 2 + 20);
      ctx.textAlign = "left";
    }
  }

  function drawOverlay(title, subtitle) {
    ctx.fillStyle = "rgba(14, 17, 23, 0.88)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.font = "bold 22px sans-serif";
    ctx.fillStyle = "#FFFFFF";
    ctx.textAlign = "center";
    ctx.fillText(title, canvas.width / 2, canvas.height / 2 - 15);

    ctx.font = "14px sans-serif";
    ctx.fillStyle = "#8B949E";
    ctx.fillText(subtitle, canvas.width / 2, canvas.height / 2 + 25);
    ctx.textAlign = "left";
  }

  let lastTime = performance.now();
  function draw(currentTime) {
    const dt = currentTime - lastTime;
    lastTime = currentTime;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (gameState === 'START') {
      drawOverlay("🎮 모바일 벽돌깨기", "화면을 터치하여 시작하세요!");
    } else if (gameState === 'STAGE_CLEAR') {
      drawOverlay(`🎉 STAGE ${currentStage} CLEAR!`, "화면을 터치해 다음 스테이지로!");
    } else if (gameState === 'ALL_CLEAR') {
      drawOverlay("🏆 ALL STAGE CLEAR!", `축하합니다! 최종 점수: ${score}점`);
    } else if (gameState === 'GAMEOVER') {
      drawOverlay("💥 GAME OVER", `점수: ${score}점 (터치하여 다시 시작)`);
    } else if (gameState === 'PLAYING') {
      // 프렌지 타이머
      if (frenzyTimer > 0) {
        frenzyTimer -= dt;
        if (frenzyTimer <= 0) {
          frenzyTimer = 0;
          if (balls.length > 1) {
            balls = [balls[0]];
          }
        }
      }

      drawBricks();
      drawItems();
      drawBalls();
      drawPaddle();
      drawUI();

      // 리스폰 대기 중일 때는 공과 충돌 로직 정지
      if (respawnTimer > 0) {
        respawnTimer -= dt;
        requestAnimationFrame(draw);
        return;
      }

      collisionDetection();

      // 볼 이동 및 반사
      const paddleY = canvas.height - paddleHeight - 12;
      for (let i = balls.length - 1; i >= 0; i--) {
        const ball = balls[i];

        // 좌우 벽
        if (ball.x + ball.dx > canvas.width - ballRadius || ball.x + ball.dx < ballRadius) {
          ball.dx = -ball.dx;
        }

        // 천장
        if (ball.y + ball.dy < ballRadius + 30) {
          ball.dy = -ball.dy;
        } 
        // 패들 충돌
        else if (ball.y + ball.dy >= paddleY - ballRadius && ball.y <= paddleY + paddleHeight) {
          if (ball.x >= paddleX && ball.x <= paddleX + paddleWidth) {
            const hitPoint = (ball.x - (paddleX + paddleWidth / 2)) / (paddleWidth / 2);
            const currentSpeed = Math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy);
            ball.dx = hitPoint * (currentSpeed * 0.9);
            ball.dy = -Math.abs(Math.sqrt(Math.max(4, currentSpeed * currentSpeed - ball.dx * ball.dx)));
            
            // 패들에 닿으면 콤보 리셋
            combo = 0;
          }
        }

        // 바닥 추락
        if (ball.y + ball.dy > canvas.height - ballRadius) {
          balls.splice(i, 1);
        } else {
          ball.x += ball.dx;
          ball.y += ball.dy;
        }
      }

      // 모든 공을 놓친 경우
      if (balls.length === 0) {
        lives--;
        combo = 0;
        frenzyTimer = 0;
        if (lives <= 0) {
          gameState = 'GAMEOVER';
        } else {
          resetBalls(true); // 사망 후 텀을 두고 리스폰
        }
      }
    }

    requestAnimationFrame(draw);
  }

  resetGame();
  requestAnimationFrame(draw);
</script>
</body>
</html>
"""

components.html(game_html, height=540)
