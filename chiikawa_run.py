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

    st.caption(
        "파일 이름과 assets 폴더 위치를 확인하세요."
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

        visibility:
            hidden;
    }


    .block-container {

        padding-top:
            2px !important;

        padding-bottom:
            0 !important;

        max-width:
            1000px !important;
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

    box-sizing:
        border-box;

    -webkit-tap-highlight-color:
        transparent;
}


html,
body {

    margin:
        0;

    padding:
        0;

    width:
        100%;

    height:
        100%;

    overflow:
        hidden;

    background:
        transparent;

    font-family:
        Arial,
        sans-serif;
}


body {

    display:
        flex;

    justify-content:
        center;

    align-items:
        flex-start;
}


/* =====================================================
   GAME
   ===================================================== */

#gameWrap {

    width:
        100%;

    display:
        flex;

    justify-content:
        center;

    align-items:
        flex-start;
}


#game {

    position:
        relative;

    width:
        920px;

    height:
        650px;

    flex-shrink:
        0;
}


canvas {

    width:
        100%;

    height:
        100%;

    display:
        block;

    border-radius:
        20px;

    background:
        #ffffff;

    box-shadow:
        0 5px 18px
        rgba(80,60,70,.16);
}


/* =====================================================
   HUD
   ===================================================== */

.hud {

    position:
        absolute;

    top:
        10px;

    left:
        10px;

    right:
        10px;

    display:
        flex;

    justify-content:
        space-between;

    gap:
        6px;

    z-index:
        5;

    pointer-events:
        none;
}


.hudBox {

    background:
        rgba(255,255,255,.94);

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
   MENU
   ===================================================== */

#menu {

    position:
        absolute;

    inset:
        0;

    z-index:
        20;

    display:
        flex;

    justify-content:
        center;

    align-items:
        center;

    padding:
        12px;

    background:
        rgba(255,255,255,.12);

    border-radius:
        20px;

    overflow:
        hidden;
}


.menuCard {

    width:
        min(390px,82%);

    max-height:
        86%;

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
        clamp(21px,5vw,32px);

    margin-bottom:
        8px;
}


