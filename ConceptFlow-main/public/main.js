// --- STATE ---
let scene = null;
let isPlaying = false;
let currentTime = 0;
let rafId = null;
let lastTime = 0;
let mediaRecorder = null;
let recordedChunks = [];
let spokenActions = new Set(); // Track which narratives have been spoken

// --- DOM ELEMENTS ---
const promptInput = document.getElementById('promptInput');
const generateBtn = document.getElementById('generateBtn');
const jsonEditor = document.getElementById('jsonEditor');
const codeViewer = document.getElementById('codeViewer');
const applyJsonBtn = document.getElementById('applyJsonBtn');
const canvas = document.getElementById('previewCanvas');
const ctx = canvas.getContext('2d');
const playPauseBtn = document.getElementById('playPauseBtn');
const resetBtn = document.getElementById('resetBtn');
const timelineScrub = document.getElementById('timelineScrub');
const timeDisplay = document.getElementById('timeDisplay');
const exportBtn = document.getElementById('exportBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const errorToast = document.getElementById('errorToast');
const errorMessage = document.getElementById('errorMessage');
const breakdownList = document.getElementById('breakdownList');
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const narratorToggle = document.getElementById('narratorToggle');
const voiceBtn = document.getElementById('voiceBtn');

// --- CONSTANTS ---
const API_URL = ''; // Uses relative path for production

// --- INITIALIZATION ---
function init() {
    generateBtn.addEventListener('click', handleGenerate);
    if (voiceBtn) {
        voiceBtn.addEventListener('click', handleVoiceInput);
    }
    applyJsonBtn.addEventListener('click', handleApplyJson);
    playPauseBtn.addEventListener('click', togglePlay);
    resetBtn.addEventListener('click', resetPlayback);
    timelineScrub.addEventListener('input', handleScrub);
    exportBtn.addEventListener('click', handleExport);

    // Fullscreen
    const fullscreenBtn = document.getElementById('fullscreenBtn');
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', () => {
            if (!document.fullscreenElement) {
                canvas.requestFullscreen().catch(err => {
                    showError(`Error attempting to enable full-screen mode: ${err.message} (${err.name})`);
                });
            } else {
                document.exitFullscreen();
            }
        });
    }

    // Tab Switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
        });
    });

    // Initial clear
    ctx.fillStyle = '#1a1c2c'; // Dark theme bg
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#a0a0a0';
    ctx.font = '20px Inter';
    ctx.textAlign = 'center';
    ctx.fillText('Enter a prompt to generate a scene', canvas.width / 2, canvas.height / 2);
}

function handleVoiceInput() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        showError('Voice input is not supported in this browser.');
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
        voiceBtn.classList.add('listening');
    };

    recognition.onend = () => {
        voiceBtn.classList.remove('listening');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        promptInput.value = transcript;
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        voiceBtn.classList.remove('listening');
        showError('Voice recognition error: ' + event.error);
    };

    recognition.start();
}

