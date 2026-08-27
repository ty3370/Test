import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64


# =========================================================
# STREAMLIT
# =========================================================

st.set_page_config(
    page_title="Chiikawa Run!",
    page_icon="🌸",
    layout="centered"
)


# =========================================================
# PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"


# =========================================================
# IMAGE → BASE64
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
# CHARACTERS
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
# FILE CHECK
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


# =========================================================
# STREAMLIT CSS
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
# GAME HTML
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
   RESET
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

    justify-content:
        center;

    align-items:
        flex-start;
}


/* =====================================================
   GAME
   ===================================================== */

#gameWrap {

    width: 100%;

    display: flex;

    justify-content: center;
}


#game {

    position: relative;

    width: 920px;
    height: 650px;

    flex-shrink: 0;

    outline: none;
}


canvas {

    width: 100%;
    height: 100%;

    display: block;

    border-radius: 20px;

    background: #ffffff;

    box-shadow:
        0 5px 18px
        rgba(80,60,70,.16);

    outline: none;

    user-select: none;
    -webkit-user-select: none;
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
        rgba(255,255,255,.94);

    color: #604850;

    font-weight: 900;

    font-size: 13px;

    padding: 6px 10px;

    border-radius: 13px;

    box-shadow:
        0 3px 8px
        rgba(0,0,0,.12);

    white-space: nowrap;
}


/* =====================================================
   MENU
   ===================================================== */

#menu {

    position: absolute;

    inset: 0;

    z-index: 20;

    display: flex;

    justify-content: center;

    align-items: center;

    padding: 12px;

    border-radius: 20px;
}


.menuCard {

    width: min(390px,82%);

    max-height: 86%;

    background:
        rgba(255,255,255,.97);

    border-radius: 22px;

    padding: 18px 14px;

    text-align: center;

    box-shadow:
        0 10px 25px
        rgba(60,40,60,.22);
}


.title {

    color: #5d3f47;

    font-weight: 900;

    font-size:
        clamp(21px,5vw,32px);

    margin-bottom: 8px;
}


.description {

    color: #76666d;

    font-size:
        clamp(11px,2.8vw,15px);

    line-height: 1.34;

    margin-bottom: 11px;
}


.startButton {

    appearance: none;

    -webkit-appearance: none;

    border: none;

    width: 100%;

    padding: 13px 18px;

    border-radius: 15px;

    background:
        linear-gradient(
            135deg,
            #ff9abb,
            #ff6497
        );

    color: white;

    font-size: 16px;

    font-weight: 900;

    box-shadow:
        0 5px 0
        #d74d79;

    cursor: pointer;

    touch-action: manipulation;
}


.startButton:active {

    transform:
        translateY(4px);

    box-shadow: none;
}


/* =====================================================
   CONTROLS
   ===================================================== */

.controls {

    position: absolute;

    left: 50%;
    bottom: 8px;

    transform:
        translateX(-50%);

    display: flex;

    gap: 6px;

    z-index: 15;
}


.ctrl {

    appearance: none;

    -webkit-appearance: none;

    width: 43px;
    height: 39px;

    padding: 0;

    border: 0;

    border-radius: 13px;

    background:
        rgba(255,255,255,.94);

    color: #5d4b50;

    font-size: 18px;

    font-weight: 900;

    box-shadow:
        0 3px 8px
        rgba(0,0,0,.13);

    touch-action: manipulation;
}


.ctrl:active {

    transform:
        scale(.93);
}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width:600px) {

    #game,
    canvas {
        border-radius: 14px;
    }

    .menuCard {

        width: 80%;

        padding:
            11px 10px;

        border-radius: 18px;
    }

    .title {

        font-size: 20px;

        margin-bottom: 5px;
    }

    .description {

        font-size: 10px;

        line-height: 1.25;

        margin-bottom: 7px;
    }

    .startButton {

        padding:
            9px 10px;

        font-size: 13px;
    }

    .hud {

        top: 5px;
        left: 5px;
        right: 5px;
    }

    .hudBox {

        font-size: 9px;

        padding:
            4px 6px;
    }

    .controls {

        bottom: 5px;

        gap: 5px;
    }

    .ctrl {

        width: 38px;
        height: 34px;

        font-size: 15px;
    }
}


/* =====================================================
   SHORT SCREEN
   ===================================================== */

@media (max-height:600px) {

    .menuCard {

        width: 66%;

        padding:
            8px 10px;
    }

    .title {
        font-size: 18px;
    }

    .description {

        font-size: 9px;

        line-height: 1.2;

        margin-bottom: 5px;
    }

    .startButton {

        padding:
            7px 10px;

        font-size: 12px;
    }

    .controls {
        bottom: 3px;
    }

    .ctrl {

        width: 34px;
        height: 30px;

        font-size: 13px;
    }
}

</style>

</head>


<body>

<div id="gameWrap">

<div
    id="game"
    tabindex="0"
>

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
     MENU
     =================================================== -->

<div id="menu">

    <div class="menuCard">

        <div class="title">

            🌸 CHIIKAWA RUN! 🌸

        </div>

        <div class="description">

            치이카와 친구들과 함께 달려보세요!

            <br>

            PC:
            ← → 이동 · ↑ 점프 · ↓ 숙이기

            <br>

            모바일:
            아래 버튼 사용

            <br>

            낮은 장애물은 점프!
            높은 장애물은 숙이기!

            <br>

            랜덤박스를 먹으면 아이템을 획득합니다!

            <br>

            ✨ 점수가 올라가면 변신합니다!

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
     MOBILE CONTROLS
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
// IMAGES
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
// CANVAS
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
// DOM
// =====================================================

