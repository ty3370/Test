import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64


# =========================================================
# Streamlit 설정
# =========================================================

st.set_page_config(
    page_title="Chiikawa Run!",
    page_icon="🌸",
    layout="centered"
)


# =========================================================
# 파일 경로
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
        data = base64.b64encode(path.read_bytes()).decode("utf-8")

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

CHARACTER1 = image_to_base64("character1.png")
CHARACTER1_RUN2 = image_to_base64("character1_run2.png")

CHARACTER2 = image_to_base64("character2.png")
CHARACTER2_RUN2 = image_to_base64("character2_run2.png")

CHARACTER3 = image_to_base64("character3.png")
CHARACTER3_RUN2 = image_to_base64("character3_run2.png")

BACKGROUND = image_to_base64("background.jpg")


# =========================================================
# 이미지 파일 검사
# =========================================================

required_files = [
    "character1.png",
    "character1_run2.png",
    "character2.png",
    "character2_run2.png",
    "character3.png",
    "character3_run2.png",
    "background.jpg",
]

missing_files = [
    filename
    for filename in required_files
    if not (ASSETS / filename).exists()
]


if missing_files:
    st.warning("⚠️ 일부 이미지 파일을 찾을 수 없습니다.")

    st.code(
        "\n".join(
            f"assets/{filename}"
            for filename in missing_files
        )
    )

    st.caption(
        "위 파일 이름과 assets 폴더의 실제 파일 이름이 정확히 같은지 확인하세요."
    )


# =========================================================
# Streamlit 바깥쪽 CSS
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
        padding-top: 5px !important;
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

#gameWrap {

    width: 100%;

    display: flex;

    justify-content: center;
}

#game {

    width:
        min(920px, 100vw);

    position: relative;
}

canvas {

    width: 100%;
    height: auto;

    display: block;

    border-radius: 20px;

    background: #dff6ff;
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

    justify-content: space-between;

    gap: 6px;

    z-index: 5;

    pointer-events: none;
}

.hudBox {

    background:
        rgba(255,255,255,.92);

    color: #604850;

    font-weight: 900;

    font-size: 13px;

    padding: 6px 10px;

    border-radius: 13px;

    box-shadow:
        0 3px 8px
        rgba(0,0,0,.12);
}


/* =====================================================
   메뉴
   ===================================================== */

#menu {

    position: absolute;

    inset: 0;

    z-index: 20;

    display: flex;

    justify-content: center;

    align-items: center;

    padding: 12px;

    background:
        rgba(255,255,255,.20);

    border-radius: 20px;

    overflow: auto;
}

.menuCard {

    width:
        min(420px, 88%);

    max-height: 94%;

    background:
        rgba(255,255,255,.97);

    border-radius: 24px;

    padding: 18px 15px;

    text-align: center;

    box-shadow:
        0 10px 25px
        rgba(60,40,60,.22);

    overflow: auto;
}

.title {

    color: #5d3f47;

    font-weight: 900;

    font-size:
        clamp(23px, 6vw, 32px);

    margin-bottom: 8px;
}

.description {

    color: #76666d;

    font-size:
        clamp(12px, 3.2vw, 15px);

    line-height: 1.4;

    margin-bottom: 12px;
}


/* =====================================================
   캐릭터 선택
   ===================================================== */

.selectTitle {

    color: #604850;

    font-weight: 900;

    font-size: 16px;

    margin:
        10px 0 8px;
}

.characterGrid {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 7px;

    margin-bottom: 12px;
}

.characterCard {

    border: 3px solid
        transparent;

    background:
        #fff8fb;

    border-radius: 16px;

    padding: 7px 4px;

    cursor: pointer;

    transition:
        transform .12s,
        border-color .12s,
        background .12s;
}

.characterCard:hover {

    transform:
        translateY(-2px);
}

.characterCard.selected {

    border-color:
        #ff78a5;

    background:
        #fff0f5;

    box-shadow:
        0 4px 10px
        rgba(255,100,150,.18);
}

.characterPreview {

    width: 100%;
    height: 90px;

    object-fit: contain;

    display: block;
}

.characterName {

    color: #654a52;

    font-size: 11px;

    font-weight: 900;

    margin-top: 3px;
}


