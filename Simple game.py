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

# 모바일 최적화 HTML/JS 코드
game_html = """
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <style>
    * {
      touch-action: none; /* 스마트폰 스크롤 방지 */
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

  // 게임 상태: 'START', 'PLAYING', 'GAMEOVER', 'WIN'
  let gameState = 'START';

  // 볼 속성
  let ballRadius = 8;
  let x, y, dx, dy;

  // 패들 속성
  const paddleHeight = 12;
  const paddleWidth = 85;
  let paddleX;

  // 벽돌 설정 (세로형 모바일에 맞춰 4행 5열)
  const brickRowCount = 4;
  const brickColumnCount = 5;
  const brickWidth = 56;
  const brickHeight = 20;
  const brickPadding = 8;
  const brickOffsetTop = 50;
  const brickOffsetLeft = 22;

  let score = 0;
  let lives = 3;
  let bricks = [];

  function resetGame() {
    x = canvas.width / 2;
    y = canvas.height - 40;
    dx = 3;
    dy = -4;
    paddleX = (canvas.width - paddleWidth) / 2;
    score = 0;
    lives = 3;

    bricks = [];
    for (let c = 0; c < brickColumnCount; c++) {
      bricks[c] = [];
      for (let r = 0; r < brickRowCount; r++) {
        bricks[c][r] = { x: 0, y: 0, status: 1 };
      }
    }
  }

  // 터치 & 마우스 드래그 조작 이벤트
  function updatePaddlePosition(clientX) {
    const rect = canvas.getBoundingClientRect();
    const touchX = clientX - rect.left;
    const scale = canvas.width / rect.width;
    const gameX = touchX * scale;

    paddleX = gameX - paddleWidth / 2;

    if (paddleX < 0) paddleX = 0;
    if (paddleX > canvas.width - paddleWidth) paddleX = canvas.width - paddleWidth;
  }

  // 터치 이벤트
  canvas.addEventListener("touchstart", (e) => {
    if (gameState !== 'PLAYING') {
      resetGame();
      gameState = 'PLAYING';
    } else {
      updatePaddlePosition(e.touches[0].clientX);
    }
  }, { passive: false });

  canvas.addEventListener("touchmove", (e) => {
    if (gameState === 'PLAYING') {
      updatePaddlePosition(e.touches[0].clientX);
    }
  }, { passive: false });

  // 마우스 이벤트 (PC 테스트용)
  canvas.addEventListener("mousedown", () => {
    if (gameState !== 'PLAYING') {
      resetGame();
      gameState = 'PLAYING';
    }
  });

  canvas.addEventListener("mousemove", (e) => {
    if (gameState === 'PLAYING') {
      updatePaddlePosition(e.clientX);
    }
  });

  function collisionDetection() {
    for (let c = 0; c < brickColumnCount; c++) {
      for (let r = 0; r < brickRowCount; r++) {
        const b = bricks[c][r];
        if (b.status === 1) {
          if (x > b.x && x < b.x + brickWidth && y > b.y && y < b.y + brickHeight) {
            dy = -dy;
            b.status = 0;
            score++;
            if (score === brickRowCount * brickColumnCount) {
              gameState = 'WIN';
            }
          }
        }
      }
    }
  }

  function drawBall() {
    ctx.beginPath();
    ctx.arc(x, y, ballRadius, 0, Math.PI * 2);
    ctx.fillStyle = "#FF4B4B";
    ctx.fill();
    ctx.closePath();
  }

  function drawPaddle() {
    ctx.beginPath();
    ctx.roundRect(paddleX, canvas.height - paddleHeight - 10, paddleWidth, paddleHeight, 6);
    ctx.fillStyle = "#58A6FF";
    ctx.fill();
    ctx.closePath();
  }

  function drawBricks() {
    const rowColors = ["#FF7B72", "#FFA657", "#D2A8FF", "#7EE787"];
    for (let c = 0; c < brickColumnCount; c++) {
      for (let r = 0; r < brickRowCount; r++) {
        if (bricks[c][r].status === 1) {
          const brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
          const brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
          bricks[c][r].x = brickX;
          bricks[c][r].y = brickY;
          ctx.beginPath();
          ctx.roundRect(brickX, brickY, brickWidth, brickHeight, 4);
          ctx.fillStyle = rowColors[r % rowColors.length];
          ctx.fill();
          ctx.closePath();
        }
      }
    }
  }

  function drawUI() {
    ctx.font = "bold 14px sans-serif";
    ctx.fillStyle = "#C9D1D9";
    ctx.fillText("점수: " + score, 15, 25);
    ctx.fillText("❤️ " + lives, canvas.width - 55, 25);
  }

  function drawOverlay(title, subtitle) {
    ctx.fillStyle = "rgba(14, 17, 23, 0.85)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.font = "bold 24px sans-serif";
    ctx.fillStyle = "#FFFFFF";
    ctx.textAlign = "center";
    ctx.fillText(title, canvas.width / 2, canvas.height / 2 - 20);

    ctx.font = "14px sans-serif";
    ctx.fillStyle = "#8B949E";
    ctx.fillText(subtitle, canvas.width / 2, canvas.height / 2 + 20);
    ctx.textAlign = "left";
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (gameState === 'START') {
      drawOverlay("🎮 스마트폰 벽돌깨기", "화면을 터치하여 시작하세요!");
    } else if (gameState === 'GAMEOVER') {
      drawOverlay("💥 GAME OVER", "화면을 터치하여 다시 도전!");
    } else if (gameState === 'WIN') {
      drawOverlay("🎉 STAGE CLEAR!", "화면을 터치하여 다시 시작!");
    } else if (gameState === 'PLAYING') {
      drawBricks();
      drawBall();
      drawPaddle();
      drawUI();
      collisionDetection();

      // 벽면 충돌
      if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
        dx = -dx;
      }
      if (y + dy < ballRadius + 30) {
        dy = -dy;
      } else if (y + dy > canvas.height - paddleHeight - 10 - ballRadius) {
        if (x > paddleX && x < paddleX + paddleWidth) {
          // 패들의 맞은 위치에 따라 반사 각도 조절
          let hitPoint = (x - (paddleX + paddleWidth / 2)) / (paddleWidth / 2);
          dx = hitPoint * 4;
          dy = -Math.abs(dy);
        } else if (y + dy > canvas.height - ballRadius) {
          lives--;
          if (!lives) {
            gameState = 'GAMEOVER';
          } else {
            x = canvas.width / 2;
            y = canvas.height - 40;
            dx = 3;
            dy = -4;
            paddleX = (canvas.width - paddleWidth) / 2;
          }
        }
      }

      x += dx;
      y += dy;
    }

    requestAnimationFrame(draw);
  }

  resetGame();
  draw();
</script>
</body>
</html>
"""

# 모바일 화면 크기에 적합한 높이로 컴포넌트 출력
components.html(game_html, height=540)
