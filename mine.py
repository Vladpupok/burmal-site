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

# ТВОЙ ПОЛНЫЙ ДИЗАЙН БЕЗ ИЗМЕНЕНИЙ
HTML = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BurmalCraft | Закат на сервере</title>
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

        body {
            background: linear-gradient(180deg, var(--sky-top) 0%, var(--sky-mid) 60%, var(--sky-bottom) 100%);
            color: white;
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
            position: relative;
        }

        .sun {
            position: absolute;
            width: 90px;
            height: 90px;
            background: #fff;
            bottom: 25%;
            left: 15%;
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
            background: rgba(255, 255, 255, 0.2);
            animation: moveClouds 45s infinite linear;
        }
        .c1 { width: 180px; height: 35px; top: 15%; }
        .c2 { width: 120px; height: 25px; top: 35%; animation-duration: 60s; animation-delay: -10s; }

        @keyframes moveClouds {
            from { left: -200px; }
            to { left: 110vw; }
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            padding: 50px;
            border: 3px solid var(--mc-gold);
            border-radius: 10px;
            text-align: center;
            width: 400px;
            z-index: 10;
            box-shadow: 0 25px 50px rgba(0,0,0,0.6);
            animation: blockSpawn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        @keyframes blockSpawn {
            0% { transform: scale(0.5) translateY(100px); opacity: 0; }
            100% { transform: scale(1) translateY(0); opacity: 1; }
        }

        h1 {
            font-size: 42px;
            margin: 0;
            color: var(--mc-gold);
            text-transform: uppercase;
            letter-spacing: 4px;
            text-shadow: 3px 3px 0px #000;
        }

        .online-status {
            color: #55ff55;
            font-family: monospace;
            font-size: 18px;
            margin: 15px 0 30px;
            text-shadow: 0 0 10px rgba(85, 255, 85, 0.5);
            animation: blink 2s infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .ip-box {
            background: rgba(0,0,0,0.5);
            border: 2px dashed var(--mc-gold);
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
            cursor: pointer;
            transition: 0.3s;
        }

        .ip-box:hover {
            background: rgba(255, 223, 145, 0.1);
            transform: scale(1.03);
        }

        .ip-text {
            font-size: 22px;
            font-weight: bold;
            letter-spacing: 1px;
        }

        .btn {
            display: block;
            padding: 18px;
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
            text-transform: uppercase;
            transition: 0.3s;
            margin-bottom: 15px;
            border-bottom: 4px solid rgba(0,0,0,0.3);
        }

        .btn-play { background: var(--mc-gold); color: #3d2919; }
        .btn-play:hover { background: #fff; transform: translateY(-3px); }
        .btn-discord { background: #5865F2; color: white; border-bottom-color: #3b44a3; }
        .btn-discord:hover { background: #7289da; transform: translateY(-2px); }
        .btn-donate { background: #ff4d4d; color: white; border-bottom-color: #b33030; }
        .btn-donate:hover { background: #ff6666; transform: translateY(-2px); }

        .footer { margin-top: 30px; font-size: 12px; color: #aaa; letter-spacing: 1px; }

        .slot-machine { display: flex; justify-content: center; align-items: center; gap: 6px; margin-bottom: 18px; }
        .slot-reel { width: 44px; height: 44px; background: rgba(0,0,0,0.5); border: 2px solid var(--mc-gold); border-radius: 6px; overflow: hidden; position: relative; }
        .slot-inner { display: flex; flex-direction: column; align-items: center; transition: transform 0.1s linear; will-change: transform; }
        .slot-symbol { width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0; }
        .slot-btn { background: var(--mc-gold); color: #3d2919; border: none; border-radius: 6px; padding: 6px 12px; font-weight: bold; font-size: 13px; cursor: pointer; border-bottom: 3px solid #b38600; transition: 0.15s; }
        .slot-btn:hover { background: #fff; transform: translateY(-1px); }
        .slot-btn:active { transform: translateY(1px); border-bottom-width: 1px; }
        .slot-win { font-size: 11px; color: #55ff55; min-height: 16px; margin-top: -12px; margin-bottom: 8px; text-align: center; font-family: monospace; }

        .tagline { font-size: 14px; color: rgba(255,255,255,0.6); margin: 8px 0 20px; min-height: 20px; font-style: italic; }
        .cursor { display: inline-block; width: 2px; background: rgba(255,255,255,0.6); animation: blink-cursor 0.7s infinite; vertical-align: middle; height: 14px; margin-left: 2px; }
        @keyframes blink-cursor { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

        #particles { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; }
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
            <div style="font-size: 10px; color: var(--mc-gold); margin-bottom: 5px;">НАЖМИ, ЧТОБЫ СКОПИРОВАТЬ IP</div>
            <div class="ip-text" id="ip">burmalcraft.sosal.today</div>
        </div>

        <div class="slot-machine">
            <div class="slot-reel" id="r0"><div class="slot-inner" id="i0"></div></div>
            <div class="slot-reel" id="r1"><div class="slot-inner" id="i1"></div></div>
            <div class="slot-reel" id="r2"><div class="slot-inner" id="i2"></div></div>
            <button class="slot-btn" onclick="spinSlot()">▶</button>
        </div>
        <div class="slot-win" id="slot-win"></div>

        <a href="https://discord.gg/FePmE3pQZ" target="_blank" class="btn btn-discord">Наш Discord</a>
        <a href="https://destream.net/live/zemaks999" target="_blank" class="btn btn-donate">❤ Задонатить</a>

        <div class="footer">VERSION <span id="server-version">...</span> | СДЕЛАНО ДЛЯ BURMALCRAFT</div>
    </div>

    <script>
        const symbols = ['⚔️','💎','🏆','🌟','🍀','💀','🔥','🎯'];
        const reels = [0,1,2].map(i => document.getElementById('i'+i));
        let spinning = false;

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
                const symHeight = 44;
                const totalSyms = symbols.length;
                const spins = 3;
                const target = -(spins * totalSyms * symHeight + finalIdx * symHeight);
                let pos = 0;
                const speed = 12;

                setTimeout(() => {
                    el.style.transition = 'none';
                    el.style.transform = 'translateY(0px)';
                    buildReel(el);
                    let frame;
                    function animate() {
                        pos -= speed;
                        if (pos <= target) {
                            pos = target % (totalSyms * symHeight) - symHeight * finalIdx;
                            el.style.transform = `translateY(${-Math.abs(finalIdx * symHeight)}px)`;
                            resolve(finalIdx);
                            return;
                        }
                        el.style.transform = `translateY(${pos}px)`;
                        frame = requestAnimationFrame(animate);
                    }
                    frame = requestAnimationFrame(animate);
                }, delay);
            });
        }

        async function spinSlot() {
            if (spinning) return;
            spinning = true;
            document.getElementById('slot-win').textContent = '';
            const picks = [0,1,2].map(() => Math.floor(Math.random() * symbols.length));
            await Promise.all([
                spinReel(reels[0], 0,   picks[0]),
                spinReel(reels[1], 200, picks[1]),
                spinReel(reels[2], 400, picks[2]),
            ]);
            const winEl = document.getElementById('slot-win');
            if (picks[0] === picks[1] && picks[1] === picks[2]) {
                winEl.textContent = '🎉 ДЖЕКПОТ! Все совпали!';
                winEl.style.color = '#ffdf91';
            } else if (picks[0] === picks[1] || picks[1] === picks[2] || picks[0] === picks[2]) {
                winEl.textContent = '✨ Два совпали!';
                winEl.style.color = '#55ff55';
            } else {
                winEl.textContent = 'Не повезло, крути ещё!';
                winEl.style.color = '#aaa';
            }
            spinning = false;
        }
        spinSlot();

        const canvas = document.getElementById('particles');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
        const colors = ['#ffdf91','#ff5e3a','#55ff55','#5865F2','#ffffff'];
        const particles = Array.from({length: 35}, () => ({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 6 + 3,
            color: colors[Math.floor(Math.random() * colors.length)],
            speedX: (Math.random() - 0.5) * 0.6,
            speedY: -Math.random() * 0.8 - 0.2,
            opacity: Math.random() * 0.5 + 0.1
        }));
        function drawParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => {
                ctx.globalAlpha = p.opacity;
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x, p.y, p.size, p.size);
                p.x += p.speedX;
                p.y += p.speedY;
                if (p.y < -10) { p.y = canvas.height + 10; p.x = Math.random() * canvas.width; }
            });
            ctx.globalAlpha = 1;
            requestAnimationFrame(drawParticles);
        }
        drawParticles();

        const taglines = [
            'Лучший сервер для друзей',
            'Строй. Сражайся. Побеждай.',
            'Присоединяйся к BurmalCraft!',
            'Новые приключения каждый день'
        ];
        let tagIdx = 0, charIdx = 0, deleting = false;
        const tagEl = document.getElementById('tagline-text');
        function typeTagline() {
            const current = taglines[tagIdx];
            if (!deleting) {
                tagEl.textContent = current.slice(0, ++charIdx);
                if (charIdx === current.length) { deleting = true; setTimeout(typeTagline, 1800); return; }
            } else {
                tagEl.textContent = current.slice(0, --charIdx);
                if (charIdx === 0) { deleting = false; tagIdx = (tagIdx + 1) % taglines.length; }
            }
            setTimeout(typeTagline, deleting ? 40 : 70);
        }
        typeTagline();

        async function fetchPlayers() {
            try {
                const res = await fetch('/api/players');
                const data = await res.json();
                const el = document.getElementById('player-count');
                document.getElementById('server-version').textContent = data.version || '—';
                if (data.status === 'online') {
                    el.textContent = '● Игроков на сервере: ' + data.online + ' / ' + data.max;
                    el.style.color = '#55ff55';
                } else {
                    el.textContent = '● Сервер недоступен';
                    el.style.color = '#ff5555';
                }
            } catch (e) {
                document.getElementById('player-count').textContent = '● Ошибка соединения';
            }
        }
        fetchPlayers();
        setInterval(fetchPlayers, 30000);

        function copyIP() {
            const ip = document.getElementById('ip');
            navigator.clipboard.writeText(ip.innerText);
            const original = ip.innerText;
            ip.innerText = "СКОПИРОВАНО!";
            ip.style.color = "#55ff55";
            setTimeout(() => {
                ip.innerText = original;
                ip.style.color = "white";
            }, 1200);
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    # Эта часть важна для Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