const game =
    document.getElementById(
        "game"
    );


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
// GAME STATE
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


// =====================================================
// SPEED
// =====================================================

const BASE_SPEED =
    7;


const MAX_SPEED =
    16;


let speed =
    BASE_SPEED;


// =====================================================
// TIME
// =====================================================

let lastTime =
    0;


let elapsedTime =
    0;


const MAX_DELTA =
    0.035;


// =====================================================
// GAME OBJECTS
// =====================================================

let distance =
    0;


let spawnTimer =
    0.75;


let objects =
    [];


let particles =
    [];


// =====================================================
// RUN ANIMATION
// =====================================================

let animationFrame =
    0;


let animationTimer =
    0;


// =====================================================
// ROAD ANIMATION
// =====================================================

let roadOffset =
    0;


let sceneryOffset =
    0;


// =====================================================
// TRANSFORMATION
// =====================================================

let transformationEffect =
    0;


let transformationParticles =
    [];


// =====================================================
// PERSPECTIVE
// =====================================================

const HORIZON_Y =
    145;


const HORIZON_LANES = [

    450,
    460,
    470

];


const BOTTOM_LANES = [

    300,
    460,
    620

];


// =====================================================
// PLAYER
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

    /*
     * 착지 직후 아주 짧은 판정 여유.
     * 장애물이 발밑을 통과하는 순간 점프가
     * 끊겨 보이는 문제를 방지한다.
     */
    jumpClearTimer:
        0,

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
        0
};


// =====================================================
// FRIEND
// =====================================================

let friend = {

    rotation:
        0,

    jumping:
        false,

    jumpStart:
        0,

    jumpDuration:
        0.72
};


// =====================================================
// SCREEN FIT
// =====================================================

function fitGameToScreen() {

    const screenWidth =
        window.innerWidth;


    const screenHeight =
        window.innerHeight;


    const widthFromHeight =
        screenHeight *
        WIDTH /
        HEIGHT;


    const finalWidth =
        Math.min(
            WIDTH,
            screenWidth,
            widthFromHeight
        );


    game.style.width =
        Math.max(
            280,
            finalWidth
        ) + "px";


    game.style.height =
        (
            finalWidth *
            HEIGHT /
            WIDTH
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
// FOCUS
// =====================================================

function focusGame() {

    try {

        game.focus({
            preventScroll:
                true
        });

    }

    catch (e) {

        game.focus();

    }
}


canvas.addEventListener(
    "pointerdown",
    focusGame
);


game.addEventListener(
    "pointerdown",
    focusGame
);


// =====================================================
// START
// =====================================================

function startGame() {

    running =
        true;


    score =
        0;


    distance =
        0;


    speed =
        BASE_SPEED;


    spawnTimer =
        0.75;


    objects =
        [];


    particles =
        [];


    transformationParticles =
        [];


    transformationEffect =
        0;


    animationFrame =
        0;


    animationTimer =
        0;


    roadOffset =
        0;


    sceneryOffset =
        0;


    elapsedTime =
        0;


    lastTime =
        performance.now();


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

        jumpClearTimer:
            0,

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
            0
    };


    friend = {

        rotation:
            0,

        jumping:
            false,

        jumpStart:
            0,

        jumpDuration:
            0.72
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
        .style
        .display =
            "none";


    focusGame();
}


// =====================================================
// POINTER ACTION
// =====================================================

function addPointerAction(
    element,
    action
) {

    element.addEventListener(
        "pointerdown",
        function(event) {

            event.preventDefault();

            event.stopPropagation();

            action();

            focusGame();

        }
    );
}


addPointerAction(
    startButton,
    startGame
);


addPointerAction(
    leftButton,
    moveLeft
);


addPointerAction(
    rightButton,
    moveRight
);


addPointerAction(
    jumpButton,
    jump
);


addPointerAction(
    slideButton,
    slide
);


// =====================================================
// KEYBOARD
// =====================================================

/*
 * 핵심 수정:
 *
 * event.repeat을 무시한다.
 *
 * 따라서
 *
 * ←를 계속 누르고 있어도
 * 한 번만 한 칸 이동한다.
 *
 * 키를 떼고 다시 누르면
 * 다시 한 칸 이동한다.
 */

function handleKey(event) {

    if (!running)
        return;


    /*
     * 브라우저의 key repeat 차단
     */

    if (
        event.repeat
    ) {

        event.preventDefault();

        return;
    }


    const key =
        event.key;


    const code =
        event.code;


    if (
        key ===
        "ArrowLeft"
    ) {

        moveLeft();

        event.preventDefault();

        return;
    }


    if (
        key ===
        "ArrowRight"
    ) {

        moveRight();

        event.preventDefault();

        return;
    }


    if (
        key ===
        "ArrowUp"
    ) {

        jump();

        event.preventDefault();

        return;
    }


    if (
        key ===
        "ArrowDown"
    ) {

        slide();

        event.preventDefault();

        return;
    }


    if (
        code ===
        "Space"
    ) {

        jump();

        event.preventDefault();

        return;
    }
}


/*
 * document 한 곳에서만 처리한다.
 *
 * 이전 코드처럼 window와 document 양쪽에
 * 같은 함수를 등록하면 한 번의 키 입력이
 * 중복 처리될 가능성이 있기 때문이다.
 */

document.addEventListener(
    "keydown",
    handleKey,
    {
        passive:
            false
    }
);


// =====================================================
// MOVE LEFT
// =====================================================

function moveLeft() {

    if (!running)
        return;


    if (
        player.lane <= 0
    ) {

        return;
    }


    /*
     * 정확히 한 레인만 이동
     */

    player.lane -=
        1;


    player.targetX =
        BOTTOM_LANES[
            player.lane
        ];
}


// =====================================================
// MOVE RIGHT
// =====================================================

function moveRight() {

    if (!running)
        return;


    if (
        player.lane >= 2
    ) {

        return;
    }


    /*
     * 정확히 한 레인만 이동
     */

    player.lane +=
        1;


    player.targetX =
        BOTTOM_LANES[
            player.lane
        ];
}


// =====================================================
// JUMP
// =====================================================

function jump() {

    if (!running)
        return;


    if (
        player.jumping
    ) {

        return;
    }


    player.jumping =
        true;

    /*
     * 바닥 장애물을 확실하게 뛰어넘을 수 있도록
     * 점프 시작 직후부터 짧은 "점프 판정"을 유지한다.
     */
    player.jumpClearTimer =
        0.72;


    player.vy =
        -18;


    /*
     * 친구도 동시에 점프
     */

    friend.jumping =
        true;


    friend.jumpStart =
        elapsedTime;


    friend.rotation =
        0;
}


// =====================================================
// SLIDE
// =====================================================

function slide() {

    if (!running)
        return;


    if (
        player.jumping
    ) {

        return;
    }


    player.sliding =
        true;


    player.slideTimer =
        0.65;
}


// =====================================================
// FRIEND UPDATE
// =====================================================

function updateFriend() {

    if (
        !friend.jumping
    ) {

        friend.rotation =
            0;

        return;
    }


    const t =
        (
            elapsedTime -
            friend.jumpStart
        )
        /
        friend.jumpDuration;


    if (
        t >= 1
    ) {

        friend.jumping =
            false;


        friend.rotation =
            0;


        return;
    }


    /*
     * 0 → 1 구간에서
     * 정확히 한 바퀴 회전
     *
     * 0
     * ↓
     * 90°
     * ↓
     * 180°
     * ↓
     * 270°
     * ↓
     * 360°
     */

    friend.rotation =
        t *
        Math.PI *
        2;
}


// =====================================================
// PERSPECTIVE POINT
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
// SPAWN
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


    if (
        r < 0.27
    ) {

        type =
            "jumpObstacle";
    }


    else if (
        r < 0.43
    ) {

        type =
            "slideObstacle";
    }


    else if (
        r < 0.68
    ) {

        type =
            "box";
    }


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
            0.01,

        type:
            type,

        item:
            item
    });
}


