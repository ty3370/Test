import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64


# =========================================================
# STREAMLIT 설정
# =========================================================

st.set_page_config(
    page_title="Chiikawa Run!",
    page_icon="🌸",
    layout="centered"
)


# =========================================================
# 경로
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"


# =========================================================
# 이미지 → Base64
# =========================================================

def image_to_base64(filename):

    path = ASSETS / filename

    if not path.exists():
        return ""

    try:

        data = base64.b64encode(
            path.read_bytes()
        ).decode("utf-8")

        ext = path.suffix.lower()

        if ext == ".png":
            mime = "image/png"

        elif ext in [".jpg", ".jpeg"]:
            mime = "image/jpeg"

        elif ext == ".webp":
            mime = "image/webp"

        else:
            mime = "application/octet-stream"

        return f"data:{mime};base64,{data}"

    except Exception:

        return ""


# =========================================================
# 캐릭터 이미지
# =========================================================

CHARACTER1 = image_to_base64(
    "character1.png"
)

CHARACTER1_RUN2 = image_to_base64(
    "character1_run2.png"
)

CHARACTER2 = image_to_base64(
    "character2.png"
)

CHARACTER2_RUN2 = image_to_base64(
    "character2_run2.png"
)

CHARACTER3 = image_to_base64(
    "character3.png"
)

CHARACTER3_RUN2 = image_to_base64(
    "character3_run2.png"
)

BACKGROUND = image_to_base64(
    "background.jpg"
)


# =========================================================
# 파일 확인
# =========================================================

required_files = [

    "character1.png",
    "character1_run2.png",

    "character2.png",
    "character2_run2.png",

    "character3.png",
    "character3_run2.png",

    "background.jpg"
]


missing_files = [

    filename

    for filename in required_files

    if not (
        ASSETS / filename
    ).exists()
]


if missing_files:

    st.warning(
        "⚠️ 일부 이미지 파일을 찾을 수 없습니다."
    )

    st.code(
        "\n".join(
            f"assets/{filename}"
            for filename in missing_files
        )
    )

    st.caption(
        "assets 폴더 안의 파일 이름이 정확히 일치하는지 확인하세요."
    )


# =========================================================
# Streamlit 외부 CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            linear-gradient(
                180deg,
                #dff6ff 0%,
                #fff0f5 100%
            );
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2px !important;
        padding-bottom: 0 !important;
        max-width: 1000px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 게임 HTML
# =========================================================

