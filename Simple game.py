
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="벽돌깨기 게임",
    page_icon="🎮",
    layout="centered"
)

st.title("🎮 벽돌깨기 (Brick Breaker)")
st.write("마우스 이동 또는 키보드 방향키(← / →)로 패들을 조작하여 공을 튕겨내세요!")

# HTML/JS 게임 코드
game_html = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      margin: 0;
      padding: 0;
      background-color: #0e1117;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-family: sans-serif;
    }
    canvas {
      background: #161b22;
      border: 2px solid #30363d;
      border-radius: 8px;
      box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.5);
      cursor: none;
    }
  </style>
</head>
<body>

<canvas id="gameCanvas" width="480" height="320"></canvas>

<script>
  const canvas = document.getElementById("gameCanvas");
  const ctx = canvas.getContext("2d");

  // 볼 속성
  let ballRadius = 7;
  let x = canvas.width / 2;
  let y = canvas.height - 30;
  let dx = 3;
  let dy = -3;

  // 패들 속성
  const paddleHeight = 10;
  let paddleWidth = 75;
  let paddleX = (canvas.width - paddleWidth) / 2;

  // 키 제어
  let rightPressed = false;
  let leftPressed = false;

  // 벽돌 설정
  const brickRowCount = 3;
  const brickColumnCount = 5;
  const brickWidth = 75;
  const brickHeight = 18;
  const brickPadding = 10;
  const brickOffsetTop = 30;
  const brickOffsetLeft = 30;

  let score = 0;
  let lives = 3;

  let bricks = [];
  for (let c = 0; c < brickColumnCount; c++) {
    bricks[c] = [];
    for (let r = 0; r < brickRowCount; r++) {
      bricks[c][r] = { x: 0, y: 0, status: 1 };
    }
  }

  // 이벤트 리스너 (키보드 및 마우스)
  document.addEventListener("keydown", keyDownHandler, false);
  document.addEventListener("keyup", keyUpHandler, false);
  document.addEventListener("mousemove", mouseMoveHandler, false);

  function keyDownHandler(e) {
    if (e.key === "Right" || e.key === "ArrowRight") rightPressed = true;
    else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = true;
  }

  function keyUpHandler(e) {
    if (e.key === "Right" || e.key === "ArrowRight") rightPressed = false;
    else if (e.key === "Left" || e.key === "ArrowLeft") leftPressed = false;
  }

  function mouseMoveHandler(e) {
    const relativeX = e.clientX - canvas.getBoundingClientRect().left;
    if (relativeX > 0 && relativeX < canvas.width) {
      paddleX = relativeX - paddleWidth / 2;
    }
  }

  // 충돌 감지
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
              alert("🎉 축하합니다! 모든 벽돌을 깨트렸습니다!");
              document.location.reload();
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
    ctx.rect(paddleX, canvas.height - paddleHeight, paddleWidth, paddleHeight);
    ctx.fillStyle = "#58A6FF";
    ctx.fill();
    ctx.closePath();
  }

  function drawBricks() {
    const rowColors = ["#FF7B72", "#FFA657", "#D2A8FF"];
    for (let c = 0; c < brickColumnCount; c++) {
      for (let r = 0; r < brickRowCount; r++) {
        if (bricks[c][r].status === 1) {
          const brickX = c * (brickWidth + brickPadding) + brickOffsetLeft;
          const brickY = r * (brickHeight + brickPadding) + brickOffsetTop;
          bricks[c][r].x = brickX;
          bricks[c][r].y = brickY;
          ctx.beginPath();
          ctx.rect(brickX, brickY, brickWidth, brickHeight);
          ctx.fillStyle = rowColors[r % rowColors.length];
          ctx.fill();
          ctx.closePath();
        }
      }
    }
  }

  function drawScore() {
    ctx.font = "14px sans-serif";
    ctx.fillStyle = "#8B949E";
    ctx.fillText("점수: " + score, 10, 20);
  }

  function drawLives() {
    ctx.font = "14px sans-serif";
    ctx.fillStyle = "#8B949E";
    ctx.fillText("남은 기회: " + lives, canvas.width - 85, 20);
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBricks();
    drawBall();
    drawPaddle();
    drawScore();
    drawLives();
    collisionDetection();

    // 벽면 반사 처리
    if (x + dx > canvas.width - ballRadius || x + dx < ballRadius) {
      dx = -dx;
    }
    if (y + dy < ballRadius) {
      dy = -dy;
    } else if (y + dy > canvas.height - ballRadius) {
      if (x > paddleX && x < paddleX + paddleWidth) {
        dy = -dy;
      } else {
        lives--;
        if (!lives) {
          alert("GAME OVER! 다시 도전해보세요.");
          document.location.reload();
        } else {
          x = canvas.width / 2;
          y = canvas.height - 30;
          dx = 3;
          dy = -3;
          paddleX = (canvas.width - paddleWidth) / 2;
        }
      }
    }

    if (rightPressed && paddleX < canvas.width - paddleWidth) {
      paddleX += 7;
    } else if (leftPressed && paddleX > 0) {
      paddleX -= 7;
    }

    x += dx;
    y += dy;
    requestAnimationFrame(draw);
  }

  draw();
</script>
</body>
</html>
"""

# HTML 컴포넌트 렌더링
components.html(game_html, height=360)
