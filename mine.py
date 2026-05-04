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
        .slot-machine { display: flex; justify-content: center; align-items: center; gap: 8px; margin-bottom: 15px; }
        .slot-reel { width: 44px; height: 44px; background: rgba(0,0,0,0.5); border: 2px solid var(--mc-gold); border-radius: 6px; overflow: hidden; position: relative; }
        .slot-inner { display: flex; flex-direction: column; align-items: center; }
        .slot-symbol { width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
        .slot-btn { background: var(--mc-gold); color: #3d2919; border: none; border-radius: 6px; padding: 10px 15px; font-weight: bold; cursor: pointer; border-bottom: 3px solid #b38600; }

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

        <div class="slot-machine">
            <div class="slot-reel" id="r0"><div class="slot-inner" id="i0"></div></div>
            <div class="slot-reel" id="r1"><div class="slot-inner" id="i1"></div></div>
            <div class="slot-reel" id="r2"><div class="slot-inner" id="i2"></div></div>
            <button class="slot-btn" onclick="spinSlot()">▶</button>
        </div>
        <div id="slot-win" style="font-size: 11px; margin-bottom: 15px; min-height: 15px; font-family: monospace;"></div>

        <a href="https://discord.gg/FePmE3pQZ" target="_blank" class="btn btn-discord">Наш Discord</a>
        <a href="https://destream.net/live/zemaks999" target="_blank" class="btn btn-donate">❤ Задонатить</a>

        <div class="footer">VERSION <span id="server-version">...</span> | BURMALCRAFT 2024</div>
    </div>

    <script>
        // Скрипты остаются без изменений, так как они логически верны
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
            document.getElementById('slot-win').textContent = '';
            const picks = [0,1,2].map(() => Math.floor(Math.random() * symbols.length));
            await Promise.all([
                spinReel(reels[0], 0,   picks[0]),
                spinReel(reels[1], 200, picks[1]),
                spinReel(reels[2], 400, picks[2]),
            ]);
            const winEl = document.getElementById('slot-win');
            if (picks[0] === picks[1] && picks[1] === picks[2]) {
                winEl.textContent = '🎉 ДЖЕКПОТ!';
                winEl.style.color = '#ffdf91';
            } else if (picks[0] === picks[1] || picks[1] === picks[2] || picks[0] === picks[2]) {
                winEl.textContent = '✨ Почти!';
                winEl.style.color = '#55ff55';
            }
            spinning = false;
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