/* =====================================================
   버튼
   ===================================================== */

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
        0 5px 0 #d74d79;

    cursor: pointer;

    touch-action: manipulation;
}

.startButton:active {

    transform:
        translateY(4px);

    box-shadow: none;
}


/* =====================================================
   조작 버튼
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
        rgba(255,255,255,.9);

    color: #5d4b50;

    font-size: 18px;

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
   모바일
   ===================================================== */

@media (max-width: 600px) {

    #game {

        width: 100vw;
    }

    canvas {

        border-radius: 16px;
    }

    #menu {

        padding: 7px;
    }

    .menuCard {

        width: 82%;

        max-height: 90%;

        padding:
            13px 10px;

        border-radius: 20px;
    }

    .title {

        font-size: 21px;
    }

    .description {

        font-size: 11px;
    }

    .characterGrid {

        gap: 5px;
    }

    .characterPreview {

        height: 72px;
    }

    .characterName {

        font-size: 10px;
    }

    .startButton {

        padding:
            11px 12px;

        font-size: 14px;
    }

    .hud {

        top: 7px;

        left: 7px;
        right: 7px;
    }

    .hudBox {

        font-size: 10px;

        padding:
            5px 7px;
    }

    .controls {

        bottom: 6px;
    }

    .ctrl {

        width: 39px;
        height: 36px;

        font-size: 16px;
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
        ⭐ <span id="score">0</span>
    </div>

    <div class="hudBox">
        🏆 <span id="best">0</span>
    </div>

    <div class="hudBox">
        🎭 <span id="form">기본</span>
    </div>

    <div class="hudBox">
        💗 <span id="selectedName">치이카와</span>
    </div>

</div>


<!-- ===================================================
     메뉴 / 캐릭터 선택
     =================================================== -->

<div id="menu">

<div class="menuCard">

    <div class="title">
        🌸 CHIIKAWA RUN! 🌸
    </div>

    <div class="description">

        치이카와 친구들과 함께 달려보세요! 🏃

        <br><br>

        ◀ ▶ 이동 · ⬆ 점프 · ⬇ 슬라이드

        <br>

        🎁 랜덤박스를 먹으면
        좋은 아이템 또는 나쁜 아이템 등장!

        <br>

        🍄 거대화하면 장애물을 부술 수 있어요.

        <br>

        ✨ 점수가 올라가면 변신합니다.

    </div>


    <div class="selectTitle">
        캐릭터를 선택하세요 💗
    </div>


    <div class="characterGrid">

        <div
            class="characterCard selected"
            data-character="1"
            id="characterCard1"
        >

            <img
                class="characterPreview"
                src="__CHARACTER1__"
            >

            <div class="characterName">
                치이카와
            </div>

        </div>


        <div
            class="characterCard"
            data-character="2"
            id="characterCard2"
        >

            <img
                class="characterPreview"
                src="__CHARACTER2__"
            >

            <div class="characterName">
                하치와레
            </div>

        </div>


        <div
            class="characterCard"
            data-character="3"
            id="characterCard3"
        >

            <img
                class="characterPreview"
                src="__CHARACTER3__"
            >

            <div class="characterName">
                변신 치이카와
            </div>

        </div>

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
     모바일 조작
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

const character1 = new Image();

character1.src =
    "__CHARACTER1__";


const character1Run2 = new Image();

character1Run2.src =
    "__CHARACTER1_RUN2__";


const character2 = new Image();

character2.src =
    "__CHARACTER2__";


const character2Run2 = new Image();

character2Run2.src =
    "__CHARACTER2_RUN2__";


const character3 = new Image();

character3.src =
    "__CHARACTER3__";


const character3Run2 = new Image();

character3Run2.src =
    "__CHARACTER3_RUN2__";


const background = new Image();

background.src =
    "__BACKGROUND__";


// =====================================================
// Canvas
// =====================================================

const canvas =
    document.getElementById("canvas");

const ctx =
    canvas.getContext("2d");

const WIDTH =
    canvas.width;

const HEIGHT =
    canvas.height;


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

const menu =
    document.getElementById(
        "menu"
    );


// =====================================================
// 게임 상태
// =====================================================

let running = false;

let score = 0;

let best =
    Number(
        localStorage.getItem(
            "chiikawa_best"
        ) || 0
    );

let speed = 7;

let distance = 0;

let spawnTimer = 40;

let objects = [];

let particles = [];


// =====================================================
// 캐릭터 선택
// =====================================================

let selectedCharacter = 1;

let animationFrame = 0;

let animationTimer = 0;

const CHARACTER_NAMES = {

    1: "치이카와",

    2: "하치와레",

    3: "변신 치이카와"
};


// =====================================================
// 레인
// =====================================================

const lanes = [
    300,
    460,
    620
];


// =====================================================
// 플레이어
// =====================================================

let player = {

    lane: 1,

    x: 460,

    targetX: 460,

    y: 515,

    vy: 0,

    jumping: false,

    sliding: false,

    slideTimer: 0,

    giant: false,

    giantTimer: 0,

    shield: false,

    shieldTimer: 0,

    form: 0,

    turning: false,

    turnTimer: 0,

    rotation: 0
};


// =====================================================
// 캐릭터 이미지 선택
// =====================================================

function getCharacterImages() {

    if (selectedCharacter === 1) {

        return {
            normal: character1,
            run2: character1Run2
        };
    }


    if (selectedCharacter === 2) {

        return {
            normal: character2,
            run2: character2Run2
        };
    }


    return {
        normal: character3,
        run2: character3Run2
    };
}


// =====================================================
// 이미지가 로드됐는지 검사
// =====================================================

function imageReady(image) {

    return (
        image &&
        image.complete &&
        image.naturalWidth > 0
    );
}


// =====================================================
// 캐릭터 선택 UI
// =====================================================

function selectCharacter(number) {

    selectedCharacter =
        number;


    document
        .querySelectorAll(
            ".characterCard"
        )
        .forEach(
            function(card) {

                card.classList.remove(
                    "selected"
                );
            }
        );


    const selectedCard =
        document.getElementById(
            "characterCard" + number
        );


    if (selectedCard) {

        selectedCard.classList.add(
            "selected"
        );
    }


    document
        .getElementById(
            "selectedName"
        )
        .textContent =
            CHARACTER_NAMES[number];
}


// =====================================================
// 캐릭터 선택 버튼
// =====================================================

document
    .querySelectorAll(
        ".characterCard"
    )
    .forEach(
        function(card) {

            card.addEventListener(
                "pointerdown",
                function(event) {

                    event.preventDefault();

                    const number =
                        Number(
                            card.dataset.character
                        );

                    selectCharacter(
                        number
                    );
                }
            );
        }
    );


// =====================================================
// START
// =====================================================

function startGame() {

    running = true;

    score = 0;

    speed = 7;

    distance = 0;

    spawnTimer = 40;

    objects = [];

    particles = [];

    animationFrame = 0;

    animationTimer = 0;


    player = {

        lane: 1,

        x: 460,

        targetX: 460,

        y: 515,

        vy: 0,

        jumping: false,

        sliding: false,

        slideTimer: 0,

        giant: false,

        giantTimer: 0,

        shield: false,

        shieldTimer: 0,

        form: 0,

        turning: false,

        turnTimer: 0,

        rotation: 0
    };


    document
        .getElementById("form")
        .textContent =
            "기본";


    document
        .getElementById(
            "selectedName"
        )
        .textContent =
            CHARACTER_NAMES[
                selectedCharacter
            ];


    menu.style.display =
        "none";
}


// =====================================================
// 모바일 버튼
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
// 이동
// =====================================================

function moveLeft() {

    if (!running)
        return;


    if (player.lane > 0) {

        player.lane--;

        player.targetX =
            lanes[
                player.lane
            ];
    }
}


function moveRight() {

    if (!running)
        return;


    if (player.lane < 2) {

        player.lane++;

        player.targetX =
            lanes[
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


    if (!player.jumping) {

        player.jumping = true;

        player.vy = -18;

        player.rotation = 0;
    }
}


// =====================================================
// 슬라이드
// =====================================================

function slide() {

    if (!running)
        return;


    if (!player.jumping) {

        player.sliding = true;

        player.slideTimer = 38;
    }
}


// =====================================================
// 키보드
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
// 오브젝트 생성
// =====================================================

function spawnObject() {

    const lane =
        Math.floor(
            Math.random() * 3
        );


    const r =
        Math.random();


    let type =
        "obstacle";


    let item = null;


    if (r < 0.45) {

        type =
            "obstacle";

    }
    else if (r < 0.70) {

        type =
            "box";

    }
    else {

        type =
            "item";


        const q =
            Math.random();


        if (q < 0.18)
            item = "giant";

        else if (q < 0.36)
            item = "score";

        else if (q < 0.52)
            item = "shield";

        else if (q < 0.68)
            item = "slow";

        else if (q < 0.84)
            item = "speed";

        else
            item = "bad";
    }


    objects.push({

        lane: lane,

        x: lanes[lane],

        y: -80,

        type: type,

        item: item
    });
}


// =====================================================
// 아이템
// =====================================================

function getItem(item) {

    if (item === "giant") {

        player.giant = true;

        player.giantTimer = 420;
    }


    if (item === "score") {

        score += 500;
    }


    if (item === "shield") {

        player.shield = true;

        player.shieldTimer = 360;
    }


    if (item === "slow") {

        speed =
            Math.max(
                4,
                speed - 2
            );
    }


    if (item === "speed") {

        score += 250;

        speed =
            Math.min(
                16,
                speed + 1
            );
    }


    if (item === "bad") {

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


    if (r < 0.20)
        item = "giant";

    else if (r < 0.40)
        item = "score";

    else if (r < 0.58)
        item = "shield";

    else if (r < 0.72)
        item = "slow";

    else if (r < 0.86)
        item = "speed";

    else
        item = "bad";


    getItem(item);


    burst(
        obj.x,
        obj.y,
        "#ffd447",
        22
    );
}


// =====================================================
// 충돌
// =====================================================

function hit(
    playerObj,
    obj
) {

    return (

        playerObj.lane ===
            obj.lane

        &&

        Math.abs(
            playerObj.y -
            obj.y
        ) < 70
    );
}


// =====================================================
// 변신
// =====================================================

function transformationCheck() {

    let newForm = 0;


    /*
     * 선택한 캐릭터가 3번이면
     * 이미 변신 상태이므로
     * form은 2로 유지
     */

    if (
        selectedCharacter === 3
    ) {

        newForm = 2;

    }
    else {

        if (score >= 5000) {

            newForm = 2;

        }
        else if (score >= 2500) {

            newForm = 1;
        }
    }


    if (
        newForm >
        player.form
    ) {

        player.form =
            newForm;

        player.turning = true;

        player.turnTimer = 120;


        burst(
            player.x,
            player.y - 70,
            "#ff9fc0",
            30
        );
    }


    let text = "기본";


    if (
        player.form === 1
    )
        text =
            "✨ 변신";


    if (
        player.form === 2
    )
        text =
            "👑 최종";


    document
        .getElementById("form")
        .textContent =
            text;
}


// =====================================================
// UPDATE
// =====================================================

function update() {

    if (!running)
        return;


    distance += speed;


    score += 0.28;


    speed =
        Math.min(
            16,
            7 +
            distance / 6500
        );


    transformationCheck();


    // 레인 이동

    player.x +=
        (
            player.targetX -
            player.x
        ) * 0.2;


    // 점프

    if (player.jumping) {

        player.vy += 1;

        player.y +=
            player.vy;


        if (
            player.y >= 515
        ) {

            player.y = 515;

            player.vy = 0;

            player.jumping = false;
        }
    }


    // 슬라이드

    if (player.sliding) {

        player.slideTimer--;


        if (
            player.slideTimer <= 0
        ) {

            player.sliding = false;
        }
    }


    // 거대화

    if (player.giant) {

        player.giantTimer--;


        if (
            player.giantTimer <= 0
        ) {

            player.giant = false;
        }
    }


    // 보호막

    if (player.shield) {

        player.shieldTimer--;


        if (
            player.shieldTimer <= 0
        ) {

            player.shield = false;
        }
    }


    // 뒤돌아보기

    if (player.turning) {

        player.turnTimer--;


        if (
            player.turnTimer <= 0
        ) {

            player.turning = false;
        }
    }


    // 달리기 애니메이션

    animationTimer++;


    if (
        animationTimer >= 8
    ) {

        animationTimer = 0;

        animationFrame =
            animationFrame === 0
                ? 1
                : 0;
    }


    // 생성

    spawnTimer--;


    if (
        spawnTimer <= 0
    ) {

        spawnObject();


        spawnTimer =
            Math.max(
                28,
                75 -
                speed * 2
            );
    }


    // 오브젝트 이동

    objects.forEach(
        function(obj) {

            obj.y += speed;
        }
    );


    // 충돌

    for (
        let i =
            objects.length - 1;

        i >= 0;

        i--
    ) {

        const obj =
            objects[i];


        if (
            !hit(
                player,
                obj
            )
        )
            continue;


        if (
            obj.type ===
            "box"
        ) {

            openBox(obj);

            objects.splice(
                i,
                1
            );

            continue;
        }


        if (
            obj.type ===
            "item"
        ) {

            getItem(
                obj.item
            );

            objects.splice(
                i,
                1
            );

            continue;
        }


        if (
            obj.type ===
            "obstacle"
        ) {

            if (
                player.jumping
            )
                continue;


            if (
                player.giant
            ) {

                score += 200;


                burst(
                    obj.x,
                    obj.y,
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
    }


    // 화면 밖 오브젝트 제거

    objects =
        objects.filter(
            function(obj) {

                return (
                    obj.y <
                    HEIGHT + 100
                );
            }
        );


    updateParticles();
}


// =====================================================
// GAME OVER
// =====================================================

function gameOver() {

    running = false;


    const finalScore =
        Math.floor(score);


    if (
        finalScore > best
    ) {

        best =
            finalScore;


        localStorage.setItem(
            "chiikawa_best",
            best
        );
    }


    menu.innerHTML = `

        <div class="menuCard">

            <div class="title">
                💥 GAME OVER
            </div>

            <div class="description">

                ${CHARACTER_NAMES[selectedCharacter]}
                로 달린 기록

                <br><br>

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

                🏆 최고 점수 ${best}

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
// BACKGROUND
// =====================================================

function drawBackground() {

    if (
        imageReady(background)
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
            "#bfeaff"
        );


        gradient.addColorStop(
            1,
            "#d9efc9"
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


    // 달리는 길

    ctx.fillStyle =
        "rgba(220,205,185,.65)";


    ctx.beginPath();


    ctx.moveTo(
        230,
        300
    );


    ctx.lineTo(
        690,
        300
    );


    ctx.lineTo(
        860,
        HEIGHT
    );


    ctx.lineTo(
        60,
        HEIGHT
    );


    ctx.closePath();

    ctx.fill();


    // 레인

    ctx.strokeStyle =
        "rgba(255,255,255,.72)";


    ctx.lineWidth = 7;


    ctx.beginPath();


    ctx.moveTo(
        390,
        300
    );


    ctx.lineTo(
        325,
        HEIGHT
    );


    ctx.stroke();


    ctx.beginPath();


    ctx.moveTo(
        530,
        300
    );


    ctx.lineTo(
        595,
        HEIGHT
    );


    ctx.stroke();
}


// =====================================================
// 장애물
// =====================================================

function drawObstacle(obj) {

    ctx.fillStyle =
        "#ff779e";


    ctx.strokeStyle =
        "#67404a";


    ctx.lineWidth = 5;


    ctx.beginPath();


    ctx.roundRect(
        obj.x - 35,
        obj.y - 35,
        70,
        70,
        15
    );


    ctx.fill();

    ctx.stroke();


    ctx.fillStyle =
        "white";


    ctx.font =
        "bold 30px Arial";


    ctx.textAlign =
        "center";


    ctx.textBaseline =
        "middle";


    ctx.fillText(
        "!",
        obj.x,
        obj.y
    );
}


// =====================================================
// 랜덤박스
// =====================================================

function drawBox(obj) {

    ctx.fillStyle =
        "#ffd447";


    ctx.strokeStyle =
        "#9b7430";


    ctx.lineWidth = 5;


    ctx.fillRect(
        obj.x - 32,
        obj.y - 32,
        64,
        64
    );


    ctx.strokeRect(
        obj.x - 32,
        obj.y - 32,
        64,
        64
    );


    ctx.fillStyle =
        "white";


    ctx.font =
        "bold 35px Arial";


    ctx.textAlign =
        "center";


    ctx.textBaseline =
        "middle";


    ctx.fillText(
        "?",
        obj.x,
        obj.y
    );
}


// =====================================================
// 아이템
// =====================================================

function drawItem(obj) {

    const icons = {

        giant: "🍄",

        score: "💎",

        shield: "🛡️",

        slow: "🐌",

        speed: "⚡",

        bad: "💀"
    };


    ctx.font =
        "46px Arial";


    ctx.textAlign =
        "center";


    ctx.textBaseline =
        "middle";


    ctx.fillText(
        icons[obj.item],
        obj.x,
        obj.y
    );
}


// =====================================================
// 플레이어
// =====================================================

function drawPlayer() {

    let images;


    /*
     * 캐릭터 선택
     *
     * 1 = 치이카와
     * 2 = 하치와레
     * 3 = 변신 치이카와
     */

    if (
        selectedCharacter === 3
    ) {

        images = {

            normal:
                character3,

            run2:
                character3Run2
        };

    }
    else if (
        selectedCharacter === 2
    ) {

        images = {

            normal:
                character2,

            run2:
                character2Run2
        };

    }
    else {

        /*
         * 치이카와는 점수에 따라
         * 변신 캐릭터 이미지로 변경
         */

        if (
            player.form >= 1
        ) {

            images = {

                normal:
                    character3,

                run2:
                    character3Run2
            };

        }
        else {

            images = {

                normal:
                    character1,

                run2:
                    character1Run2
            };
        }
    }


    let image =
        animationFrame === 0
            ? images.normal
            : images.run2;


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

        width = 110;

        height = 70;
    }


    ctx.save();


    ctx.translate(
        player.x,
        player.y
    );


    if (
        player.turning
    ) {

        ctx.rotate(
            Math.PI
        );
    }


    if (
        imageReady(image)
    ) {

        ctx.drawImage(
            image,
            -width / 2,
            -height,
            width,
            height
        );

    }
    else {

        // 이미지가 없을 때 표시할 임시 캐릭터

        ctx.fillStyle =
            "#ffffff";

        ctx.strokeStyle =
            "#67404a";

        ctx.lineWidth = 4;


        ctx.beginPath();

        ctx.arc(
            0,
            -70,
            42,
            0,
            Math.PI * 2
        );

        ctx.fill();

        ctx.stroke();


        ctx.fillStyle =
            "#ff9fba";

        ctx.beginPath();

        ctx.arc(
            -14,
            -65,
            5,
            0,
            Math.PI * 2
        );

        ctx.arc(
            14,
            -65,
            5,
            0,
            Math.PI * 2
        );

        ctx.fill();
    }


    // 최종 단계 왕관

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


    // 거대화

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


    // 보호막

    if (
        player.shield
    ) {

        ctx.strokeStyle =
            "#63dcff";


        ctx.lineWidth = 5;


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
// 파티클
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

            x: x,

            y: y,

            vx:
                (
                    Math.random() -
                    0.5
                ) * 9,

            vy:
                (
                    Math.random() -
                    0.5
                ) * 9,

            life: 35,

            color: color
        });
    }
}


function updateParticles() {

    particles.forEach(
        function(p) {

            p.x += p.vx;

            p.y += p.vy;

            p.vy += 0.25;

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


    ctx.globalAlpha = 1;
}


// =====================================================
// DRAW
// =====================================================

function draw() {

    drawBackground();


    objects.forEach(
        function(obj) {

            if (
                obj.type ===
                "obstacle"
            ) {

                drawObstacle(obj);

            }
            else if (
                obj.type ===
                "box"
            ) {

                drawBox(obj);

            }
            else {

                drawItem(obj);
            }
        }
    );


    drawPlayer();


    drawParticles();
}


// =====================================================
// LOOP
// =====================================================

function loop() {

    update();

    draw();


    document
        .getElementById("score")
        .textContent =
            Math.floor(score);


    document
        .getElementById("best")
        .textContent =
            Math.max(
                best,
                Math.floor(score)
            );


    requestAnimationFrame(
        loop
    );
}


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
