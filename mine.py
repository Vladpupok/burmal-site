import os
from flask import Flask, render_template_string, jsonify
from mcstatus import JavaServer

app = Flask(__name__)

SERVER_HOST = "burmalcraft.sosal.today"

@app.route('/api/players')
def api_players():
    try:
        server = JavaServer.lookup(SERVER_HOST)
        status = server.status()
        return jsonify({"online": status.players.online, "max": 50, "status": "online", "version": status.version.name})
    except Exception:
        return jsonify({"online": 0, "max": 50, "status": "offline", "version": "—"})

# ОБНОВЛЕННЫЙ АДАПТИВНЫЙ ДИЗАЙН
HTML = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BurmalCraft | Закат на сервере</title>
    <link rel="icon" type="image/png" href="https://cdn.discordapp.com/attachments/1209502089210757141/1500758633301151744/content.png?ex=69f999e4&is=69f84864&hm=d14f95bc8d53d659f1f801649fd1fa89c8e38179a6b1cec382823c8b5192d311&">

    <style>
        :root {
            --sky-top: #151530;
            --sky-mid: #ff5e3a;
            --sky-bottom: #fccb90;
            --card-bg: rgba(20, 10, 30, 0.85);
            --mc-gold: #ffdf91;
            --mc-dirt: #3d2919;
            --mc-green: #2d5a27;
        }

        * {
            box-sizing: border-box;
        }

        body {
            background: linear-gradient(180deg, var(--sky-top) 0%, var(--sky-mid) 60%, var(--sky-bottom) 100%);
            color: white;
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
        }

        .sun {
            position: absolute;
            width: 80px;
            height: 80px;
            background: #fff;
            bottom: 20%;
            left: 10%;
            border-radius: 50%;
            box-shadow: 0 0 50px var(--sky-mid), 0 0 100px #fff;
            animation: sunPulse 4s infinite alternate ease-in-out;
            z-index: 1;
        }

        @keyframes sunPulse {
            from { transform: scale(1); opacity: 0.8; }
            to { transform: scale(1.1); opacity: 1; }
        }

        .cloud {
            position: absolute;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 50px;
            animation: moveClouds 45s infinite linear;
        }
        .c1 { width: 150px; height: 30px; top: 10%; }
        .c2 { width: 100px; height: 20px; top: 25%; animation-duration: 60s; animation-delay: -10s; }

        @keyframes moveClouds {
            from { left: -200px; }
            to { left: 110vw; }
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            padding: 40px 20px;
            border: 3px solid var(--mc-gold);
            border-radius: 12px;
            text-align: center;
            width: 90%;
            max-width: 420px;
            z-index: 10;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            animation: blockSpawn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            margin: 20px auto;
        }

        @keyframes blockSpawn {
            0% { transform: scale(0.8) translateY(50px); opacity: 0; }
            100% { transform: scale(1) translateY(0); opacity: 1; }
        }

        h1 {
            font-size: clamp(28px, 8vw, 42px);
            margin: 0;
            color: var(--mc-gold);
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 2px 2px 0px #000;
        }

        .tagline { 
            font-size: 14px; 
            color: rgba(255,255,255,0.7); 
            margin: 10px 0 20px; 
            min-height: 20px; 
            font-style: italic; 
        }

        .online-status {
            color: #55ff55;
            font-family: monospace;
            font-size: 16px;
            margin: 10px 0 25px;
            text-shadow: 0 0 10px rgba(85, 255, 85, 0.4);
            animation: blink 2s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .ip-box {
            background: rgba(0,0,0,0.4);
            border: 2px dashed var(--mc-gold);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 25px;
            cursor: pointer;
            transition: 0.2s;
        }

        .ip-box:active { transform: scale(0.97); }

        .ip-text {
            font-size: 18px;
            font-weight: bold;
            word-break: break-all;
        }

        .btn {
            display: block;
            padding: 15px;
            text-decoration: none;
            font-weight: bold;
            border-radius: 6px;
            text-transform: uppercase;
            transition: 0.2s;
            margin-bottom: 12px;
            border-bottom: 4px solid rgba(0,0,0,0.3);
            font-size: 14px;
        }

        .btn-play { background: var(--mc-gold); color: #3d2919; }
        .btn-discord { background: #5865F2; color: white; border-bottom-color: #3b44a3; }
        .btn-donate { background: #ff4d4d; color: white; border-bottom-color: #b33030; }

        .btn:hover { transform: translateY(-2px); filter: brightness(1.1); }

        .footer { margin-top: 25px; font-size: 10px; color: #bbb; letter-spacing: 1px; }

        /* Игровой автомат */
        .slot-wrap {
            background: linear-gradient(145deg, #1a0a00, #2d1500);
            border: 2px solid var(--mc-gold);
            border-radius: 14px;
            padding: 14px 16px 12px;
            margin-bottom: 14px;
            box-shadow: 0 0 20px rgba(255,200,0,0.15), inset 0 0 30px rgba(0,0,0,0.5);
            position: relative;
        }
        .slot-label {
            font-size: 9px;
            letter-spacing: 2px;
            color: var(--mc-gold);
            text-align: center;
            margin-bottom: 8px;
            opacity: 0.7;
            text-transform: uppercase;
        }
        .slot-machine { display: flex; justify-content: center; align-items: center; gap: 6px; margin-bottom: 10px; }
        .slot-reel {
            width: 58px; height: 58px;
            background: #000;
            border: 2px solid #555;
            border-radius: 8px;
            overflow: hidden;
            position: relative;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.8), 0 0 8px rgba(255,200,0,0.1);
        }
        .slot-reel::before, .slot-reel::after {
            content: '';
            position: absolute;
            left: 0; right: 0;
            height: 14px;
            z-index: 2;
            pointer-events: none;
        }
        .slot-reel::before { top: 0; background: linear-gradient(to bottom, #000, transparent); }
        .slot-reel::after  { bottom: 0; background: linear-gradient(to top, #000, transparent); }
        .slot-inner { display: flex; flex-direction: column; align-items: center; }
        .slot-symbol { width: 58px; height: 58px; display: flex; align-items: center; justify-content: center; font-size: 26px; flex-shrink: 0; }
        .slot-controls { display: flex; align-items: center; justify-content: center; gap: 10px; }
        .slot-btn {
            background: linear-gradient(145deg, var(--mc-gold), #c8960a);
            color: #1a0800;
            border: none;
            border-radius: 8px;
            padding: 9px 22px;
            font-weight: bold;
            font-size: 15px;
            cursor: pointer;
            border-bottom: 3px solid #7a5500;
            letter-spacing: 1px;
            transition: 0.15s;
            box-shadow: 0 4px 12px rgba(255,180,0,0.3);
        }
        .slot-btn:hover { filter: brightness(1.15); transform: translateY(-1px); }
        .slot-btn:active { transform: translateY(1px); border-bottom-width: 1px; }
        .slot-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .slot-result {
            font-size: 11px;
            font-family: monospace;
            text-align: center;
            min-height: 14px;
            color: #aaa;
            margin-top: 4px;
        }
        /* Видео-оверлей */
        .win-overlay {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.85);
            z-index: 999;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }
        .win-overlay.show { display: flex; animation: fadeIn 0.3s ease; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .win-overlay video {
            max-width: 90vw;
            max-height: 70vh;
            border-radius: 12px;
            border: 3px solid var(--mc-gold);
            box-shadow: 0 0 40px rgba(255,200,0,0.4);
        }
        .win-overlay-title {
            color: var(--mc-gold);
            font-size: 26px;
            font-weight: bold;
            text-shadow: 0 0 20px #ffdf91;
            margin-bottom: 16px;
            letter-spacing: 3px;
            animation: pulse 0.6s infinite alternate;
        }
        @keyframes pulse { from { transform: scale(1); } to { transform: scale(1.06); } }
        .win-close {
            margin-top: 16px;
            background: var(--mc-gold);
            color: #1a0800;
            border: none;
            border-radius: 8px;
            padding: 10px 30px;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
        }

        #particles { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }

        /* Мобильные правки */
        @media (max-width: 480px) {
            .card { padding: 30px 15px; }
            .sun { width: 60px; height: 60px; left: 5%; bottom: 15%; }
            .btn { padding: 12px; font-size: 13px; }
        }
    </style>
</head>
<body>

    <canvas id="particles"></canvas>
    <div class="sun"></div>
    <div class="cloud c1"></div>
    <div class="cloud c2"></div>

    <div class="card">
        <h1>BURMALCRAFT</h1>
        <div class="tagline"><span id="tagline-text"></span><span class="cursor"></span></div>
        <div class="online-status" id="player-count">● Подключение...</div>

        <div class="ip-box" onclick="copyIP()">
            <div style="font-size: 9px; color: var(--mc-gold); margin-bottom: 5px; opacity: 0.8;">НАЖМИ, ЧТОБЫ СКОПИРОВАТЬ IP</div>
            <div class="ip-text" id="ip">burmalcraft.sosal.today</div>
        </div>

        <div class="slot-wrap">
            <div class="slot-label">🎰 испытай удачу</div>
            <input type="text" id="nickname-input" placeholder="Введи свой ник..." maxlength="32"
                style="width:100%;box-sizing:border-box;background:#1a1008;border:2px solid #5a3a00;border-radius:8px;
                color:#ffdf91;font-size:14px;padding:10px 14px;margin-bottom:10px;outline:none;
                font-family:inherit;letter-spacing:0.5px;" />
            <div class="slot-machine">
                <div class="slot-reel"><div class="slot-inner" id="i0"></div></div>
                <div class="slot-reel"><div class="slot-inner" id="i1"></div></div>
                <div class="slot-reel"><div class="slot-inner" id="i2"></div></div>
            </div>
            <div id="chance-bar-wrap" style="width:100%;margin-top:8px;">
                <div style="font-size:10px;color:#888;text-align:right;margin-bottom:2px;">шанс джекпота: <span id="chance-label">5%</span></div>
                <div style="background:#1a1008;border-radius:4px;height:6px;overflow:hidden;border:1px solid #3a2200;">
                    <div id="chance-bar" style="height:100%;width:5%;background:linear-gradient(90deg,#ff9900,#ffdf91);border-radius:4px;transition:width 0.5s;"></div>
                </div>
            </div>
            <div class="slot-controls">
                <button class="slot-btn" id="slot-btn" onclick="spinSlot()">▶ КРУТИТЬ</button>
            </div>
            <div class="slot-result" id="slot-win"></div>
        </div>

        <!-- Видео оверлей на выигрыш -->
        <div class="win-overlay" id="win-overlay" onclick="closeWin()">
            <div class="win-overlay-title">🎉 ДЖЕКПОТ! 🎉</div>
            <video id="win-video" src="https://cdn.discordapp.com/attachments/1209502089210757141/1500758354874597436/VID_20260504_101735_866.mp4?ex=69f999a2&is=69f84822&hm=3bc5c25faa95c7804863166734334c44b5eaf2c239ed5afe2cd6850ae2503d96&" autoplay playsinline></video>
            <button class="win-close">✕ Закрыть</button>
        </div>

        <a href="https://discord.gg/FePmE3pQZ" target="_blank" class="btn btn-discord">Наш Discord</a>
        <a href="https://destream.net/live/zemaks999" target="_blank" class="btn btn-donate">❤ Задонатить</a>

        <div class="footer">VERSION <span id="server-version">...</span> | BURMALCRAFT 2024</div>
    </div>

    <script>
        // Скрипты остаются без изменений, так как они логически верны
        const symbols = ['⚔️','💎','🏆','🌟','🍀','💀','🔥','🎯'];
        const reels = [0,1,2].map(i => document.getElementById('i'+i));
        let spinning = false;
        let jackpotChance = 0.05;
        const WEBHOOK = 'https://discord.com/api/webhooks/1500775192425664512/ooLkNMiJOlvNlgjWgx3JrR3-akcEV5fcBfVbZERbyCMaQ2ee0bHVvTzHvWY4mEKfoYl3';

        function updateChanceBar() {
            const pct = Math.round(jackpotChance * 100);
            document.getElementById('chance-label').textContent = pct + '%';
            document.getElementById('chance-bar').style.width = Math.min(pct, 100) + '%';
            const bar = document.getElementById('chance-bar');
            if (pct >= 60) bar.style.background = 'linear-gradient(90deg,#ff4400,#ffaa00)';
            else if (pct >= 30) bar.style.background = 'linear-gradient(90deg,#ff9900,#ffdf91)';
            else bar.style.background = 'linear-gradient(90deg,#ff9900,#ffdf91)';
        }

        async function sendWinWebhook(nick) {
            const name = nick.trim() || 'Аноним';
            const payload = {
                embeds: [{
                    title: '🎰 ДЖЕКПОТ НА BURMALCRAFT! 🎉',
                    description: `**${name}** сорвал джекпот в слот-машине!\n\n🏆 Все три символа совпали!\n\nЗаходи: \`burmalcraft.sosal.today\``,
                    color: 0xFFD700,
                    footer: { text: 'BurmalCraft Casino' },
                    timestamp: new Date().toISOString()
                }]
            };
            try {
                await fetch(WEBHOOK, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
            } catch(e) {}
        }

        function buildReel(el) {
            el.innerHTML = '';
            const extended = [...symbols, ...symbols, ...symbols];
            extended.forEach(s => {
                const div = document.createElement('div');
                div.className = 'slot-symbol';
                div.textContent = s;
                el.appendChild(div);
            });
            el.style.transform = 'translateY(0px)';
        }
        reels.forEach(buildReel);

        function spinReel(el, delay, finalIdx) {
            return new Promise(resolve => {
                const symHeight = 58;
                const totalSyms = symbols.length;
                const spins = 3;
                const target = -(spins * totalSyms * symHeight + finalIdx * symHeight);
                let pos = 0;
                const speed = 14;

                setTimeout(() => {
                    function animate() {
                        pos -= speed;
                        if (pos <= target) {
                            el.style.transform = `translateY(${-Math.abs(finalIdx * symHeight)}px)`;
                            resolve(finalIdx);
                            return;
                        }
                        el.style.transform = `translateY(${pos}px)`;
                        requestAnimationFrame(animate);
                    }
                    requestAnimationFrame(animate);
                }, delay);
            });
        }

        async function spinSlot() {
            if (spinning) return;
            spinning = true;
            const btn = document.getElementById('slot-btn');
            btn.disabled = true;
            document.getElementById('slot-win').textContent = '';

            const isJackpot = Math.random() < jackpotChance;
            const jackpotIdx = Math.floor(Math.random() * symbols.length);
            let picks;
            if (isJackpot) {
                picks = [jackpotIdx, jackpotIdx, jackpotIdx];
            } else {
                do {
                    picks = [0,1,2].map(() => Math.floor(Math.random() * symbols.length));
                } while (picks[0] === picks[1] && picks[1] === picks[2]);
            }

            await Promise.all([
                spinReel(reels[0], 0,   picks[0]),
                spinReel(reels[1], 220, picks[1]),
                spinReel(reels[2], 440, picks[2]),
            ]);

            const winEl = document.getElementById('slot-win');
            if (isJackpot) {
                winEl.textContent = '🎉 ДЖЕКПОТ! ВСЕ СОВПАЛИ!';
                winEl.style.color = '#ffdf91';
                jackpotChance = 0.05;
                updateChanceBar();
                const nick = document.getElementById('nickname-input').value;
                sendWinWebhook(nick);
                setTimeout(showWinVideo, 400);
            } else if (picks[0] === picks[1] || picks[1] === picks[2] || picks[0] === picks[2]) {
                winEl.textContent = '✨ Два совпали! Почти!';
                winEl.style.color = '#55ff55';
                jackpotChance = Math.min(jackpotChance + 0.07, 0.95);
                updateChanceBar();
            } else {
                winEl.textContent = 'Не повезло, крути ещё!';
                winEl.style.color = '#888';
                jackpotChance = Math.min(jackpotChance + 0.05, 0.95);
                updateChanceBar();
            }
            spinning = false;
            btn.disabled = false;
        }

        function showWinVideo() {
            const overlay = document.getElementById('win-overlay');
            const video = document.getElementById('win-video');
            overlay.classList.add('show');
            video.currentTime = 0;
            video.play();
        }

        function closeWin() {
            const overlay = document.getElementById('win-overlay');
            const video = document.getElementById('win-video');
            overlay.classList.remove('show');
            video.pause();
        }

        // Частицы
        const canvas = document.getElementById('particles');
        const ctx = canvas.getContext('2d');
        function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        window.addEventListener('resize', resize);
        resize();

        const particles = Array.from({length: 25}, () => ({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 4 + 2,
            speedY: -Math.random() * 0.5 - 0.2,
            opacity: Math.random() * 0.5
        }));

        function draw() {
            ctx.clearRect(0,0,canvas.width, canvas.height);
            particles.forEach(p => {
                ctx.fillStyle = `rgba(255, 223, 145, ${p.opacity})`;
                ctx.fillRect(p.x, p.y, p.size, p.size);
                p.y += p.speedY;
                if (p.y < -10) p.y = canvas.height + 10;
            });
            requestAnimationFrame(draw);
        }
        draw();

        // Текст
        const taglines = ['Лучший сервер для друзей', 'Строй. Сражайся. Побеждай.', 'Присоединяйся к нам!'];
        let tIdx = 0, cIdx = 0, del = false;
        function type() {
            const full = taglines[tIdx];
            document.getElementById('tagline-text').textContent = full.slice(0, cIdx);
            if (!del && cIdx < full.length) cIdx++;
            else if (del && cIdx > 0) cIdx--;
            else { del = !del; if (!del) tIdx = (tIdx + 1) % taglines.length; }
            setTimeout(type, del ? 50 : 100);
        }
        type();

        // Статус
        async function update() {
            try {
                const res = await fetch('/api/players');
                const d = await res.json();
                const el = document.getElementById('player-count');
                document.getElementById('server-version').textContent = d.version;
                if (d.status === 'online') {
                    el.textContent = '● Игроков на сервере: ' + d.online + ' / ' + d.max;
                    el.style.color = '#55ff55';
                } else {
                    el.textContent = '● Сервер Offline';
                    el.style.color = '#ff5555';
                }
            } catch (e) {}
        }
        update();
        setInterval(update, 30000);

        function copyIP() {
            const ip = document.getElementById('ip');
            navigator.clipboard.writeText(ip.innerText);
            const old = ip.innerText;
            ip.innerText = "СКОПИРОВАНО!";
            setTimeout(() => ip.innerText = old, 1500);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