// --- API HANDLERS ---
async function handleGenerate() {
    const text = promptInput.value.trim();
    if (!text) return showError('Please enter a description');

    showLoader(true);
    try {
        const res = await fetch(`${API_URL}/generate/scenes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description: text, options: {} })
        });

        const data = await res.json();

        if (!res.ok) {
            showError(data.error || 'Generation failed');
            if (data.suggestedPrompt) {
                console.log('Suggested Prompt:', data.suggestedPrompt);
            }
            return;
        }

        loadScene(data);
    } catch (err) {
        showError('Network error. Is Flask running?');
        console.error(err);
    } finally {
        showLoader(false);
    }
}

// --- SCENE MANAGEMENT ---
function loadScene(newScene) {
    scene = newScene;

    // Update UI
    jsonEditor.value = JSON.stringify(scene, null, 2);
    codeViewer.value = scene.code || "# No code available for this scene.";
    timelineScrub.max = scene.duration;

    // Resize canvas
    canvas.width = scene.width;
    canvas.height = scene.height;

    // Render Breakdown
    renderBreakdown(scene);

    // Reset Playback
    resetPlayback();
}

function renderBreakdown(scene) {
    breakdownList.innerHTML = '';
    if (!scene.actions || scene.actions.length === 0) {
        breakdownList.innerHTML = '<div class="empty-state">No actions in this scene.</div>';
        return;
    }

    const actions = [...scene.actions].sort((a, b) => a.start - b.start);

    actions.forEach(action => {
        const div = document.createElement('div');
        div.className = 'breakdown-item';
        div.id = `step-${action.id}`;

        const timeSpan = document.createElement('span');
        timeSpan.className = 'breakdown-time';
        timeSpan.textContent = `${action.start}s`;

        const descSpan = document.createElement('span');
        // Use narrative if available, else fallback
        descSpan.textContent = action.narrative || `${action.type.toUpperCase()} object '${action.objectId}'`;

        div.appendChild(timeSpan);
        div.appendChild(descSpan);
        breakdownList.appendChild(div);
    });
}

function handleApplyJson() {
    try {
        const parsed = JSON.parse(jsonEditor.value);
        loadScene(parsed);
    } catch (e) {
        showError('Invalid JSON');
    }
}

// --- ANIMATION ENGINE ---
function togglePlay() {
    if (isPlaying) pause();
    else play();
}

function play() {
    if (!scene) return;
    isPlaying = true;
    playPauseBtn.textContent = '⏸ Pause';
    lastTime = performance.now();
    rafId = requestAnimationFrame(loop);
}

function pause() {
    isPlaying = false;
    playPauseBtn.textContent = '▶ Play';
    cancelAnimationFrame(rafId);
    window.speechSynthesis.cancel(); // Stop talking
}

function resetPlayback() {
    pause();
    currentTime = 0;
    spokenActions.clear();
    updateTimeline();
    render(0);

    // Reset active breakdown items
    document.querySelectorAll('.breakdown-item').forEach(el => el.classList.remove('active'));
}

function handleScrub() {
    currentTime = parseFloat(timelineScrub.value);
    // When scrubbing, we don't want TTS to fire crazily
    // So we mark all previous actions as "spoken" to avoid backlog
    scene.actions.forEach(a => {
        if (a.start < currentTime) spokenActions.add(a.id);
        else spokenActions.delete(a.id);
    });

    updateTimeline();
    render(currentTime);
    if (isPlaying) lastTime = performance.now();
}

function loop(timestamp) {
    if (!isPlaying) return;

    const dt = (timestamp - lastTime) / 1000;
    lastTime = timestamp;

    currentTime += dt;

    if (currentTime >= scene.duration) {
        currentTime = scene.duration;
        pause();
    }

    updateTimeline();
    render(currentTime);
    checkNarrative();

    if (isPlaying) rafId = requestAnimationFrame(loop);
}

function updateTimeline() {
    timelineScrub.value = currentTime;
    timeDisplay.textContent = `${currentTime.toFixed(1)}s / ${scene.duration.toFixed(1)}s`;
}

function checkNarrative() {
    if (!narratorToggle.checked) return;

    scene.actions.forEach(action => {
        // Trigger slightly before start or at start
        if (currentTime >= action.start && !spokenActions.has(action.id)) {
            spokenActions.add(action.id);

            // Highlight step
            document.querySelectorAll('.breakdown-item').forEach(el => el.classList.remove('active'));
            const stepEl = document.getElementById(`step-${action.id}`);
            if (stepEl) {
                stepEl.classList.add('active');
                stepEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }

            // Speak
            if (action.narrative) {
                const u = new SpeechSynthesisUtterance(action.narrative);
                window.speechSynthesis.speak(u);
            }
        }
    });
}

// --- RENDERING CORE ---
function render(t) {
    if (!scene) return;

    // Clear
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Draw Background (if not in objects)
    // Actually, let's force a nice background if none exists, or use object 0
    // But for "Glass" look, maybe transparent? No, canvas needs opaque for video export.
    // Let's stick to object rendering.

    const objectStates = {};

    scene.objects.forEach(obj => {
        objectStates[obj.id] = { ...obj.props, type: obj.type, id: obj.id };
        if (objectStates[obj.id].opacity === undefined) objectStates[obj.id].opacity = 1;
        if (objectStates[obj.id].scale === undefined) objectStates[obj.id].scale = 1;
        if (objectStates[obj.id].rotation === undefined) objectStates[obj.id].rotation = 0;
        if (objectStates[obj.id].x === undefined) objectStates[obj.id].x = 0;
        if (objectStates[obj.id].y === undefined) objectStates[obj.id].y = 0;
    });

    const actions = [...scene.actions].sort((a, b) => a.start - b.start);

    actions.forEach(action => {
        const obj = objectStates[action.objectId];
        if (!obj) return;
        if (t < action.start) return;

        let p = (t - action.start) / (action.end - action.start);
        if (p > 1) p = 1;
        if (p < 0) p = 0;

        switch (action.type) {
            case 'translate':
                const targetX = action.params.to.x;
                const targetY = action.params.to.y;
                const startX = obj.x;
                const startY = obj.y;
                obj.x = startX + (targetX - startX) * p;
                obj.y = startY + (targetY - startY) * p;
                break;
            case 'scale':
                const startScale = obj.scale;
                const targetScale = action.params.scale;
                obj.scale = startScale + (targetScale - startScale) * p;
                break;
            case 'rotate':
                const startRot = obj.rotation;
                const targetRot = action.params.rotation;
                if (targetRot !== undefined) {
                    obj.rotation = startRot + (targetRot - startRot) * p;
                }
                break;
            case 'fade':
                const startOp = obj.opacity;
                const targetOp = action.params.opacity;
                obj.opacity = startOp + (targetOp - startOp) * p;
                break;
            case 'followPath':
                const pathId = action.params.pathId;
                const pathObj = scene.objects.find(o => o.id === pathId);
                if (pathObj && pathObj.type === 'path') {
                    const pathEl = document.createElementNS("http://www.w3.org/2000/svg", "path");
                    pathEl.setAttribute("d", pathObj.props.d);
                    const len = pathEl.getTotalLength();
                    const pt = pathEl.getPointAtLength(p * len);
                    obj.x = pt.x;
                    obj.y = pt.y;
                }
                break;
        }
    });

    scene.objects.forEach(rawObj => {
        const state = objectStates[rawObj.id];
        drawObject(ctx, state);
    });
}

function drawObject(ctx, obj) {
    if (obj.opacity <= 0) return;

    ctx.save();
    ctx.globalAlpha = obj.opacity;

    // Add Shadow for depth (Premium Look)
    if (obj.type !== 'bg' && obj.type !== 'axis') {
        ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
        ctx.shadowBlur = 10;
        ctx.shadowOffsetX = 2;
        ctx.shadowOffsetY = 4;
    }

    let cx = obj.x, cy = obj.y;
    if (obj.type === 'rect' || obj.type === 'bar') {
        cx = obj.x + obj.width / 2;
        cy = obj.y + obj.height / 2;
    }

    ctx.translate(cx, cy);
    ctx.rotate(obj.rotation * Math.PI / 180);
    ctx.scale(obj.scale, obj.scale);
    ctx.translate(-cx, -cy);

    ctx.fillStyle = obj.color || '#000';
    ctx.strokeStyle = obj.color || '#000';

    if (obj.type === 'rect' || obj.type === 'bar') {
        // Rounded corners for bars/rects
        roundRect(ctx, obj.x, obj.y, obj.width, obj.height, 4);
        ctx.fill();

        if (obj.text) {
            ctx.shadowBlur = 0; // No shadow for text inside
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 16px Inter';
            ctx.textAlign = 'center';
            ctx.fillText(obj.text, obj.x + obj.width / 2, obj.y + obj.height - 10);
        }
    }
    else if (obj.type === 'circle') {
        ctx.beginPath();
        ctx.arc(obj.x, obj.y, obj.r, 0, Math.PI * 2);
        ctx.fill();
    }
    else if (obj.type === 'sphere') {
        // Enhanced 3D Sphere
        const grad = ctx.createRadialGradient(
            obj.x - obj.r / 3, obj.y - obj.r / 3, obj.r / 10,
            obj.x, obj.y, obj.r
        );
        grad.addColorStop(0, obj.color2 || '#fff');
        grad.addColorStop(1, obj.color || '#000');

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(obj.x, obj.y, obj.r, 0, Math.PI * 2);
        ctx.fill();
    }
    else if (obj.type === 'text') {
        ctx.shadowBlur = 0;
        ctx.font = obj.font || '16px Inter';
        ctx.fillText(obj.text, obj.x, obj.y);
    }
    else if (obj.type === 'path') {
        const p = new Path2D(obj.d);
        ctx.lineWidth = obj.width || 2;
        ctx.stroke(p);
    }
    else if (obj.type === 'arrow') {
        let x1 = obj.points[0];
        let y1 = obj.points[1];
        let x2 = obj.points[2];
        let y2 = obj.points[3];

        const offsetX = obj.x - x1;
        const offsetY = obj.y - y1;

        x1 += offsetX;
        y1 += offsetY;
        x2 += offsetX;
        y2 += offsetY;

        const headlen = 12;
        const angle = Math.atan2(y2 - y1, x2 - x1);

        ctx.lineWidth = obj.width || 3;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.lineTo(x2 - headlen * Math.cos(angle - Math.PI / 6), y2 - headlen * Math.sin(angle - Math.PI / 6));
        ctx.moveTo(x2, y2);
        ctx.lineTo(x2 - headlen * Math.cos(angle + Math.PI / 6), y2 - headlen * Math.sin(angle + Math.PI / 6));
        ctx.stroke();
    }
    else if (obj.type === 'axis') {
        ctx.shadowBlur = 0;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(obj.x, obj.y);
        ctx.lineTo(obj.x + obj.width, obj.y);
        ctx.moveTo(obj.x, obj.y);
        ctx.lineTo(obj.x, obj.y - obj.height);
        ctx.stroke();
    }
    else if (obj.type === 'image') {
        // Check if image is loaded in the persistent scene object
        const persistentObj = scene.objects.find(o => o.id === obj.id);
        if (persistentObj) {
            if (!persistentObj._img) {
                persistentObj._img = new Image();
                persistentObj._img.src = obj.src;
            }
            if (persistentObj._img.complete) {
                ctx.drawImage(persistentObj._img, obj.x, obj.y, obj.width, obj.height);
            }
        }
    }

    ctx.restore();
}

function roundRect(ctx, x, y, w, h, r) {
    if (w < 2 * r) r = w / 2;
    if (h < 2 * r) r = h / 2;
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
}

// --- EXPORT ---
function handleExport() {
    if (!scene) return;

    exportBtn.disabled = true;
    exportBtn.textContent = 'Recording...';

    const stream = canvas.captureStream(30);
    mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
    recordedChunks = [];

    mediaRecorder.ondataavailable = e => {
        if (e.data.size > 0) recordedChunks.push(e.data);
    };

    mediaRecorder.onstop = () => {
        const blob = new Blob(recordedChunks, { type: 'video/webm' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${scene.sceneId}.webm`;
        a.click();

        exportBtn.disabled = false;
        exportBtn.textContent = 'Export Video';
        isPlaying = false;
    };

    mediaRecorder.start();
    resetPlayback();
    play();

    setTimeout(() => {
        mediaRecorder.stop();
        pause();
    }, scene.duration * 1000 + 500);
}

// --- UTILS ---
function showLoader(show) {
    if (show) loadingOverlay.classList.remove('hidden');
    else loadingOverlay.classList.add('hidden');
}

function showError(msg) {
    errorMessage.textContent = msg;
    errorToast.classList.remove('hidden');
    setTimeout(() => errorToast.classList.add('hidden'), 5000);
}

// Start
init();