// =====================================================
// ITEM
// =====================================================

function getItem(
    item
) {

    if (
        item ===
        "giant"
    ) {

        player.giant =
            true;

        player.giantTimer =
            7;
    }


    else if (
        item ===
        "score"
    ) {

        score +=
            500;
    }


    else if (
        item ===
        "shield"
    ) {

        player.shield =
            true;

        player.shieldTimer =
            6;
    }


    else if (
        item ===
        "slow"
    ) {

        speed =
            Math.max(
                4.5,
                speed - 2
            );
    }


    else if (
        item ===
        "speed"
    ) {

        score +=
            250;

        speed =
            Math.min(
                MAX_SPEED,
                speed + 1
            );
    }


    else if (
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
                MAX_SPEED,
                speed + 2
            );
    }
}


// =====================================================
// BOX
// =====================================================

function openBox(
    obj
) {

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
// COLLISION
// =====================================================

function objectIsAtPlayer(
    obj
) {

    return (

        obj.progress >=
        0.82

        &&

        obj.progress <=
        1.05

        &&

        player.lane ===
        obj.lane
    );
}


// =====================================================
// TRANSFORMATION
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


        transformationEffect =
            1.15;


        transformationParticles =
            [];


        for (
            let i = 0;
            i < 50;
            i++
        ) {

            transformationParticles.push({

                angle:
                    Math.random() *
                    Math.PI *
                    2,

                distance:
                    10 +
                    Math.random() *
                    35,

                speed:
                    30 +
                    Math.random() *
                    80,

                size:
                    3 +
                    Math.random() *
                    6,

                life:
                    1.2
            });
        }


        burst(
            player.x,
            player.y - 65,
            "#fff3a3",
            35
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
// TRANSFORMATION UPDATE
// =====================================================

function updateTransformation(
    dt
) {

    if (
        transformationEffect <=
        0
    ) {

        return;
    }


    transformationEffect -=
        dt;


    transformationParticles.forEach(
        function(p) {

            p.distance +=
                p.speed *
                dt;

            p.life -=
                dt;
        }
    );


    transformationParticles =
        transformationParticles.filter(
            function(p) {

                return (
                    p.life > 0
                );
            }
        );
}


// =====================================================
// UPDATE
// =====================================================

function update(
    dt
) {

    if (!running)
        return;


    elapsedTime +=
        dt;


    distance +=
        speed *
        dt *
        60;


    score +=
        0.28 *
        dt *
        60;


    const targetSpeed =
        Math.min(
            MAX_SPEED,
            BASE_SPEED +
            distance / 390000
        );


    if (
        speed <
        targetSpeed
    ) {

        speed +=
            (
                targetSpeed -
                speed
            )
            *
            Math.min(
                1,
                dt * 1.5
            );
    }


    // -----------------------------------------------
    // TRANSFORMATION
    // -----------------------------------------------

    transformationCheck();


    updateTransformation(
        dt
    );


    // -----------------------------------------------
    // PLAYER LANE
    // -----------------------------------------------

    const laneEase =
        1 -
        Math.pow(
            0.001,
            dt
        );


    player.x +=
        (
            player.targetX -
            player.x
        )
        *
        laneEase;


    // -----------------------------------------------
    // PLAYER JUMP
    // -----------------------------------------------

    if (
        player.jumpClearTimer > 0
    ) {

        player.jumpClearTimer -=
            dt;


        if (
            player.jumpClearTimer < 0
        ) {

            player.jumpClearTimer =
                0;
        }
    }


    if (
        player.jumping
    ) {

        player.vy +=
            55 *
            dt;


        player.y +=
            player.vy *
            dt *
            60;


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
    // FRIEND ROTATION
    // -----------------------------------------------

    updateFriend();


    // -----------------------------------------------
    // SLIDE
    // -----------------------------------------------

    if (
        player.sliding
    ) {

        player.slideTimer -=
            dt;


        if (
            player.slideTimer <=
            0
        ) {

            player.slideTimer =
                0;


            player.sliding =
                false;
        }
    }


    // -----------------------------------------------
    // GIANT
    // -----------------------------------------------

    if (
        player.giant
    ) {

        player.giantTimer -=
            dt;


        if (
            player.giantTimer <=
            0
        ) {

            player.giant =
                false;
        }
    }


    // -----------------------------------------------
    // SHIELD
    // -----------------------------------------------

    if (
        player.shield
    ) {

        player.shieldTimer -=
            dt;


        if (
            player.shieldTimer <=
            0
        ) {

            player.shield =
                false;
        }
    }


    // -----------------------------------------------
    // RUN ANIMATION
    // -----------------------------------------------

    animationTimer +=
        dt;


    if (
        animationTimer >=
        0.13
    ) {

        animationTimer =
            0;


        animationFrame =
            animationFrame === 0
                ? 1
                : 0;
    }


    // -----------------------------------------------
    // ROAD
    // -----------------------------------------------

    roadOffset +=
        speed *
        dt *
        60;


    roadOffset %=
        100;


    sceneryOffset +=
        speed *
        1.25 *
        dt *
        60;


    sceneryOffset %=
        120;


    // -----------------------------------------------
    // SPAWN
    // -----------------------------------------------

    spawnTimer -=
        dt;


    if (
        spawnTimer <=
        0
    ) {

        spawnObject();


        const interval =
            Math.max(
                0.48,
                1.15 -
                speed * 0.035
            );


        spawnTimer =
            interval;
    }


    // -----------------------------------------------
    // OBJECT MOVEMENT
    // -----------------------------------------------

    objects.forEach(
        function(obj) {

            const distanceFactor =
                0.65 +
                obj.progress *
                1.45;


            obj.progress +=
                speed *
                dt *
                0.099 *
                distanceFactor;
        }
    );


    // -----------------------------------------------
    // COLLISION
    // -----------------------------------------------

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


        // -------------------------------------------
        // BOX
        // -------------------------------------------

                /*
         * 점프 중에는 지상에 있는 box와 item을 피한다.
         * jumpObstacle은 아래 기존 충돌 로직에서 점프로 처리하고,
         * slideObstacle은 기존대로 숙여서 피한다.
         */
        if (
            player.jumping
            &&
            (
                obj.type ===
                "box"
                ||
                obj.type ===
                "item"
            )
        ) {
            continue;
        }

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


        // -------------------------------------------
        // ITEM
        // -------------------------------------------

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
                14
            );


            objects.splice(
                i,
                1
            );


            continue;
        }


        // -------------------------------------------
        // JUMP OBSTACLE
        // -------------------------------------------

        if (
            obj.type ===
            "jumpObstacle"
        ) {

            /*
             * 바닥형 장애물은 점프로 통과한다.
             * 착지 직후의 짧은 판정 여유도 포함해
             * 장애물과 점프 타이밍이 한 프레임 어긋나도
             * 충돌하지 않도록 한다.
             *
             * 숙여야 하는 slideObstacle에는 이 조건을
             * 적용하지 않는다.
             */
            if (
                player.jumping
                ||
                player.jumpClearTimer > 0
            ) {

                objects.splice(
                    i,
                    1
                );


                score +=
                    100;


                continue;
            }


            if (
                player.giant
            ) {

                score +=
                    200;


                const point =
                    perspectivePoint(
                        obj.lane,
                        obj.progress
                    );


                burst(
                    point.x,
                    point.y,
                    "#ff82a8",
                    20
                );


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


        // -------------------------------------------
        // SLIDE OBSTACLE
        // -------------------------------------------

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


                score +=
                    100;


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
    }


    // -----------------------------------------------
    // REMOVE OBJECTS
    // -----------------------------------------------

    objects =
        objects.filter(
            function(obj) {

                return (
                    obj.progress <
                    1.12
                );
            }
        );


    // -----------------------------------------------
    // PARTICLES
    // -----------------------------------------------

    updateParticles(
        dt
    );
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


    const menu =
        document.getElementById(
            "menu"
        );


    menu.innerHTML = `

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


    menu.style.display =
        "flex";


    const restartButton =
        document.getElementById(
            "restartButton"
        );


    restartButton.addEventListener(
        "pointerdown",
        function(event) {

            event.preventDefault();

            startGame();
        }
    );
}


// =====================================================
// IMAGE READY
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

    if (
        imageReady(
            background
        )
    ) {

        ctx.drawImage(
            background,
            0,
            0,
            WIDTH,
            HEIGHT
        );

    }

    else {

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
            "#e8f4e0"
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



    drawRoad();

    drawSideScenery();
}



// =====================================================
// ROAD
// =====================================================

function drawRoad() {

    const roadTopY =
        HORIZON_Y;


    const roadTopLeft =
        410;


    const roadTopRight =
        510;


    const roadBottomLeft =
        -100;


    const roadBottomRight =
        1020;


    ctx.fillStyle =
        "rgba(100,100,100,.10)";


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


    /*
     * 흰색 도로
     */

    const roadGradient =
        ctx.createLinearGradient(
            0,
            roadTopY,
            0,
            HEIGHT
        );


    roadGradient.addColorStop(
        0,
        "#ffffff"
    );


    roadGradient.addColorStop(
        0.5,
        "#fafafa"
    );


    roadGradient.addColorStop(
        1,
        "#eeeeee"
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


    /*
     * 도로 가장자리
     */

    ctx.strokeStyle =
        "#b8b8b8";


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


    drawPerspectiveLane(
        0
    );


    drawPerspectiveLane(
        1
    );


    drawRoadTexture();
}


// =====================================================
// LANE
// =====================================================

function drawPerspectiveLane(
    laneLine
) {

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
        "#b4b4b4";


    ctx.lineCap =
        "round";


    for (
        let i = -1;
        i < 14;
        i++
    ) {

        let progress =
            (
                i * 0.085
                +
                roadOffset / 100 *
                0.085
            );


        progress =
            progress % 1;


        if (
            progress < 0
        ) {

            progress +=
                1;
        }


        const p1 =
            progress;


        const p2 =
            Math.min(
                1,
                progress + 0.045
            );


        const x1 =
            perspectiveRoadX(
                topX,
                bottomX,
                p1
            );


        const x2 =
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
            x1,
            y1
        );


        ctx.lineTo(
            x2,
            y2
        );


        ctx.stroke();
    }


    ctx.restore();
}


// =====================================================
// ROAD X
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
// ROAD Y
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
// ROAD TEXTURE
// =====================================================

function drawRoadTexture() {

    ctx.save();


    ctx.globalAlpha =
        0.18;


    ctx.strokeStyle =
        "#c0c0c0";


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
                roadOffset / 100 *
                0.075
            ) % 1;


        const y =
            perspectiveRoadY(
                progress
            );


        const leftX =
            perspectiveRoadX(
                410,
                -80,
                progress
            );


        const rightX =
            perspectiveRoadX(
                510,
                1000,
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
// SIDE SCENERY
// =====================================================

function drawSideScenery() {

    /*
     * 도로 양옆의 풍경을 "나무"처럼 보이게 만든다.
     * progress가 커질수록 가까워지고 커지며,
     * 양옆으로 살짝 벌어져 실제 도로를 달려가는 느낌을 준다.
     */

    for (
        let i = -1;
        i < 13;
        i++
    ) {

        let progress =
            (
                i * 0.095
                +
                sceneryOffset / 120 * 0.095
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


        /*
         * 가까워질수록 나무가 커지고
         * 도로에서 조금 더 바깥쪽으로 이동한다.
         */

        const scale =
            0.18 +
            progress * 1.75;


        const sideDistance =
            32 +
            progress * 82;


        const leftX =
            leftRoad -
            sideDistance;


        const rightX =
            rightRoad +
            sideDistance;


        /*
         * 좌우 나무의 높이를 일부러 다르게 해서
         * 반복되는 느낌을 줄인다.
         */

        drawTree(
            leftX,
            y + 4,
            scale,
            i % 3
        );


        drawTree(
            rightX,
            y + 12,
            scale * 0.92,
            (i + 1) % 3
        );
    }
}


// =====================================================
// TREE
// =====================================================

function drawTree(
    x,
    y,
    scale,
    variant
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


    /*
     * 나무 그림자
     */

    ctx.fillStyle =
        "rgba(70,70,70,.16)";


    ctx.beginPath();


    ctx.ellipse(
        0,
        5,
        31,
        9,
        0,
        0,
        Math.PI * 2
    );


    ctx.fill();


    /*
     * 줄기
     */

    const trunkWidth =
        variant === 2
            ? 13
            : 11;


    const trunkHeight =
        variant === 1
            ? 72
            : 66;


    ctx.fillStyle =
        "#9b6b50";


    ctx.strokeStyle =
        "#705043";


    ctx.lineWidth =
        3;


    ctx.beginPath();


    ctx.roundRect(
        -trunkWidth / 2,
        -trunkHeight,
        trunkWidth,
        trunkHeight,
        5
    );


    ctx.fill();


    ctx.stroke();


    /*
     * 가지
     */

    ctx.lineWidth =
        7;


    ctx.lineCap =
        "round";


    ctx.beginPath();


    ctx.moveTo(
        0,
        -trunkHeight + 22
    );


    ctx.lineTo(
        -20,
        -trunkHeight - 2
    );


    ctx.moveTo(
        1,
        -trunkHeight + 30
    );


    ctx.lineTo(
        21,
        -trunkHeight + 5
    );


    ctx.stroke();


    /*
     * 나뭇잎 덩어리.
     * 원 여러 개를 겹쳐서 만화풍의 둥근 나무를 만든다.
     */

    const leafMain =
        variant === 0
            ? "#8fcf91"
            : variant === 1
                ? "#a2d79a"
                : "#86c987";


    const leafLight =
        variant === 1
            ? "#c1e7b2"
            : "#b4dfaa";


    ctx.fillStyle =
        leafMain;


    ctx.strokeStyle =
        "#6ea873";


    ctx.lineWidth =
        3;


    ctx.beginPath();


    ctx.arc(
        -24,
        -trunkHeight + 10,
        25,
        0,
        Math.PI * 2
    );


    ctx.arc(
        0,
        -trunkHeight - 7,
        31,
        0,
        Math.PI * 2
    );


    ctx.arc(
        25,
        -trunkHeight + 11,
        25,
        0,
        Math.PI * 2
    );


    ctx.arc(
        0,
        -trunkHeight + 16,
        30,
        0,
        Math.PI * 2
    );


    ctx.fill();


    ctx.stroke();


    /*
     * 잎사귀 하이라이트
     */

    ctx.fillStyle =
        leafLight;


    ctx.beginPath();


    ctx.arc(
        -13,
        -trunkHeight - 10,
        9,
        0,
        Math.PI * 2
    );


    ctx.arc(
        12,
        -trunkHeight + 1,
        8,
        0,
        Math.PI * 2
    );


    ctx.arc(
        -28,
        -trunkHeight + 20,
        6,
        0,
        Math.PI * 2
    );


    ctx.fill();


    /*
     * 작은 벚꽃 포인트.
     * 배경의 벚꽃 분위기와도 자연스럽게 연결된다.
     */

    ctx.fillStyle =
        "#ffd5e3";


    const flowerPositions = [
        [-18, -trunkHeight - 15],
        [18, -trunkHeight - 2],
        [0, -trunkHeight + 18]
    ];


    flowerPositions.forEach(
        function(pos) {

            const fx =
                pos[0];

            const fy =
                pos[1];


            for (
                let k = 0;
                k < 5;
                k++
            ) {

                const angle =
                    k *
                    Math.PI *
                    2 /
                    5;


                ctx.beginPath();


                ctx.arc(
                    fx +
                    Math.cos(angle) * 4,
                    fy +
                    Math.sin(angle) * 4,
                    3.2,
                    0,
                    Math.PI * 2
                );


                ctx.fill();
            }


            ctx.fillStyle =
                "#fff4a8";


            ctx.beginPath();


            ctx.arc(
                fx,
                fy,
                2.2,
                0,
                Math.PI * 2
            );


            ctx.fill();


            ctx.fillStyle =
                "#ffd5e3";
        }
    );


    ctx.restore();
}


// =====================================================
// JUMP OBSTACLE
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


    ctx.fillStyle =
        "rgba(70,70,70,.20)";


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


    ctx.fillStyle =
        "#ffffff";


    ctx.font =
        `bold ${Math.max(
            9,
            20 * scale
        )}px Arial`;


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
// SLIDE OBSTACLE
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


    ctx.fillStyle =
        "rgba(70,70,70,.20)";


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


    ctx.fillStyle =
        "#ffffff";


    ctx.font =
        `bold ${Math.max(
            8,
            18 * scale
        )}px Arial`;


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
// BOX
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
        obj.progress *
        1.45;


    const size =
        42 * scale;


    ctx.fillStyle =
        "rgba(70,70,70,.18)";


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
        "#ffffff";


    ctx.font =
        `bold ${Math.max(
            9,
            25 * scale
        )}px Arial`;


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
// ITEM ICON
// =====================================================

function drawItemIcon(
    type,
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


    ctx.lineJoin =
        "round";


    ctx.lineCap =
        "round";


    ctx.shadowColor =
        "rgba(0,0,0,.20)";


    ctx.shadowBlur =
        5;


    if (
        type ===
        "giant"
    ) {

        ctx.fillStyle =
            "#fff1d0";


        ctx.strokeStyle =
            "#784d3e";


        ctx.lineWidth =
            3;


        ctx.beginPath();


        ctx.roundRect(
            -13,
            0,
            26,
            28,
            6
        );


        ctx.fill();


        ctx.stroke();


        ctx.fillStyle =
            "#ff759d";


        ctx.beginPath();


        ctx.arc(
            0,
            0,
            27,
            Math.PI,
            0
        );


        ctx.lineTo(
            27,
            5
        );


        ctx.quadraticCurveTo(
            0,
            18,
            -27,
            5
        );


        ctx.closePath();


        ctx.fill();


        ctx.stroke();


        ctx.shadowBlur =
            0;


        ctx.fillStyle =
            "#ffffff";


        ctx.beginPath();


        ctx.arc(
            -10,
            -3,
            5,
            0,
            Math.PI * 2
        );


        ctx.arc(
            7,
            -7,
            4,
            0,
            Math.PI * 2
        );


        ctx.arc(
            13,
            4,
            3,
            0,
            Math.PI * 2
        );


        ctx.fill();
    }


    else if (
        type ===
        "score"
    ) {

        ctx.fillStyle =
            "#65d9ff";


        ctx.strokeStyle =
            "#277fbd";


        ctx.lineWidth =
            3;


        ctx.beginPath();


        ctx.moveTo(
            0,
            -30
        );


        ctx.lineTo(
            24,
            -8
        );


        ctx.lineTo(
            13,
            25
        );


        ctx.lineTo(
            -13,
            25
        );


        ctx.lineTo(
            -24,
            -8
        );


        ctx.closePath();


        ctx.fill();


        ctx.stroke();


        ctx.shadowBlur =
            0;


        ctx.fillStyle =
            "rgba(255,255,255,.78)";


        ctx.beginPath();


        ctx.moveTo(
            -10,
            -16
        );


        ctx.lineTo(
            -2,
            -23
        );


        ctx.lineTo(
            4,
            -8
        );


        ctx.lineTo(
            -5,
            -2
        );


        ctx.closePath();


        ctx.fill();
    }


    else if (
        type ===
        "shield"
    ) {

        ctx.fillStyle =
            "#65dfff";


        ctx.strokeStyle =
            "#267dba";


        ctx.lineWidth =
            3;


        ctx.beginPath();


        ctx.moveTo(
            0,
            -30
        );


        ctx.lineTo(
            25,
            -20
        );


        ctx.lineTo(
            21,
            10
        );


        ctx.quadraticCurveTo(
            13,
            27,
            0,
            34
        );


        ctx.quadraticCurveTo(
            -13,
            27,
            -21,
            10
        );


        ctx.lineTo(
            -25,
            -20
        );


        ctx.closePath();


        ctx.fill();


        ctx.stroke();


        ctx.shadowBlur =
            0;


        ctx.strokeStyle =
            "#ffffff";


        ctx.lineWidth =
            4;


        ctx.beginPath();


        ctx.moveTo(
            0,
            -20
        );


        ctx.lineTo(
            12,
            -14
        );


        ctx.lineTo(
            10,
            7
        );


        ctx.quadraticCurveTo(
            6,
            17,
            0,
            21
        );


        ctx.quadraticCurveTo(
            -6,
            17,
            -10,
            7
        );


        ctx.lineTo(
            -12,
            -14
        );


        ctx.closePath();


        ctx.stroke();
    }


    else if (
        type ===
        "speed"
    ) {

        ctx.fillStyle =
            "#ffd43b";


        ctx.strokeStyle =
            "#9b7114";


        ctx.lineWidth =
            3;


        ctx.beginPath();


        ctx.moveTo(
            7,
            -33
        );


        ctx.lineTo(
            -19,
            3
        );


        ctx.lineTo(
            -4,
            3
        );


        ctx.lineTo(
            -12,
            32
        );


        ctx.lineTo(
            22,
            -8
        );


        ctx.lineTo(
            6,
            -8
        );


        ctx.closePath();


        ctx.fill();


        ctx.stroke();
    }


    else if (
        type ===
        "slow"
    ) {

        ctx.fillStyle =
            "#9bd47f";


        ctx.strokeStyle =
            "#4c8050";


        ctx.lineWidth =
            3;


        ctx.beginPath();


        ctx.ellipse(
            0,
            10,
            30,
            14,
            0,
            0,
            Math.PI * 2
        );


        ctx.fill();


        ctx.stroke();


        ctx.fillStyle =
            "#ffb276";


        ctx.beginPath();


        ctx.arc(
            -7,
            -4,
            20,
            0,
            Math.PI * 2
        );


        ctx.fill();


        ctx.stroke();


        ctx.shadowBlur =
            0;


        ctx.strokeStyle =
            "#d8784b";


        ctx.lineWidth =
            3;


        ctx.beginPath();


        ctx.arc(
            -7,
            -4,
            9,
            0,
            Math.PI * 1.7
        );


        ctx.stroke();


        ctx.fillStyle =
            "#333333";


        ctx.beginPath();


        ctx.arc(
            21,
            -3,
            2.5,
            0,
            Math.PI * 2
        );


        ctx.arc(
            28,
            -3,
            2.5,
            0,
            Math.PI * 2
        );


        ctx.fill();


        ctx.strokeStyle =
            "#4c8050";


        ctx.lineWidth =
            2;


        ctx.beginPath();


        ctx.moveTo(
            21,
            -4
        );


        ctx.lineTo(
            20,
            -16
        );


        ctx.moveTo(
            28,
            -4
        );


        ctx.lineTo(
            29,
            -16
        );


        ctx.stroke();
    }


    else if (
        type ===
        "bad"
    ) {

        ctx.fillStyle =
            "#e5e5e5";


        ctx.strokeStyle =
            "#555555";


        ctx.lineWidth =
            3;


        ctx.beginPath();


        ctx.arc(
            0,
            -8,
            25,
            Math.PI,
            0
        );


        ctx.lineTo(
            23,
            17
        );


        ctx.lineTo(
            15,
            30
        );


        ctx.lineTo(
            -15,
            30
        );


        ctx.lineTo(
            -23,
            17
        );


        ctx.closePath();


        ctx.fill();


        ctx.stroke();


        ctx.shadowBlur =
            0;


        ctx.fillStyle =
            "#444444";


        ctx.beginPath();


        ctx.arc(
            -9,
            -7,
            6,
            0,
            Math.PI * 2
        );


        ctx.arc(
            9,
            -7,
            6,
            0,
            Math.PI * 2
        );


        ctx.fill();


        ctx.beginPath();


        ctx.moveTo(
            0,
            1
        );


        ctx.lineTo(
            -4,
            8
        );


        ctx.lineTo(
            4,
            8
        );


        ctx.closePath();


        ctx.fill();


        ctx.strokeStyle =
            "#444444";


        ctx.lineWidth =
            2;


        ctx.beginPath();


        ctx.moveTo(
            -10,
            16
        );


        ctx.lineTo(
            10,
            16
        );


        ctx.moveTo(
            -5,
            16
        );


        ctx.lineTo(
            -5,
            23
        );


        ctx.moveTo(
            0,
            16
        );


        ctx.lineTo(
            0,
            23
        );


        ctx.moveTo(
            5,
            16
        );


        ctx.lineTo(
            5,
            23
        );


        ctx.stroke();
    }


    ctx.restore();
}


// =====================================================
// ITEM
// =====================================================

function drawItem(
    obj
) {

    const point =
        perspectivePoint(
            obj.lane,
            obj.progress
        );


    const scale =
        0.22 +
        obj.progress *
        1.35;


    ctx.save();


    ctx.fillStyle =
        "rgba(50,50,50,.16)";


    ctx.beginPath();


    ctx.ellipse(
        point.x,
        point.y + 5 * scale,
        25 * scale,
        7 * scale,
        0,
        0,
        Math.PI * 2
    );


    ctx.fill();


    ctx.restore();


    drawItemIcon(
        obj.item,
        point.x,
        point.y -
        18 * scale,
        scale
    );
}


// =====================================================
// PLAYER
// =====================================================

function drawPlayer() {

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


    if (
        transformationEffect > 0
    ) {

        const elapsed =
            1.15 -
            transformationEffect;


        const pulse =
            Math.sin(
                elapsed * 18
            );


        scale *=
            1 +
            pulse *
            0.18;
    }


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


    if (
        transformationEffect > 0
    ) {

        const glow =
            20 +
            Math.sin(
                transformationEffect *
                18
            ) *
            12;


        ctx.shadowColor =
            "#fff2a3";


        ctx.shadowBlur =
            glow;
    }


    /*
     * 캐릭터를 회전시키지 않는다.
     * 변신 캐릭터가 뒤집히는 문제 방지.
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


    ctx.shadowBlur =
        0;


    if (
        transformationEffect > 0
    ) {

        ctx.font =
            "25px Arial";


        ctx.textAlign =
            "center";


        ctx.textBaseline =
            "middle";


        ctx.fillText(
            "✨",
            -48,
            -height + 15
        );


        ctx.fillText(
            "✨",
            48,
            -height / 2
        );


        ctx.fillText(
            "⭐",
            0,
            -height - 25
        );
    }


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
// FRIEND
// =====================================================

function drawFriend() {

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


    /*
     * 점프 중에는 친구가 살짝 위로 올라간다.
     */

    let jumpOffset =
        0;


    if (
        friend.jumping
    ) {

        const t =
            Math.min(
                1,
                (
                    elapsedTime -
                    friend.jumpStart
                )
                /
                friend.jumpDuration
            );


        /*
         * 포물선
         */

        jumpOffset =
            -80 *
            Math.sin(
                t * Math.PI
            );
    }


    ctx.save();


    ctx.translate(
        x,
        y + jumpOffset
    );


    /*
     * 핵심:
     *
     * 친구가 점프할 때만
     * 자신의 중심을 기준으로 한 바퀴 회전.
     */

    if (
        friend.jumping
    ) {

        ctx.rotate(
            friend.rotation
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
// TRANSFORMATION PARTICLES
// =====================================================

function drawTransformationParticles() {

    if (
        transformationParticles.length === 0
    ) {

        return;
    }


    transformationParticles.forEach(
        function(p) {

            const x =
                player.x +
                Math.cos(
                    p.angle
                ) *
                p.distance;


            const y =
                player.y -
                65 +
                Math.sin(
                    p.angle
                ) *
                p.distance;


            ctx.save();


            ctx.globalAlpha =
                Math.max(
                    0,
                    p.life / 1.2
                );


            ctx.fillStyle =
                "#fff4a3";


            ctx.shadowColor =
                "#ffffff";


            ctx.shadowBlur =
                12;


            ctx.font =
                `${p.size * 3}px Arial`;


            ctx.textAlign =
                "center";


            ctx.textBaseline =
                "middle";


            ctx.fillText(
                "✦",
                x,
                y
            );


            ctx.restore();
        }
    );
}


// =====================================================
// PARTICLES
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
                    -
                    0.5
                ) * 9,

            vy:
                (
                    Math.random()
                    -
                    0.5
                ) * 9,

            life:
                0.6,

            color:
                color
        });
    }
}


function updateParticles(
    dt
) {

    particles.forEach(
        function(p) {

            p.x +=
                p.vx *
                dt *
                60;


            p.y +=
                p.vy *
                dt *
                60;


            p.vy +=
                0.25 *
                dt *
                60;


            p.life -=
                dt;
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


function drawParticles() {

    particles.forEach(
        function(p) {

            ctx.globalAlpha =
                p.life /
                0.6;


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

    drawBackground();


    /*
     * 멀리 있는 물체부터 렌더링
     */

    const sortedObjects =
        [...objects].sort(
            function(a,b) {

                return (
                    a.progress -
                    b.progress
                );
            }
        );


    sortedObjects.forEach(
        function(obj) {

            const point =
                perspectivePoint(
                    obj.lane,
                    obj.progress
                );


            if (
                obj.type ===
                "jumpObstacle"
            ) {

                const scale =
                    0.18 +
                    obj.progress *
                    1.55;


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

                const scale =
                    0.18 +
                    obj.progress *
                    1.55;


                drawSlideObstacle(
                    point.x,
                    point.y,
                    scale
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


    /*
     * 친구
     */

    drawFriend();


    /*
     * 플레이어
     */

    drawPlayer();


    /*
     * 변신 효과
     */

    drawTransformationParticles();


    /*
     * 일반 파티클
     */

    drawParticles();
}


// =====================================================
// MAIN LOOP
// =====================================================

function loop(
    timestamp
) {

    if (
        lastTime === 0
    ) {

        lastTime =
            timestamp;
    }


    let dt =
        (
            timestamp -
            lastTime
        ) / 1000;


    lastTime =
        timestamp;


    /*
     * 탭 전환 등으로 엄청난 시간 차이가
     * 발생해도 캐릭터가 순간이동하지 않도록 제한
     */

    dt =
        Math.min(
            dt,
            MAX_DELTA
        );


    update(
        dt
    );


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
// START RENDER
// =====================================================

requestAnimationFrame(
    loop
);


</script>

</body>

</html>
"""


# =========================================================
# INSERT IMAGES
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
# RENDER
# =========================================================

components.html(
    game,
    height=700,
    scrolling=False
)
