/* =========================================================
   AVENGINEERS - AIRCRAFT SCROLL ANIMATION
   ========================================================= */

(function () {

    "use strict";

    const FRAME_COUNT = 300;

    // Increase this if aircraft looks too small
    const ZOOM = 1.15;

    // Lower = slower / smoother
    const SMOOTHNESS = 0.025;


    /* =====================================================
       GET ELEMENTS
    ===================================================== */

    const canvas = document.getElementById("sequenceCanvas");
    const scene = document.querySelector(".scroll-scene");
    const content = document.querySelector(".scene-content");
    const progressBar = document.querySelector(".scene-progress-bar");

    if (!canvas) {
        console.error("❌ Canvas not found");
        return;
    }

    if (!scene) {
        console.error("❌ .scroll-scene not found");
        return;
    }

    if (typeof STATIC_FRAME_BASE === "undefined") {
        console.error("❌ STATIC_FRAME_BASE not found");
        return;
    }


    const ctx = canvas.getContext("2d");


    /* =====================================================
       VARIABLES
    ===================================================== */

    const frames = new Array(FRAME_COUNT);

    let currentFrame = 0;

    let loadedFrames = 0;

    let targetProgress = 0;

    let currentProgress = 0;

    let firstFrameReady = false;


    /* =====================================================
       CANVAS SIZE
    ===================================================== */

    function resizeCanvas() {

        const width = window.innerWidth;
        const height = window.innerHeight;

        const dpr = Math.min(
            window.devicePixelRatio || 1,
            2
        );


        canvas.width = width * dpr;
        canvas.height = height * dpr;


        canvas.style.width = width + "px";
        canvas.style.height = height + "px";


        ctx.setTransform(
            dpr,
            0,
            0,
            dpr,
            0,
            0
        );


        if (firstFrameReady) {
            drawFrame(currentFrame);
        }

    }


    /* =====================================================
       DRAW IMAGE
    ===================================================== */

    function drawFrame(index) {

        const image = frames[index];

        if (!image) {
            return;
        }

        if (!image.complete) {
            return;
        }

        if (image.naturalWidth === 0) {
            return;
        }


        const screenWidth = window.innerWidth;
        const screenHeight = window.innerHeight;


        const imageWidth = image.naturalWidth;
        const imageHeight = image.naturalHeight;


        /* =================================================
           COVER SCREEN
        ================================================= */

        let scale = Math.max(
            screenWidth / imageWidth,
            screenHeight / imageHeight
        );


        /* =================================================
           EXTRA ZOOM
        ================================================= */

        scale = scale * ZOOM;


        const width = imageWidth * scale;
        const height = imageHeight * scale;


        const x = (
            screenWidth - width
        ) / 2;


        const y = (
            screenHeight - height
        ) / 2;


        /* =================================================
           CLEAR
        ================================================= */

        ctx.clearRect(
            0,
            0,
            screenWidth,
            screenHeight
        );


        /* =================================================
           DRAW
        ================================================= */

        ctx.drawImage(
            image,
            x,
            y,
            width,
            height
        );

    }


    /* =====================================================
       LOAD FIRST FRAME
       ===================================================== */

    function loadFirstFrame() {

        const image = new Image();

        image.onload = function () {

            frames[0] = image;

            loadedFrames++;

            firstFrameReady = true;

            currentFrame = 0;

            drawFrame(0);

            console.log(
                "✅ FRAME 001 DISPLAYED"
            );

        };


        image.onerror = function () {

            console.error(
                "❌ Cannot load:",
                STATIC_FRAME_BASE +
                "frame-001.jpg"
            );

        };


        image.src =
            STATIC_FRAME_BASE +
            "frame-001.jpg";

    }


    /* =====================================================
       LOAD REMAINING FRAMES
       ===================================================== */

    function loadRemainingFrames() {

        for (
            let i = 2;
            i <= FRAME_COUNT;
            i++
        ) {

            const index = i - 1;

            const image = new Image();


            image.onload = function () {

                frames[index] = image;

                loadedFrames++;


                if (
                    loadedFrames % 25 === 0 ||
                    loadedFrames === FRAME_COUNT
                ) {

                    console.log(
                        "Frames loaded:",
                        loadedFrames +
                        "/" +
                        FRAME_COUNT
                    );

                }

            };


            image.onerror = function () {

                console.warn(
                    "Frame failed:",
                    i
                );

            };


            image.src =
                STATIC_FRAME_BASE +
                "frame-" +
                String(i).padStart(3, "0") +
                ".jpg";


        }

    }


    /* =====================================================
       GET SCROLL PROGRESS
       ===================================================== */

    function getScrollProgress() {

        const rect =
            scene.getBoundingClientRect();


        const totalScroll =
            scene.offsetHeight -
            window.innerHeight;


        if (totalScroll <= 0) {
            return 0;
        }


        const distance =
            -rect.top;


        let progress =
            distance / totalScroll;


        progress = Math.max(
            0,
            Math.min(
                1,
                progress
            )
        );


        return progress;

    }


    /* =====================================================
       SCROLL
       ===================================================== */

    function handleScroll() {

        targetProgress =
            getScrollProgress();

    }


    /* =====================================================
       ANIMATION
       ===================================================== */

    function animate() {


        /* =================================================
           SMOOTH SCROLL
        ================================================= */

        currentProgress += (
            targetProgress -
            currentProgress
        ) * SMOOTHNESS;


        if (
            Math.abs(
                targetProgress -
                currentProgress
            ) < 0.0001
        ) {

            currentProgress =
                targetProgress;

        }


        /* =================================================
           FRAME
        ================================================= */

        const frameNumber =
            Math.floor(
                currentProgress *
                (FRAME_COUNT - 1)
            );


        if (
            frames[frameNumber]
        ) {

            if (
                frameNumber !== currentFrame
            ) {

                currentFrame =
                    frameNumber;

                drawFrame(
                    currentFrame
                );

            }

        }


        /* =================================================
           INTRO TEXT
        ================================================= */

        if (content) {

            const fade =
                Math.max(
                    0,
                    1 -
                    currentProgress / 0.20
                );


            content.style.opacity =
                fade;


            const movement =
                (1 - fade) * -50;


            content.style.transform =
                "translate(-50%, calc(-50% + " +
                movement +
                "px))";

        }


        /* =================================================
           PROGRESS BAR
        ================================================= */

        if (progressBar) {

            progressBar.style.width =
                (
                    currentProgress * 100
                ) + "%";

        }


        requestAnimationFrame(
            animate
        );

    }


    /* =====================================================
       START
       ===================================================== */

    resizeCanvas();

    loadFirstFrame();

    loadRemainingFrames();

    handleScroll();

    requestAnimationFrame(
        animate
    );


    /* =====================================================
       EVENTS
       ===================================================== */

    window.addEventListener(
        "resize",
        resizeCanvas
    );


    window.addEventListener(
        "scroll",
        handleScroll,
        {
            passive: true
        }
    );


})();