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

HTML = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BurmalCraft | Slots Edition</title>
    <link rel="icon" type="image/png" href="https://cdn.discordapp.com/attachments/1209502089210757141/1500758633301151744/content.png">
    
    <style>
        :root {
            --sky-top: #151530;
            --sky-mid: #ff5e3a;
            --sky-bottom: #fccb90;
            --card-bg: rgba(20, 10, 30, 0.9);
            --mc-gold: #ffdf91;
            --mc-border: #5d4d2d;
            --jackpot-color: #00ffff;
        }

        * { box-sizing: border-box; }
        body {
            background: linear-gradient(180deg, var(--sky-top) 0%, var(--sky-mid) 60%, var(--sky-bottom) 100%);
            color: white;
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }

        /* КАРТОЧКА */
        .card {
            background: var(--card-bg);
            backdrop-filter: blur(15px);
            padding: 30px 20px;
            border: 4px solid var(--mc-gold);
            border-radius: 15px;
            text-align: center;
            width: 90%;
            max-width: 420px;
            z-index: 10;
            box-shadow: 0 0 30px rgba(255, 223, 145, 0.2);
            animation: blockSpawn 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        h1 { font-size: 32px; color: var(--mc-gold); text-shadow: 3px 3px 0 #000; margin: 0; }

        /* ДИЗАЙН СЛОТ-МАШИНЫ */
        .slot-machine-container {
            background: #1a0f00;
            border: 4px solid #3d2919;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            position: relative;
            box-shadow: inset 0 0 15px #000;
        }

        .slot-machine {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }

        .slot-reel {
            width: 60px;
            height: 60px;
            background: #2a1a0a;
            border: 3px solid var(--mc-gold);
            border-radius: 5px;
            overflow: hidden;
            position: relative;
            box-shadow: inset 0 0 10px #000;
        }

        .slot-inner { display: flex; flex-direction: column; align-items: center; }
        .slot-symbol { 
            width: 60px; height: 60px; 
            display: flex; align-items: center; justify-content: center; 
            font-size: 30px; flex-shrink: 0; 
        }

        .slot-btn {
            background: linear-gradient(to bottom, #ffdf91, #b38600);
            color: #3d2919;
            border: none;
            border-radius: 8px;
            padding: 12px 25px;
            font-weight: bold;
            font-size: 18px;
            cursor: pointer;
            border-bottom: 4px solid #664d00;
            transition: 0.1s;
            width: 100%;
        }

        .slot-btn:active { transform: translateY(2px); border-bottom-width: 2px; }
        .slot-btn:disabled { opacity: 0.5; cursor: not-allowed; }

        /* SUPER WIN OVERLAY */
        #super-win-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85);
            z-index: 100;
            display: none; /* Скрыт по умолчанию */
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            backdrop-filter: blur(10px);
        }

        .win-video {
            width: 90%;
            max-width: 600px;
            border: 5px solid var(--mc-gold);
            box-shadow: 0 0 50px var(--mc-gold);
            border-radius: 10px;
        }

        .win-text {
            font-size: 50px;
            color: var(--mc-gold);
            text-transform: uppercase;
            margin-top: 20px;
            font-weight: bold;
            text-shadow: 0 0 20px #ffdf91;
            animation: pulse 1s infinite;
        }

        .close-win-btn {
            margin-top: 30px;
            padding: 10px 30px;
            background: white;
            color: black;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }

        @keyframes blockSpawn {
            0% { transform: scale(0.5); opacity: 0; }
            100% { transform: scale(1); opacity: 1; }
        }

        .btn {
            display: block; padding: 15px; margin-top: 10px;
            text-decoration: none; border-radius: 5px; font-weight: bold;
            text-transform: uppercase; color: white;
            background: #5865F2; border-bottom: 4px solid #3b44a3;
        }
    </style>
</head>
<body>

    <div id="super-win-overlay">
        <img class="win-video" src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJmZGRmZ3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4Z3R4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l41lTjJpfSQIbCc9y/giphy.gif" alt="Winner!">
        <div class="win-text">SUPER JACKPOT!</div>
        <button class="close-win-btn" onclick="closeWin()">ЗАБРАТЬ ПРИЗ</button>
    </div>

    <div class="card">
        <h1>BURMALCRAFT</h1>
        <div id="player-count" style="margin: 10px 0; color: #55ff55; font-family: monospace;">● Загрузка...</div>

        <div class="slot-machine-container">
            <div class="slot-machine">
                <div class="slot-reel" id="r0"><div class="slot-inner" id="i0"></div></div>
                <div class="slot-reel" id="r1"><div class="slot-inner" id="i1"></div></div>
                <div class="slot-reel" id="r2"><div class="slot-inner" id="i2"></div></div>
            </div>
            <button class="slot-btn" id="spin-btn" onclick="spinSlot()">КРУТИТЬ</button>
        </div>

        <div id="slot-status" style="min-height: 20px; font-size: 14px; margin-bottom: 10px;"></div>

        <a href="https://discord.gg/FePmE3pQZ" target="_blank" class="btn">DISCORD СЕРВЕРА</a>
    </div>

    <script>
        const symbols = ['💎','⚔️','🍎','🔥','💀','🌟','🍀'];
        const reels = [0,1,2].map(i => document.getElementById('i'+i));
        const spinBtn = document.getElementById('spin-btn');
        let spinning = false;

        function buildReel(el) {
            el.innerHTML = '';
            // Создаем длинную ленту символов
            const extended = [];
            for(let i=0; i<40; i++) extended.push(symbols[Math.floor(Math.random()*symbols.length)]);
            extended.forEach(s => {
                const div = document.createElement('div');
                div.className = 'slot-symbol';
                div.textContent = s;
                el.appendChild(div);
            });
            el.style.transform = 'translateY(0px)';
        }
        reels.forEach(buildReel);

        async function spinSlot() {
            if (spinning) return;
            spinning = true;
            spinBtn.disabled = true;
            document.getElementById('slot-status').textContent = "Испытываем удачу...";

            const picks = [0,1,2].map(() => Math.floor(Math.random() * symbols.length));
            
            // Анимация кручения
            const promises = reels.map((el, i) => {
                return new Promise(resolve => {
                    const time = 2000 + (i * 500);
                    const targetY = -(30 * 60); // прокрутить 30 символов
                    el.style.transition = `transform ${time}ms cubic-bezier(0.45, 0.05, 0.55, 0.95)`;
                    el.style.transform = `translateY(${targetY}px)`;
                    
                    setTimeout(() => {
                        el.style.transition = 'none';
                        el.innerHTML = '';
                        // Ставим выигрышный символ в центр
                        const winSym = symbols[picks[i]];
                        const div = document.createElement('div');
                        div.className = 'slot-symbol';
                        div.textContent = winSym;
                        el.appendChild(div);
                        el.style.transform = 'translateY(0px)';
                        resolve(winSym);
                    }, time);
                });
            });

            const results = await Promise.all(promises);

            // ПРОВЕРКА ПОБЕДЫ
            if (results[0] === results[1] && results[1] === results[2]) {
                showSuperWin();
            } else if (results[0] === results[1] || results[1] === results[2] || results[0] === results[2]) {
                document.getElementById('slot-status').textContent = "✨ Малая победа!";
                document.getElementById('slot-status').style.color = "#55ff55";
            } else {
                document.getElementById('slot-status').textContent = "Попробуй еще раз!";
                document.getElementById('slot-status').style.color = "#aaa";
            }

            spinning = false;
            spinBtn.disabled = false;
            setTimeout(() => buildReel(reels[0]), 2000); // Сброс лент
            reels.forEach(buildReel);
        }

        function showSuperWin() {
            const overlay = document.getElementById('super-win-overlay');
            overlay.style.display = 'flex';
            // Если есть видео, можно запустить: document.querySelector('.win-video').play();
        }

        function closeWin() {
            document.getElementById('super-win-overlay').style.display = 'none';
        }

        // Обновление онлайна
        async function fetchStatus() {
            try {
                const res = await fetch('/api/players');
                const data = await res.json();
                document.getElementById('player-count').textContent = `● Игроков: ${data.online} / ${data.max}`;
            } catch(e) {}
        }
        setInterval(fetchStatus, 15000);
        fetchStatus();
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