.description {

    color:
        #76666d;

    font-size:
        clamp(11px,2.8vw,15px);

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
   MOBILE CONTROL
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
        rgba(255,255,255,.94);

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
   MOBILE
   ===================================================== */

@media (max-width:600px) {

    #game {

        border-radius:
            14px;
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
            88%;

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
   VERY SHORT SCREEN
   ===================================================== */

@media (max-height:600px) {

    .menuCard {

        width:
            66%;

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

        line-height:
            1.2;

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
     MENU
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
            아이템을 획득합니다!

            <br>

            🪨 낮은 장애물은 점프!
            높은 장애물은 숙이기!

            <br>

            ✨ 점수에 따라 변신합니다!

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
     CONTROLS
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
// RESPONSIVE GAME
// =====================================================

function fitGameToScreen() {

    const game =
        document.getElementById(
            "game"
        );


    if (!game)
        return;


    let screenWidth =
        window.innerWidth;


    let screenHeight =
        window.innerHeight;


    /*
     * iframe 환경에서도
     * 가능한 화면 크기를 얻는다.
     */

    try {

        if (
            window.parent &&
            window.parent.innerWidth
        ) {

            screenWidth =
                Math.min(
                    screenWidth,
                    window.parent.innerWidth
                );
        }

        if (
            window.parent &&
            window.parent.innerHeight
        ) {

            screenHeight =
                Math.min(
                    screenHeight,
                    window.parent.innerHeight
                );
        }

    }
    catch (e) {

        // 무시
    }


    /*
     * 920 × 650 비율 유지
     */

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
// RUNNING ANIMATION
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
// BACKGROUND
// =====================================================

let skyOffset =
    0;


// =====================================================
// TRANSFORMATION EFFECT
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
// START
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
        .style
        .display =
            "none";
}


// =====================================================
// TOUCH BUTTON
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
// KEYBOARD
// =====================================================

document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key ===
            "ArrowLeft"
        ) {

            moveLeft();

            event.preventDefault();
        }


        if (
            event.key ===
            "ArrowRight"
        ) {

            moveRight();

            event.preventDefault();
        }


        if (
            event.key ===
            "ArrowUp" ||
            event.code ===
            "Space"
        ) {

            jump();

            event.preventDefault();
        }


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
// MOVE
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
// JUMP
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
    }
}


// =====================================================
// SLIDE
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
// SPAWN OBJECT
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
     * 낮은 장애물
     * 점프로 피한다.
     */

    if (
        r < 0.27
    ) {

        type =
            "jumpObstacle";
    }


    /*
     * 높은 장애물
     * 숙여서 피한다.
     */

    else if (
        r < 0.43
    ) {

        type =
            "slideObstacle";
    }


    /*
     * 랜덤박스
     */

    else if (
        r < 0.68
    ) {

        type =
            "box";
    }


    /*
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
// RANDOM BOX
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
// OBJECT COLLISION
// =====================================================

function objectIsAtPlayer(
    obj
) {

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
// TRANSFORMATION
// =====================================================

function transformationCheck() {

    let newForm =
        0;


    /*
     * 원본 변신 조건
     */

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


    /*
     * 새로운 변신
     */

    if (
        newForm >
        player.form
    ) {

        player.form =
            newForm;


        /*
         * 70 프레임 동안
         * 변신 효과
         */

        transformationEffect =
            70;


        transformationParticles =
            [];


        /*
         * 주변에서 별이 터져나온다.
         */

        for (
            let i = 0;
            i < 45;
            i++
        ) {

            transformationParticles.push({

                angle:
                    Math.random() *
                    Math.PI * 2,

                distance:
                    10 +
                    Math.random() * 35,

                speed:
                    1.2 +
                    Math.random() * 3,

                size:
                    3 +
                    Math.random() * 6,

                life:
                    60 +
                    Math.random() * 30
            });
        }


        /*
         * 중심에서도
         * 큰 빛이 터진다.
         */

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

function updateTransformation() {

    if (
        transformationEffect <= 0
    ) {

        return;
    }


    transformationEffect--;


    transformationParticles.forEach(
        function(p) {

            p.distance +=
                p.speed;

            p.life--;
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

function update() {

    if (!running)
        return;


    // -----------------------------------------------
    // distance
    // -----------------------------------------------

    distance +=
        speed;


    // -----------------------------------------------
    // score
    // -----------------------------------------------

    score +=
        0.28;


    // -----------------------------------------------
    // speed
    // -----------------------------------------------

    speed =
        Math.min(
            16,
            7 +
            distance / 6500
        );


    // -----------------------------------------------
    // transformation
    // -----------------------------------------------

    transformationCheck();


    updateTransformation();


    // -----------------------------------------------
    // player lane
    // -----------------------------------------------

    player.x +=
        (
            player.targetX -
            player.x
        ) * 0.2;


    // -----------------------------------------------
    // jump
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
    // slide
    // -----------------------------------------------

    if (
        player.sliding
    ) {

        player.slideTimer--;


        if (
            player.slideTimer <=
            0
        ) {

            player.sliding =
                false;
        }
    }


    // -----------------------------------------------
    // giant
    // -----------------------------------------------

    if (
        player.giant
    ) {

        player.giantTimer--;


        if (
            player.giantTimer <=
            0
        ) {

            player.giant =
                false;
        }
    }


    // -----------------------------------------------
    // shield
    // -----------------------------------------------

    if (
        player.shield
    ) {

        player.shieldTimer--;


        if (
            player.shieldTimer <=
            0
        ) {

            player.shield =
                false;
        }
    }


    // -----------------------------------------------
    // running animation
    // -----------------------------------------------

    animationTimer++;


    if (
        animationTimer >=
        8
    ) {

        animationTimer =
            0;


        animationFrame =
            animationFrame === 0
                ? 1
                : 0;
    }


    // -----------------------------------------------
    // road movement
    // -----------------------------------------------

    roadOffset +=
        speed;


    if (
        roadOffset >=
        100
    ) {

        roadOffset -=
            100;
    }


    // -----------------------------------------------
    // scenery
    // -----------------------------------------------

    sceneryOffset +=
        speed *
        1.25;


    if (
        sceneryOffset >=
        120
    ) {

        sceneryOffset -=
            120;
    }


    // -----------------------------------------------
    // background
    // -----------------------------------------------

    skyOffset +=
        speed *
        0.12;


    if (
        skyOffset >=
        HEIGHT
    ) {

        skyOffset -=
            HEIGHT;
    }


    // -----------------------------------------------
    // spawn
    // -----------------------------------------------

    spawnTimer--;


    if (
        spawnTimer <=
        0
    ) {

        spawnObject();


        spawnTimer =
            Math.max(
                28,
                68 -
                speed * 1.8
            );
    }


    // -----------------------------------------------
    // objects
    // -----------------------------------------------

    objects.forEach(
        function(obj) {

            /*
             * 멀리서는 천천히,
             * 가까워질수록 빠르게 접근
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


    // -----------------------------------------------
    // collision
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
        // box
        // -------------------------------------------

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
        // item
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
                12
            );


            objects.splice(
                i,
                1
            );


            continue;
        }


        // -------------------------------------------
        // jump obstacle
        // -------------------------------------------

        if (
            obj.type ===
            "jumpObstacle"
        ) {

            /*
             * 점프 중이면 통과
             */

            if (
                player.jumping
            ) {

                objects.splice(
                    i,
                    1
                );

                continue;
            }


            /*
             * 거대화하면 파괴
             */

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


            /*
             * 보호막
             */

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
        // slide obstacle
        // -------------------------------------------

        if (
            obj.type ===
            "slideObstacle"
        ) {

            /*
             * 숙이고 있으면 통과
             */

            if (
                player.sliding
            ) {

                objects.splice(
                    i,
                    1
                );

                continue;
            }


            /*
             * 보호막
             */

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
    // remove
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
    // particles
    // -----------------------------------------------

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
        .style
        .display =
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

    /*
     * background.jpg를
     * 하늘/주변 배경으로 사용
     */

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

        /*
         * background.jpg가 없을 때
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


    // -----------------------------------------------
    // horizon
    // -----------------------------------------------

    drawHorizon();


    // -----------------------------------------------
    // road
    // -----------------------------------------------

    drawRoad();


    // -----------------------------------------------
    // scenery
    // -----------------------------------------------

    drawSideScenery();
}


// =====================================================
// HORIZON
// =====================================================

function drawHorizon() {

    ctx.save();


    ctx.globalAlpha =
        0.35;


    ctx.fillStyle =
        "#a7cba4";


    ctx.beginPath();


    ctx.moveTo(
        0,
        HORIZON_Y + 28
    );


    ctx.lineTo(
        80,
        HORIZON_Y
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
        HORIZON_Y
    );


    ctx.lineTo(
        920,
        HORIZON_Y + 28
    );


    ctx.lineTo(
        920,
        HORIZON_Y + 75
    );


    ctx.lineTo(
        0,
        HORIZON_Y + 75
    );


    ctx.closePath();


    ctx.fill();


    ctx.restore();
}


// =====================================================
// WHITE ROAD
// =====================================================

function drawRoad() {

    /*
     * 흰색 도로
     *
     * 소실점에서 시작해서
     * 화면 하단 전체까지 연결한다.
     */

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


    // -----------------------------------------------
    // road shadow
    // -----------------------------------------------

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


    // -----------------------------------------------
    // WHITE ROAD
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


    // -----------------------------------------------
    // ROAD EDGE
    // -----------------------------------------------

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


    // -----------------------------------------------
    // LANES
    // -----------------------------------------------

    drawPerspectiveLane(
        0
    );


    drawPerspectiveLane(
        1
    );


    // -----------------------------------------------
    // ROAD TEXTURE
    // -----------------------------------------------

    drawRoadTexture();
}


// =====================================================
// PERSPECTIVE LANE
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


    /*
     * 회색 선
     */

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

    for (
        let i = -1;
        i < 11;
        i++
    ) {

        let progress =
            (
                i * 0.11
                +
                sceneryOffset / 120 *
                0.11
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
// BUSH
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
        "#9bcf93";


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
        "#74ba78";


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
// OBSTACLE
// =====================================================

function drawObstacle(
    obj
) {

    const point =
        perspectivePoint(
            obj.lane,
            obj.progress
        );


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


    /*
     * shadow
     */

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


    /*
     * obstacle
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
     * warning
     */

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


    /*
     * shadow
     */

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


    /*
     * posts
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
     * beam
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
     * slide indicator
     */

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
// RANDOM BOX
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
     * shadow
     */

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


    /*
     * box
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
     * shadow
     */

    ctx.fillStyle =
        "rgba(70,70,70,.18)";


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
     * item
     */

    ctx.font =
        `${Math.max(
            12,
            42 * scale
        )}px Arial`;


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
// PLAYER
// =====================================================

function drawPlayer() {

    /*
     * 기본
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


    /*
     * 변신 순간
     * 살짝 커졌다가 줄어드는 pulse
     */

    if (
        transformationEffect > 0
    ) {

        const elapsed =
            70 -
            transformationEffect;


        const pulse =
            Math.sin(
                elapsed * 0.35
            );


        scale *=
            1 +
            pulse * 0.18;
    }


    let width =
        105 * scale;


    let height =
        120 * scale;


    /*
     * 숙이기
     */

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
     * 변신 중 광채
     */

    if (
        transformationEffect > 0
    ) {

        const glow =
            20 +
            Math.sin(
                transformationEffect *
                0.4
            ) *
            12;


        ctx.shadowColor =
            "#fff2a3";


        ctx.shadowBlur =
            glow;
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


    ctx.shadowBlur =
        0;


    /*
     * 변신 순간 별
     */

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


    /*
     * 최종 변신 왕관
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
     * GIANT
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
     * SHIELD
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


    ctx.save();


    ctx.translate(
        x,
        y
    );


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

            const angle =
                p.angle;


            const x =
                player.x +
                Math.cos(
                    angle
                ) *
                p.distance;


            const y =
                player.y -
                65 +
                Math.sin(
                    angle
                ) *
                p.distance;


            ctx.save();


            ctx.globalAlpha =
                Math.max(
                    0,
                    p.life / 80
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
// PARTICLE
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
                35,

            color:
                color
        });
    }
}


// =====================================================
// UPDATE PARTICLES
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
// DRAW PARTICLES
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

    /*
     * 배경
     */

    drawBackground();


    /*
     * 멀리 있는 오브젝트부터
     * 가까운 오브젝트 순으로 그린다.
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


    /*
     * 친구
     */

    drawFriend();


    /*
     * 플레이어
     */

    drawPlayer();


    /*
     * 변신 별
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
// START LOOP
// =====================================================

loop();


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
# RUN
# =========================================================

components.html(
    game,
    height=700,
    scrolling=False
)