game = r"""
<!DOCTYPE html>

<html lang="ko">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="
        width=device-width,
        initial-scale=1.0,
        maximum-scale=1.0,
        user-scalable=no
    "
>


<style>


/* =====================================================
   기본
   ===================================================== */

* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}


html,
body {

    margin: 0;
    padding: 0;

    width: 100%;
    height: 100%;

    overflow: hidden;

    background: transparent;

    font-family:
        Arial,
        sans-serif;
}


body {
    display: flex;
    justify-content: center;
    align-items: flex-start;
}


#gameWrap {

    width: 100%;

    display: flex;

    justify-content: center;

    align-items: flex-start;
}


#game {

    position: relative;

    width: min(
        920px,
        100vw
    );

    flex-shrink: 0;
}


canvas {

    width: 100%;
    height: auto;

    display: block;

    border-radius: 20px;

    background:
        #dff6ff;

    box-shadow:
        0 5px 18px
        rgba(80,60,70,.16);
}


/* =====================================================
   HUD
   ===================================================== */

.hud {

    position: absolute;

    top: 10px;

    left: 10px;
    right: 10px;

    display: flex;

    justify-content:
        space-between;

    gap: 6px;

    z-index: 5;

    pointer-events: none;
}


.hudBox {

    background:
        rgba(255,255,255,.92);

    color:
        #604850;

    font-weight:
        900;

    font-size:
        13px;

    padding:
        6px 10px;

    border-radius:
        13px;

    box-shadow:
        0 3px 8px
        rgba(0,0,0,.12);

    white-space:
        nowrap;
}


/* =====================================================
   메뉴
   ===================================================== */

#menu {

    position: absolute;

    inset: 0;

    z-index: 20;

    display: flex;

    justify-content:
        center;

    align-items:
        center;

    padding: 12px;

    background:
        rgba(255,255,255,.18);

    border-radius: 20px;

    overflow: hidden;
}


.menuCard {

    width:
        min(390px, 82%);

    max-height:
        88%;

    background:
        rgba(255,255,255,.97);

    border-radius:
        22px;

    padding:
        18px 14px;

    text-align:
        center;

    box-shadow:
        0 10px 25px
        rgba(60,40,60,.22);

    overflow:
        hidden;
}


.title {

    color:
        #5d3f47;

    font-weight:
        900;

    font-size:
        clamp(21px, 5vw, 32px);

    margin-bottom:
        8px;
}


.description {

    color:
        #76666d;

    font-size:
        clamp(11px, 2.8vw, 15px);

    line-height:
        1.34;

    margin-bottom:
        11px;
}


.startButton {

    appearance:
        none;

    -webkit-appearance:
        none;

    border:
        none;

    width:
        100%;

    padding:
        13px 18px;

    border-radius:
        15px;

    background:
        linear-gradient(
            135deg,
            #ff9abb,
            #ff6497
        );

    color:
        white;

    font-size:
        16px;

    font-weight:
        900;

    box-shadow:
        0 5px 0
        #d74d79;

    cursor:
        pointer;

    touch-action:
        manipulation;
}


.startButton:active {

    transform:
        translateY(4px);

    box-shadow:
        none;
}


/* =====================================================
   모바일 조작
   ===================================================== */

.controls {

    position:
        absolute;

    left:
        50%;

    bottom:
        8px;

    transform:
        translateX(-50%);

    display:
        flex;

    gap:
        6px;

    z-index:
        15;
}


.ctrl {

    appearance:
        none;

    -webkit-appearance:
        none;

    width:
        43px;

    height:
        39px;

    padding:
        0;

    border:
        0;

    border-radius:
        13px;

    background:
        rgba(255,255,255,.92);

    color:
        #5d4b50;

    font-size:
        18px;

    font-weight:
        900;

    box-shadow:
        0 3px 8px
        rgba(0,0,0,.13);

    touch-action:
        manipulation;
}


.ctrl:active {

    transform:
        scale(.93);
}


/* =====================================================
   작은 화면
   ===================================================== */

@media (max-width: 600px) {

    #game {

        width:
            min(
                100vw,
                920px
            );
    }


    canvas {

        border-radius:
            14px;
    }


    #menu {

        padding:
            5px;
    }


    .menuCard {

        width:
            80%;

        max-height:
            90%;

        padding:
            11px 10px;

        border-radius:
            18px;
    }


    .title {

        font-size:
            20px;

        margin-bottom:
            5px;
    }


    .description {

        font-size:
            10px;

        line-height:
            1.25;

        margin-bottom:
            7px;
    }


    .startButton {

        padding:
            9px 10px;

        font-size:
            13px;
    }


    .hud {

        top:
            5px;

        left:
            5px;

        right:
            5px;
    }


    .hudBox {

        font-size:
            9px;

        padding:
            4px 6px;
    }


    .controls {

        bottom:
            5px;

        gap:
            5px;
    }


    .ctrl {

        width:
            38px;

        height:
            34px;

        font-size:
            15px;
    }
}


/* =====================================================
   매우 작은 화면
   ===================================================== */

@media (max-height: 600px) {

    .menuCard {

        width:
            65%;

        padding:
            8px 10px;
    }


    .title {

        font-size:
            18px;
    }


    .description {

        font-size:
            9px;

        margin-bottom:
            5px;
    }


    .startButton {

        padding:
            7px 10px;

        font-size:
            12px;
    }


    .controls {

        bottom:
            3px;
    }


    .ctrl {

        width:
            34px;

        height:
            30px;

        font-size:
            13px;
    }
}

</style>

</head>


<body>


<div id="gameWrap">

<div id="game">


<canvas
    id="canvas"
    width="920"
    height="650">
</canvas>


<!-- ===================================================
     HUD
     =================================================== -->

<div class="hud">

    <div class="hudBox">

        ⭐
        <span id="score">
            0
        </span>

    </div>


    <div class="hudBox">

        🏆
        <span id="best">
            0
        </span>

    </div>


    <div class="hudBox">

        🎭
        <span id="form">
            기본
        </span>

    </div>

</div>


<!-- ===================================================
     시작 메뉴
     =================================================== -->

<div id="menu">

    <div class="menuCard">

        <div class="title">

            🌸 CHIIKAWA RUN! 🌸

        </div>


        <div class="description">

            치이카와 친구들과 함께
            달려보세요! 🏃

            <br>

            ◀ ▶ 이동 ·
            ⬆ 점프 ·
            ⬇ 숙이기

            <br>

            🎁 랜덤박스를 먹으면
            좋은 아이템 또는 나쁜 아이템 등장!

            <br>

            🪨 장애물은 점프하거나
            숙여서 피하세요!

            <br>

            ✨ 점수에 따라 모습이 바뀝니다.

        </div>


        <button
            id="startButton"
            class="startButton"
            type="button"
        >

            START RUN! 🏃

        </button>

    </div>

</div>


<!-- ===================================================
     모바일 조작 버튼
     =================================================== -->

<div class="controls">

    <button
        class="ctrl"
        id="leftButton"
        type="button"
    >
        ◀
    </button>


    <button
        class="ctrl"
        id="jumpButton"
        type="button"
    >
        ⬆
    </button>


    <button
        class="ctrl"
        id="rightButton"
        type="button"
    >
        ▶
    </button>


    <button
        class="ctrl"
        id="slideButton"
        type="button"
    >
        ⬇
    </button>

</div>


</div>

</div>


<script>


// =====================================================
// 이미지
// =====================================================

const character1 =
    new Image();

character1.src =
    "__CHARACTER1__";


const character1Run2 =
    new Image();

character1Run2.src =
    "__CHARACTER1_RUN2__";


const character2 =
    new Image();

character2.src =
    "__CHARACTER2__";


const character2Run2 =
    new Image();

character2Run2.src =
    "__CHARACTER2_RUN2__";


const character3 =
    new Image();

character3.src =
    "__CHARACTER3__";


const character3Run2 =
    new Image();

character3Run2.src =
    "__CHARACTER3_RUN2__";


const background =
    new Image();

background.src =
    "__BACKGROUND__";


// =====================================================
// Canvas
// =====================================================

const canvas =
    document.getElementById(
        "canvas"
    );


const ctx =
    canvas.getContext(
        "2d"
    );


const WIDTH =
    canvas.width;


const HEIGHT =
    canvas.height;


// =====================================================
// 화면 크기 최적화
// =====================================================

function fitGameToScreen() {

    const game =
        document.getElementById(
            "game"
        );


    if (!game)
        return;


    let availableWidth =
        window.innerWidth;


    let availableHeight =
        window.innerHeight;


    /*
     * Streamlit iframe 안에서 실행되기 때문에
     * 가능한 경우 부모 창의 실제 높이를 사용한다.
     */

    try {

        if (
            window.parent &&
            window.parent.innerHeight
        ) {

            availableHeight =
                window.parent.innerHeight;
        }

    }
    catch (error) {

        // iframe 접근이 막힌 경우
        // 현재 iframe 크기를 그대로 사용
    }


    /*
     * 920 × 650 비율을 유지한다.
     *
     * 가로가 좁으면 가로 기준으로 축소.
     * 세로가 좁으면 세로 기준으로 축소.
     */

    const widthByHeight =
        availableHeight *
        WIDTH /
        HEIGHT;


    const finalWidth =
        Math.min(
            920,
            availableWidth,
            widthByHeight
        );


    game.style.width =
        Math.max(
            280,
            finalWidth
        ) + "px";
}


window.addEventListener(
    "resize",
    fitGameToScreen
);


window.addEventListener(
    "orientationchange",
    function() {

        setTimeout(
            fitGameToScreen,
            100
        );
    }
);


fitGameToScreen();


// =====================================================
// DOM
// =====================================================

const startButton =
    document.getElementById(
        "startButton"
    );


const leftButton =
    document.getElementById(
        "leftButton"
    );


const rightButton =
    document.getElementById(
        "rightButton"
    );


const jumpButton =
    document.getElementById(
        "jumpButton"
    );


const slideButton =
    document.getElementById(
        "slideButton"
    );


// =====================================================
// 게임 상태
// =====================================================

let running =
    false;


let score =
    0;


let best =
    Number(
        localStorage.getItem(
            "chiikawa_best"
        ) || 0
    );


let speed =
    7;


let distance =
    0;


let spawnTimer =
    45;


let objects =
    [];


let particles =
    [];


// =====================================================
// 달리기 애니메이션
// =====================================================

let animationFrame =
    0;


let animationTimer =
    0;


// =====================================================
// 도로 애니메이션
// =====================================================

let roadOffset =
    0;


let sceneryOffset =
    0;


// =====================================================
// 배경 움직임
// =====================================================

let skyOffset =
    0;


// =====================================================
// 원근
// =====================================================

const HORIZON_Y =
    145;


const HORIZON_X =
    460;


// 실제 플레이어 근처의 레인 중심
const BOTTOM_LANES = [
    300,
    460,
    620
];


// 멀리 있는 레인의 중심
const HORIZON_LANES = [
    450,
    460,
    470
];


// =====================================================
// 플레이어
// =====================================================

let player = {

    lane:
        1,

    x:
        460,

    targetX:
        460,

    y:
        515,

    vy:
        0,

    jumping:
        false,

    sliding:
        false,

    slideTimer:
        0,

    giant:
        false,

    giantTimer:
        0,

    shield:
        false,

    shieldTimer:
        0,

    form:
        0,

    turning:
        false,

    turnTimer:
        0,

    rotation:
        0
};


// =====================================================
// 시작
// =====================================================

function startGame() {

    running =
        true;


    score =
        0;


    speed =
        7;


    distance =
        0;


    spawnTimer =
        45;


    objects =
        [];


    particles =
        [];


    animationFrame =
        0;


    animationTimer =
        0;


    roadOffset =
        0;


    sceneryOffset =
        0;


    skyOffset =
        0;


    player = {

        lane:
            1,

        x:
            460,

        targetX:
            460,

        y:
            515,

        vy:
            0,

        jumping:
            false,

        sliding:
            false,

        slideTimer:
            0,

        giant:
            false,

        giantTimer:
            0,

        shield:
            false,

        shieldTimer:
            0,

        form:
            0,

        turning:
            false,

        turnTimer:
            0,

        rotation:
            0
    };


    document
        .getElementById(
            "form"
        )
        .textContent =
            "기본";


    document
        .getElementById(
            "menu"
        )
        .style.display =
            "none";
}


// =====================================================
// 터치 버튼
// =====================================================

function touchAction(
    element,
    action
) {

    element.addEventListener(
        "pointerdown",
        function(event) {

            event.preventDefault();

            action();
        }
    );
}


touchAction(
    startButton,
    startGame
);


touchAction(
    leftButton,
    moveLeft
);


touchAction(
    rightButton,
    moveRight
);


touchAction(
    jumpButton,
    jump
);


touchAction(
    slideButton,
    slide
);


// =====================================================
// 키보드
// =====================================================

document.addEventListener(
    "keydown",
    function(event) {

        /*
         * 왼쪽
         */

        if (
            event.key ===
            "ArrowLeft"
        ) {

            moveLeft();

            event.preventDefault();
        }


        /*
         * 오른쪽
         */

        if (
            event.key ===
            "ArrowRight"
        ) {

            moveRight();

            event.preventDefault();
        }


        /*
         * 위쪽 = 점프
         */

        if (
            event.key ===
            "ArrowUp" ||
            event.code ===
            "Space"
        ) {

            jump();

            event.preventDefault();
        }


        /*
         * 아래쪽 = 숙이기
         */

        if (
            event.key ===
            "ArrowDown"
        ) {

            slide();

            event.preventDefault();
        }

    }
);


// =====================================================
// 이동
// =====================================================

function moveLeft() {

    if (!running)
        return;


    if (
        player.lane > 0
    ) {

        player.lane--;

        player.targetX =
            BOTTOM_LANES[
                player.lane
            ];
    }
}


function moveRight() {

    if (!running)
        return;


    if (
        player.lane < 2
    ) {

        player.lane++;

        player.targetX =
            BOTTOM_LANES[
                player.lane
            ];
    }
}


// =====================================================
// 점프
// =====================================================

function jump() {

    if (!running)
        return;


    if (
        !player.jumping
    ) {

        player.jumping =
            true;

        player.vy =
            -18;

        player.rotation =
            0;
    }
}


// =====================================================
// 숙이기
// =====================================================

function slide() {

    if (!running)
        return;


    if (
        !player.jumping
    ) {

        player.sliding =
            true;

        player.slideTimer =
            38;
    }
}


// =====================================================
// 원근 좌표
// =====================================================

function perspectivePoint(
    lane,
    progress
) {

    progress =
        Math.max(
            0,
            Math.min(
                1,
                progress
            )
        );


    /*
     * x:
     * 멀리에서는 중앙에 모이고
     * 가까워질수록 레인 간격이 넓어진다.
     */

    const x =
        HORIZON_LANES[lane]
        +
        (
            BOTTOM_LANES[lane]
            -
            HORIZON_LANES[lane]
        )
        *
        progress;


    /*
     * y:
     * 먼 곳은 천천히,
     * 가까워질수록 빠르게 커지는
     * 원근 효과.
     */

    const curved =
        Math.pow(
            progress,
            1.18
        );


    const y =
        HORIZON_Y
        +
        (
            HEIGHT -
            HORIZON_Y
        )
        *
        curved;


    return {
        x:
            x,

        y:
            y
    };
}


// =====================================================
// 오브젝트 생성
// =====================================================

function spawnObject() {

    const lane =
        Math.floor(
            Math.random() * 3
        );


    const r =
        Math.random();


    let type;


    let item =
        null;


    /*
     * 0.00 ~ 0.30
     * 뛰어넘는 장애물
     */

    if (
        r < 0.30
    ) {

        type =
            "jumpObstacle";
    }


    /*
     * 0.30 ~ 0.45
     * 숙여야 하는 장애물
     */

    else if (
        r < 0.45
    ) {

        type =
            "slideObstacle";
    }


    /*
     * 0.45 ~ 0.70
     * 랜덤박스
     */

    else if (
        r < 0.70
    ) {

        type =
            "box";
    }


    /*
     * 0.70 ~ 1.00
     * 아이템
     */

    else {

        type =
            "item";


        const q =
            Math.random();


        if (
            q < 0.18
        )

            item =
                "giant";


        else if (
            q < 0.36
        )

            item =
                "score";


        else if (
            q < 0.52
        )

            item =
                "shield";


        else if (
            q < 0.68
        )

            item =
                "slow";


        else if (
            q < 0.84
        )

            item =
                "speed";


        else

            item =
                "bad";
    }


    objects.push({

        lane:
            lane,

        progress:
            0.015,

        type:
            type,

        item:
            item
    });
}


// =====================================================
// 아이템
// =====================================================

function getItem(item) {

    if (
        item ===
        "giant"
    ) {

        player.giant =
            true;

        player.giantTimer =
            420;
    }


    if (
        item ===
        "score"
    ) {

        score +=
            500;
    }


    if (
        item ===
        "shield"
    ) {

        player.shield =
            true;

        player.shieldTimer =
            360;
    }


    if (
        item ===
        "slow"
    ) {

        speed =
            Math.max(
                4,
                speed - 2
            );
    }


    if (
        item ===
        "speed"
    ) {

        score +=
            250;

        speed =
            Math.min(
                16,
                speed + 1
            );
    }


    if (
        item ===
        "bad"
    ) {

        score =
            Math.max(
                0,
                score - 350
            );

        speed =
            Math.min(
                16,
                speed + 2
            );
    }
}


// =====================================================
// 랜덤박스
// =====================================================

function openBox(obj) {

    const r =
        Math.random();


    let item;


    if (
        r < 0.20
    )

        item =
            "giant";


    else if (
        r < 0.40
    )

        item =
            "score";


    else if (
        r < 0.58
    )

        item =
            "shield";


    else if (
        r < 0.72
    )

        item =
            "slow";


    else if (
        r < 0.86
    )

        item =
            "speed";


    else

        item =
            "bad";


    getItem(
        item
    );


    const point =
        perspectivePoint(
            obj.lane,
            obj.progress
        );


    burst(
        point.x,
        point.y,
        "#ffd447",
        22
    );
}


// =====================================================
// 충돌 검사
// =====================================================

function objectIsAtPlayer(
    obj
) {

    /*
     * progress가 1에 가까워질수록
     * 플레이어에게 가까워진 것이다.
     */

    if (
        obj.progress < 0.82
    ) {

        return false;
    }


    if (
        obj.progress > 1.05
    ) {

        return false;
    }


    return (
        player.lane ===
        obj.lane
    );
}


// =====================================================
// 변신
// =====================================================

function transformationCheck() {

    let newForm =
        0;


    if (
        score >= 5000
    ) {

        newForm =
            2;
    }

    else if (
        score >= 2500
    ) {

        newForm =
            1;
    }


    if (
        newForm >
        player.form
    ) {

        player.form =
            newForm;


        player.turning =
            true;


        player.turnTimer =
            120;


        burst(
            player.x,
            player.y - 70,
            "#ff9fc0",
            30
        );
    }


    let text =
        "기본";


    if (
        player.form ===
        1
    )

        text =
            "✨ 변신";


    if (
        player.form ===
        2
    )

        text =
            "👑 최종";


    document
        .getElementById(
            "form"
        )
        .textContent =
            text;
}


// =====================================================
// UPDATE
// =====================================================

function update() {

    if (!running)
        return;


    // -----------------------------------------------
    // 거리
    // -----------------------------------------------

    distance +=
        speed;


    // -----------------------------------------------
    // 점수
    // -----------------------------------------------

    score +=
        0.28;


    // -----------------------------------------------
    // 속도 증가
    // -----------------------------------------------

    speed =
        Math.min(
            16,
            7 +
            distance / 6500
        );


    // -----------------------------------------------
    // 변신
    // -----------------------------------------------

    transformationCheck();


    // -----------------------------------------------
    // 레인 이동
    // -----------------------------------------------

    player.x +=
        (
            player.targetX -
            player.x
        ) * 0.2;


    // -----------------------------------------------
    // 점프
    // -----------------------------------------------

    if (
        player.jumping
    ) {

        player.vy +=
            1;

        player.y +=
            player.vy;


        if (
            player.y >=
            515
        ) {

            player.y =
                515;

            player.vy =
                0;

            player.jumping =
                false;
        }
    }


    // -----------------------------------------------
    // 숙이기
    // -----------------------------------------------

    if (
        player.sliding
    ) {

        player.slideTimer--;


        if (
            player.slideTimer <= 0
        ) {

            player.sliding =
                false;
        }
    }


    // -----------------------------------------------
    // 거대화
    // -----------------------------------------------

    if (
        player.giant
    ) {

        player.giantTimer--;


        if (
            player.giantTimer <= 0
        ) {

            player.giant =
                false;
        }
    }


    // -----------------------------------------------
    // 보호막
    // -----------------------------------------------

    if (
        player.shield
    ) {

        player.shieldTimer--;


        if (
            player.shieldTimer <= 0
        ) {

            player.shield =
                false;
        }
    }


    // -----------------------------------------------
    // 변신 회전
    // -----------------------------------------------

    if (
        player.turning
    ) {

        player.turnTimer--;


        if (
            player.turnTimer <= 0
        ) {

            player.turning =
                false;
        }
    }


    // =================================================
    // 달리기 애니메이션
    // =================================================

    animationTimer++;


    if (
        animationTimer >= 8
    ) {

        animationTimer =
            0;


        animationFrame =
            animationFrame === 0
                ? 1
                : 0;
    }


    // =================================================
    // 도로 흐름
    // =================================================

    roadOffset +=
        speed;


    if (
        roadOffset >= 100
    ) {

        roadOffset -=
            100;
    }


    // =================================================
    // 주변 풍경 흐름
    // =================================================

    sceneryOffset +=
        speed * 1.25;


    if (
        sceneryOffset >= 120
    ) {

        sceneryOffset -=
            120;
    }


    // =================================================
    // 하늘의 아주 약한 흐름
    // =================================================

    skyOffset +=
        speed * 0.12;


    if (
        skyOffset >= HEIGHT
    ) {

        skyOffset -=
            HEIGHT;
    }


    // =================================================
    // 오브젝트 생성
    // =================================================

    spawnTimer--;


    if (
        spawnTimer <= 0
    ) {

        spawnObject();


        spawnTimer =
            Math.max(
                30,
                68 -
                speed * 1.8
            );
    }


    // =================================================
    // 오브젝트 접근
    // =================================================

    objects.forEach(
        function(obj) {

            /*
             * 멀리 있는 물체는 천천히 움직이고
             * 가까워질수록 화면에서 빠르게 이동한다.
             */

            const distanceFactor =
                0.65 +
                obj.progress * 1.45;


            obj.progress +=
                (
                    speed *
                    0.00165 *
                    distanceFactor
                );
        }
    );


    // =================================================
    // 충돌
    // =================================================

    for (
        let i =
            objects.length - 1;

        i >= 0;

        i--
    ) {

        const obj =
            objects[i];


        if (
            !objectIsAtPlayer(
                obj
            )
        ) {

            continue;
        }


        // ---------------------------------------------
        // 랜덤박스
        // ---------------------------------------------

        if (
            obj.type ===
            "box"
        ) {

            openBox(
                obj
            );


            objects.splice(
                i,
                1
            );


            continue;
        }


        // ---------------------------------------------
        // 아이템
        // ---------------------------------------------

        if (
            obj.type ===
            "item"
        ) {

            const point =
                perspectivePoint(
                    obj.lane,
                    obj.progress
                );


            getItem(
                obj.item
            );


            burst(
                point.x,
                point.y,
                "#fff0a6",
                12
            );


            objects.splice(
                i,
                1
            );


            continue;
        }


        // ---------------------------------------------
        // 뛰어넘는 장애물
        // ---------------------------------------------

        if (
            obj.type ===
            "jumpObstacle"
        ) {

            if (
                player.jumping
            ) {

                objects.splice(
                    i,
                    1
                );

                continue;
            }


            if (
                player.giant
            ) {

                score +=
                    200;


                objects.splice(
                    i,
                    1
                );

                continue;
            }


            if (
                player.shield
            ) {

                player.shield =
                    false;


                objects.splice(
                    i,
                    1
                );

                continue;
            }


            gameOver();

            return;
        }


        // ---------------------------------------------
        // 숙여야 하는 장애물
        // ---------------------------------------------

        if (
            obj.type ===
            "slideObstacle"
        ) {

            if (
                player.sliding
            ) {

                objects.splice(
                    i,
                    1
                );

                continue;
            }


            if (
                player.giant
            ) {

                /*
                 * 거대화 상태에서는
                 * 숙이기 장애물을 통과할 수 없게 한다.
                 */

                gameOver();

                return;
            }


            if (
                player.shield
            ) {

                player.shield =
                    false;


                objects.splice(
                    i,
                    1
                );

                continue;
            }


            gameOver();

            return;
        }
    }


    // =================================================
    // 화면 밖 제거
    // =================================================

    objects =
        objects.filter(
            function(obj) {

                return (
                    obj.progress <
                    1.12
                );
            }
        );


    // =================================================
    // 파티클
    // =================================================

    updateParticles();
}


// =====================================================
// GAME OVER
// =====================================================

function gameOver() {

    running =
        false;


    const finalScore =
        Math.floor(
            score
        );


    if (
        finalScore >
        best
    ) {

        best =
            finalScore;


        localStorage.setItem(
            "chiikawa_best",
            best
        );
    }


    document
        .getElementById(
            "menu"
        )
        .innerHTML = `

        <div class="menuCard">

            <div class="title">

                💥 GAME OVER

            </div>


            <div class="description">

                최종 점수

                <br>

                <b
                    style="
                        font-size:34px;
                        color:#ff6797;
                    "
                >

                    ${finalScore}

                </b>

                <br><br>

                🏆 최고 점수
                ${best}

            </div>


            <button
                id="restartButton"
                class="startButton"
                type="button"
            >

                다시 달리기! 🏃

            </button>

        </div>
    `;


    document
        .getElementById(
            "menu"
        )
        .style.display =
            "flex";


    document
        .getElementById(
            "restartButton"
        )
        .addEventListener(
            "pointerdown",
            function(event) {

                event.preventDefault();

                startGame();
            }
        );
}


// =====================================================
// 이미지 로딩 확인
// =====================================================

function imageReady(
    image
) {

    return (

        image &&

        image.complete &&

        image.naturalWidth > 0
    );
}


// =====================================================
// BACKGROUND
// =====================================================

function drawBackground() {

    /*
     * background.jpg는 하늘/주변 배경으로 사용한다.
     *
     * 이미지가 있으면 화면에 채우고,
     * 도로는 그 위에 별도로 원근형으로 그린다.
     */

    if (
        imageReady(
            background
        )
    ) {

        /*
         * 배경을 약하게 움직여서
         * 완전히 정지된 느낌을 줄인다.
         */

        const drift =
            skyOffset * 0.08;


        ctx.drawImage(
            background,
            0,
            drift - 30,
            WIDTH,
            HEIGHT
        );

    }
    else {

        /*
         * background.jpg가 없을 경우
         * 기본 하늘을 생성한다.
         */

        const gradient =
            ctx.createLinearGradient(
                0,
                0,
                0,
                HEIGHT
            );


        gradient.addColorStop(
            0,
            "#91dfff"
        );


        gradient.addColorStop(
            0.55,
            "#dff7ff"
        );


        gradient.addColorStop(
            1,
            "#d7efc9"
        );


        ctx.fillStyle =
            gradient;


        ctx.fillRect(
            0,
            0,
            WIDTH,
            HEIGHT
        );
    }


    // =================================================
    // 먼 하늘
    // =================================================

    drawHorizon();


    // =================================================
    // 도로
    // =================================================

    drawRoad();


    // =================================================
    // 주변 풍경
    // =================================================

    drawSideScenery();
}


// =====================================================
// 수평선
// =====================================================

function drawHorizon() {

    /*
     * 먼 곳의 나무/산 실루엣
     */

    ctx.save();


    ctx.globalAlpha =
        0.42;


    ctx.fillStyle =
        "#9dcc9d";


    ctx.beginPath();


    ctx.moveTo(
        0,
        HORIZON_Y + 25
    );


    ctx.lineTo(
        80,
        HORIZON_Y - 5
    );


    ctx.lineTo(
        150,
        HORIZON_Y + 18
    );


    ctx.lineTo(
        230,
        HORIZON_Y - 15
    );


    ctx.lineTo(
        310,
        HORIZON_Y + 20
    );


    ctx.lineTo(
        380,
        HORIZON_Y
    );


    ctx.lineTo(
        460,
        HORIZON_Y + 12
    );


    ctx.lineTo(
        540,
        HORIZON_Y
    );


    ctx.lineTo(
        620,
        HORIZON_Y + 20
    );


    ctx.lineTo(
        700,
        HORIZON_Y - 15
    );


    ctx.lineTo(
        780,
        HORIZON_Y + 18
    );


    ctx.lineTo(
        860,
        HORIZON_Y - 5
    );


    ctx.lineTo(
        920,
        HORIZON_Y + 25
    );


    ctx.lineTo(
        920,
        HORIZON_Y + 70
    );


    ctx.lineTo(
        0,
        HORIZON_Y + 70
    );


    ctx.closePath();


    ctx.fill();


    ctx.restore();
}


// =====================================================
// 원근 도로
// =====================================================

function drawRoad() {

    /*
     * 핵심:
     *
     * 기존 도로처럼 y=300에서 갑자기
     * 시작하는 것이 아니라
     *
     *      소실점
     *        ↓
     *       /\
     *      /  \
     *     /    \
     *    /      \
     *   /        \
     *  /          \
     *
     * 형태로 화면 끝까지 이어진다.
     */

    const roadTopY =
        HORIZON_Y;


    const roadTopLeft =
        410;


    const roadTopRight =
        510;


    const roadBottomLeft =
        -80;


    const roadBottomRight =
        1000;


    // -----------------------------------------------
    // 도로 그림자
    // -----------------------------------------------

    ctx.fillStyle =
        "rgba(80,65,60,.18)";


    ctx.beginPath();


    ctx.moveTo(
        roadTopLeft - 8,
        roadTopY
    );


    ctx.lineTo(
        roadTopRight + 8,
        roadTopY
    );


    ctx.lineTo(
        roadBottomRight,
        HEIGHT
    );


    ctx.lineTo(
        roadBottomLeft,
        HEIGHT
    );


    ctx.closePath();


    ctx.fill();


    // -----------------------------------------------
    // 실제 도로
    // -----------------------------------------------

    const roadGradient =
        ctx.createLinearGradient(
            0,
            roadTopY,
            0,
            HEIGHT
        );


    roadGradient.addColorStop(
        0,
        "#cbbfae"
    );


    roadGradient.addColorStop(
        0.45,
        "#c1b19d"
    );


    roadGradient.addColorStop(
        1,
        "#aa9a87"
    );


    ctx.fillStyle =
        roadGradient;


    ctx.beginPath();


    ctx.moveTo(
        roadTopLeft,
        roadTopY
    );


    ctx.lineTo(
        roadTopRight,
        roadTopY
    );


    ctx.lineTo(
        roadBottomRight,
        HEIGHT
    );


    ctx.lineTo(
        roadBottomLeft,
        HEIGHT
    );


    ctx.closePath();


    ctx.fill();


    // -----------------------------------------------
    // 도로 가장자리
    // -----------------------------------------------

    ctx.strokeStyle =
        "rgba(255,255,255,.7)";


    ctx.lineWidth =
        5;


    ctx.beginPath();


    ctx.moveTo(
        roadTopLeft,
        roadTopY
    );


    ctx.lineTo(
        roadBottomLeft,
        HEIGHT
    );


    ctx.stroke();


    ctx.beginPath();


    ctx.moveTo(
        roadTopRight,
        roadTopY
    );


    ctx.lineTo(
        roadBottomRight,
        HEIGHT
    );


    ctx.stroke();


    // -----------------------------------------------
    // 움직이는 중앙 차선
    // -----------------------------------------------

    drawPerspectiveLane(
        0
    );


    drawPerspectiveLane(
        1
    );


    // -----------------------------------------------
    // 움직이는 노면 표시
    // -----------------------------------------------

    drawRoadTexture();
}


// =====================================================
// 원근 차선
// =====================================================

function drawPerspectiveLane(
    laneLine
) {

    /*
     * laneLine = 0
     * 왼쪽 중앙선
     *
     * laneLine = 1
     * 오른쪽 중앙선
     */

    const topX =
        laneLine === 0
            ? 445
            : 475;


    const bottomX =
        laneLine === 0
            ? 380
            : 540;


    ctx.save();


    ctx.strokeStyle =
        "rgba(255,255,255,.78)";


    ctx.lineCap =
        "round";


    /*
     * 작은 점선이 먼 곳에서 시작해
     * 아래로 빠르게 지나간다.
     */

    for (
        let i = -1;
        i < 14;
        i++
    ) {

        let progress =
            (
                i * 0.085
                +
                roadOffset / 100 * 0.085
            );


        progress =
            progress % 1;


        if (
            progress < 0
        ) {

            progress +=
                1;
        }


        /*
         * 화면 아래로 갈수록
         * 차선이 넓어지는 효과
         */

        const p1 =
            progress;


        const p2 =
            Math.min(
                1,
                progress + 0.045
            );


        const a =
            perspectiveRoadX(
                topX,
                bottomX,
                p1
            );


        const b =
            perspectiveRoadX(
                topX,
                bottomX,
                p2
            );


        const y1 =
            perspectiveRoadY(
                p1
            );


        const y2 =
            perspectiveRoadY(
                p2
            );


        ctx.lineWidth =
            2 +
            p1 * 7;


        ctx.beginPath();


        ctx.moveTo(
            a,
            y1
        );


        ctx.lineTo(
            b,
            y2
        );


        ctx.stroke();
    }


    ctx.restore();
}


// =====================================================
// 도로 X 원근
// =====================================================

function perspectiveRoadX(
    topX,
    bottomX,
    progress
) {

    return (
        topX +
        (
            bottomX -
            topX
        ) *
        progress
    );
}


// =====================================================
// 도로 Y 원근
// =====================================================

function perspectiveRoadY(
    progress
) {

    return (
        HORIZON_Y +
        (
            HEIGHT -
            HORIZON_Y
        )
        *
        Math.pow(
            progress,
            1.16
        )
    );
}


// =====================================================
// 도로 노면 속도 표시
// =====================================================

function drawRoadTexture() {

    ctx.save();


    ctx.globalAlpha =
        0.18;


    ctx.strokeStyle =
        "#ffffff";


    ctx.lineWidth =
        3;


    for (
        let i = 0;
        i < 18;
        i++
    ) {

        let progress =
            (
                i * 0.075
                +
                roadOffset / 100 * 0.075
            ) % 1;


        const y =
            perspectiveRoadY(
                progress
            );


        const leftX =
            perspectiveRoadX(
                410,
                80,
                progress
            );


        const rightX =
            perspectiveRoadX(
                510,
                840,
                progress
            );


        const center =
            (
                leftX +
                rightX
            ) / 2;


        const width =
            (
                rightX -
                leftX
            ) * 0.12;


        ctx.beginPath();


        ctx.moveTo(
            center - width,
            y
        );


        ctx.lineTo(
            center + width,
            y
        );


        ctx.stroke();
    }


    ctx.restore();
}


// =====================================================
// 주변 풍경
// =====================================================

function drawSideScenery() {

    /*
     * 도로 양옆의 나무가
     * 멀리서 작게 보였다가
     * 아래로 빠르게 지나간다.
     */

    for (
        let i = -1;
        i < 11;
        i++
    ) {

        let progress =
            (
                i * 0.11
                +
                sceneryOffset / 120 * 0.11
            ) % 1;


        if (
            progress < 0
        ) {

            progress +=
                1;
        }


        const y =
            perspectiveRoadY(
                progress
            );


        const leftRoad =
            perspectiveRoadX(
                410,
                -80,
                progress
            );


        const rightRoad =
            perspectiveRoadX(
                510,
                1000,
                progress
            );


        const scale =
            0.25 +
            progress * 1.5;


        const leftX =
            leftRoad -
            25 -
            progress * 45;


        const rightX =
            rightRoad +
            25 +
            progress * 45;


        drawBush(
            leftX,
            y,
            scale
        );


        drawBush(
            rightX,
            y + 18,
            scale
        );
    }
}


// =====================================================
// 덤불
// =====================================================

function drawBush(
    x,
    y,
    scale
) {

    ctx.save();


    ctx.translate(
        x,
        y
    );


    ctx.scale(
        scale,
        scale
    );


    ctx.fillStyle =
        "#8fc987";


    ctx.beginPath();


    ctx.arc(
        -18,
        0,
        18,
        0,
        Math.PI * 2
    );


    ctx.arc(
        0,
        -12,
        23,
        0,
        Math.PI * 2
    );


    ctx.arc(
        21,
        0,
        18,
        0,
        Math.PI * 2
    );


    ctx.fill();


    ctx.fillStyle =
        "#6db673";


    ctx.beginPath();


    ctx.arc(
        -8,
        -7,
        7,
        0,
        Math.PI * 2
    );


    ctx.arc(
        13,
        -8,
        6,
        0,
        Math.PI * 2
    );


    ctx.fill();


    ctx.restore();
}


// =====================================================
// 원근 장애물
// =====================================================

function drawObstacle(
    obj
) {

    const point =
        perspectivePoint(
            obj.lane,
            obj.progress
        );


    /*
     * 멀리 있을 때 작고
     * 가까이 있을 때 크게
     */

    const scale =
        0.18 +
        obj.progress * 1.55;


    if (
        obj.type ===
        "jumpObstacle"
    ) {

        drawJumpObstacle(
            point.x,
            point.y,
            scale
        );

    }
    else if (
        obj.type ===
        "slideObstacle"
    ) {

        drawSlideObstacle(
            point.x,
            point.y,
            scale
        );
    }
}


// =====================================================
// 뛰어넘는 장애물
// =====================================================

function drawJumpObstacle(
    x,
    y,
    scale
) {

    const width =
        48 * scale;


    const height =
        34 * scale;


    /*
     * 그림자
     */

    ctx.fillStyle =
        "rgba(60,50,50,.22)";


    ctx.beginPath();


    ctx.ellipse(
        x,
        y + 4 * scale,
        width * 0.65,
        7 * scale,
        0,
        0,
        Math.PI * 2
    );


    ctx.fill();


    /*
     * 장애물
     */

    ctx.fillStyle =
        "#ff779e";


    ctx.strokeStyle =
        "#67404a";


    ctx.lineWidth =
        Math.max(
            2,
            4 * scale
        );


    ctx.beginPath();


    ctx.roundRect(
        x - width / 2,
        y - height,
        width,
        height,
        8 * scale
    );


    ctx.fill();


    ctx.stroke();


    /*
     * 경고 표시
     */

    ctx.fillStyle =
        "white";


    ctx.font =
        `bold ${Math.max(9, 20 * scale)}px Arial`;


    ctx.textAlign =
        "center";


    ctx.textBaseline =
        "middle";


    ctx.fillText(
        "!",
        x,
        y - height / 2
    );
}


// =====================================================
// 숙여야 하는 장애물
// =====================================================

function drawSlideObstacle(
    x,
    y,
    scale
) {

    const postHeight =
        75 * scale;


    const beamWidth =
        76 * scale;


    const beamHeight =
        18 * scale;


    /*
     * 그림자
     */

    ctx.fillStyle =
        "rgba(60,50,50,.22)";


    ctx.beginPath();


    ctx.ellipse(
        x,
        y + 3 * scale,
        beamWidth * 0.65,
        7 * scale,
        0,
        0,
        Math.PI * 2
    );


    ctx.fill();


    /*
     * 양쪽 기둥
     */

    ctx.fillStyle =
        "#8c70b9";


    ctx.strokeStyle =
        "#5a466f";


    ctx.lineWidth =
        Math.max(
            2,
            3 * scale
        );


    ctx.fillRect(
        x -
        beamWidth / 2,
        y -
        postHeight,
        10 * scale,
        postHeight
    );


    ctx.strokeRect(
        x -
        beamWidth / 2,
        y -
        postHeight,
        10 * scale,
        postHeight
    );


    ctx.fillRect(
        x +
        beamWidth / 2 -
        10 * scale,
        y -
        postHeight,
        10 * scale,
        postHeight
    );


    ctx.strokeRect(
        x +
        beamWidth / 2 -
        10 * scale,
        y -
        postHeight,
        10 * scale,
        postHeight
    );


    /*
     * 위쪽 바
     */

    ctx.fillStyle =
        "#ff7f9f";


    ctx.beginPath();


    ctx.roundRect(
        x -
        beamWidth / 2,
        y -
        postHeight,
        beamWidth,
        beamHeight,
        5 * scale
    );


    ctx.fill();


    ctx.stroke();


    /*
     * 아래쪽으로 내려가라는 표시
     */

    ctx.fillStyle =
        "white";


    ctx.font =
        `bold ${Math.max(8, 18 * scale)}px Arial`;


    ctx.textAlign =
        "center";


    ctx.textBaseline =
        "middle";


    ctx.fillText(
        "↓",
        x,
        y -
        postHeight +
        beamHeight / 2
    );
}


// =====================================================
// 랜덤박스
// =====================================================

function drawBox(
    obj
) {

    const point =
        perspectivePoint(
            obj.lane,
            obj.progress
        );


    const scale =
        0.20 +
        obj.progress * 1.45;


    const size =
        42 * scale;


    /*
     * 그림자
     */

    ctx.fillStyle =
        "rgba(50,40,40,.2)";


    ctx.beginPath();


    ctx.ellipse(
        point.x,
        point.y + 3 * scale,
        size * 0.65,
        6 * scale,
        0,
        0,
        Math.PI * 2
    );


    ctx.fill();


    /*
     * 박스
     */

    ctx.fillStyle =
        "#ffd447";


    ctx.strokeStyle =
        "#9b7430";


    ctx.lineWidth =
        Math.max(
            2,
            4 * scale
        );


    ctx.fillRect(
        point.x -
        size / 2,
        point.y -
        size,
        size,
        size
    );


    ctx.strokeRect(
        point.x -
        size / 2,
        point.y -
        size,
        size,
        size
    );


    ctx.fillStyle =
        "white";


    ctx.font =
        `bold ${Math.max(9, 25 * scale)}px Arial`;


    ctx.textAlign =
        "center";


    ctx.textBaseline =
        "middle";


    ctx.fillText(
        "?",
        point.x,
        point.y -
        size / 2
    );
}


// =====================================================
// 아이템
// =====================================================

function drawItem(
    obj
) {

    const point =
        perspectivePoint(
            obj.lane,
            obj.progress
        );


    /*
     * 원근에 따라 크기가 변한다.
     */

    const scale =
        0.28 +
        obj.progress * 1.35;


    const icons = {

        giant:
            "🍄",

        score:
            "💎",

        shield:
            "🛡️",

        slow:
            "🐌",

        speed:
            "⚡",

        bad:
            "💀"
    };


    /*
     * 아이템 그림자
     */

    ctx.fillStyle =
        "rgba(50,40,40,.18)";


    ctx.beginPath();


    ctx.ellipse(
        point.x,
        point.y + 4 * scale,
        22 * scale,
        6 * scale,
        0,
        0,
        Math.PI * 2
    );


    ctx.fill();


    /*
     * 아이템
     */

    ctx.font =
        `${Math.max(12, 42 * scale)}px Arial`;


    ctx.textAlign =
        "center";


    ctx.textBaseline =
        "middle";


    ctx.fillText(
        icons[obj.item],
        point.x,
        point.y -
        15 * scale
    );
}


// =====================================================
// 플레이어
// =====================================================

function drawPlayer() {

    /*
     * 원본 기능 유지:
     *
     * 기본:
     * character1
     *
     * 변신:
     * character3
     */

    let image;


    if (
        player.form >= 1
    ) {

        image =
            animationFrame === 0
                ? character3
                : character3Run2;

    }
    else {

        image =
            animationFrame === 0
                ? character1
                : character1Run2;
    }


    let scale =
        player.giant
            ? 1.55
            : 1;


    let width =
        105 * scale;


    let height =
        120 * scale;


    if (
        player.sliding
    ) {

        width =
            110;

        height =
            70;
    }


    ctx.save();


    ctx.translate(
        player.x,
        player.y
    );


    /*
     * 변신 연출
     */

    if (
        player.turning
    ) {

        ctx.rotate(
            Math.PI
        );
    }


    /*
     * 캐릭터
     */

    if (
        imageReady(
            image
        )
    ) {

        ctx.drawImage(
            image,

            -width / 2,

            -height,

            width,

            height
        );
    }


    /*
     * 최종 왕관
     */

    if (
        player.form >= 2
    ) {

        ctx.font =
            "30px Arial";


        ctx.textAlign =
            "center";


        ctx.fillText(
            "👑",
            0,
            -height - 8
        );
    }


    /*
     * 거대화
     */

    if (
        player.giant
    ) {

        ctx.fillStyle =
            "#ffb52e";


        ctx.font =
            "bold 19px Arial";


        ctx.textAlign =
            "center";


        ctx.fillText(
            "GIANT!",
            0,
            -height - 12
        );
    }


    /*
     * 보호막
     */

    if (
        player.shield
    ) {

        ctx.strokeStyle =
            "#63dcff";


        ctx.lineWidth =
            5;


        ctx.beginPath();


        ctx.arc(
            0,
            -height / 2,
            65,
            0,
            Math.PI * 2
        );


        ctx.stroke();
    }


    ctx.restore();
}


// =====================================================
// 친구
// =====================================================

function drawFriend() {

    /*
     * character2도 달리기 2프레임 사용
     */

    const image =
        animationFrame === 0
            ? character2
            : character2Run2;


    const x =
        player.x -
        105;


    const y =
        player.y +
        5;


    ctx.save();


    ctx.translate(
        x,
        y
    );


    /*
     * 친구가 점프할 때 회전
     */

    if (
        player.jumping
    ) {

        player.rotation +=
            0.28;


        ctx.rotate(
            player.rotation
        );
    }


    if (
        imageReady(
            image
        )
    ) {

        ctx.drawImage(
            image,

            -38,
            -48,

            76,
            96
        );
    }


    ctx.restore();
}


// =====================================================
// 파티클 생성
// =====================================================

function burst(
    x,
    y,
    color,
    amount
) {

    for (
        let i = 0;

        i < amount;

        i++
    ) {

        particles.push({

            x:
                x,

            y:
                y,

            vx:
                (
                    Math.random()
                    - 0.5
                ) * 9,

            vy:
                (
                    Math.random()
                    - 0.5
                ) * 9,

            life:
                35,

            color:
                color
        });
    }
}


// =====================================================
// 파티클 업데이트
// =====================================================

function updateParticles() {

    particles.forEach(
        function(p) {

            p.x +=
                p.vx;

            p.y +=
                p.vy;

            p.vy +=
                0.25;

            p.life--;
        }
    );


    particles =
        particles.filter(
            function(p) {

                return (
                    p.life > 0
                );
            }
        );
}


// =====================================================
// 파티클 그리기
// =====================================================

function drawParticles() {

    particles.forEach(
        function(p) {

            ctx.globalAlpha =
                p.life / 35;


            ctx.fillStyle =
                p.color;


            ctx.beginPath();


            ctx.arc(
                p.x,
                p.y,
                5,
                0,
                Math.PI * 2
            );


            ctx.fill();
        }
    );


    ctx.globalAlpha =
        1;
}


// =====================================================
// DRAW
// =====================================================

function draw() {

    // 배경 + 도로

    drawBackground();


    /*
     * 원근에 따라 오브젝트를
     * 뒤에서 앞으로 정렬해서 그린다.
     *
     * 멀리 있는 것 → 먼저
     * 가까운 것 → 나중
     */

    const sortedObjects =
        [...objects].sort(
            function(a, b) {

                return (
                    a.progress -
                    b.progress
                );
            }
        );


    sortedObjects.forEach(
        function(obj) {

            if (
                obj.type ===
                "jumpObstacle"
            ) {

                drawObstacle(
                    obj
                );

            }
            else if (
                obj.type ===
                "slideObstacle"
            ) {

                drawObstacle(
                    obj
                );

            }
            else if (
                obj.type ===
                "box"
            ) {

                drawBox(
                    obj
                );

            }
            else {

                drawItem(
                    obj
                );
            }
        }
    );


    // 친구

    drawFriend();


    // 플레이어

    drawPlayer();


    // 파티클

    drawParticles();
}


// =====================================================
// LOOP
// =====================================================

function loop() {

    update();


    draw();


    document
        .getElementById(
            "score"
        )
        .textContent =
            Math.floor(
                score
            );


    document
        .getElementById(
            "best"
        )
        .textContent =
            Math.max(
                best,
                Math.floor(
                    score
                )
            );


    requestAnimationFrame(
        loop
    );
}


// =====================================================
// 시작
// =====================================================

loop();


</script>

</body>

</html>
"""


# =========================================================
# 이미지 삽입
# =========================================================

game = game.replace(
    "__CHARACTER1__",
    CHARACTER1
)


game = game.replace(
    "__CHARACTER1_RUN2__",
    CHARACTER1_RUN2
)


game = game.replace(
    "__CHARACTER2__",
    CHARACTER2
)


game = game.replace(
    "__CHARACTER2_RUN2__",
    CHARACTER2_RUN2
)


game = game.replace(
    "__CHARACTER3__",
    CHARACTER3
)


game = game.replace(
    "__CHARACTER3_RUN2__",
    CHARACTER3_RUN2
)


game = game.replace(
    "__BACKGROUND__",
    BACKGROUND
)


# =========================================================
# 실행
# =========================================================

components.html(
    game,
    height=700,
    scrolling=False
)
