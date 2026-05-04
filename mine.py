import os
from flask import Flask, render_template_string, jsonify
from mcstatus import JavaServer

app = Flask(__name__)

# Твой сервер
SERVER_HOST = "burmalcraft.sosal.today"

@app.route('/api/players')
def api_players():
    try:
        server = JavaServer.lookup(SERVER_HOST)
        status = server.status()
        return jsonify({
            "online": status.players.online,
            "max": 50,
            "status": "online",
            "version": status.version.name
        })
    except Exception:
        return jsonify({
            "online": 0,
            "max": 50,
            "status": "offline",
            "version": "—"
        })

HTML = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BurmalCraft | Мониторинг</title>
    
    <link rel="icon" type="image/png" href="https://cdn.discordapp.com/attachments/1209502089210757141/1500758633301151744/content.png?ex=69f999e4&is=69f84864&hm=d14f95bc8d53d659f1f801649fd1fa89c8e38179a6b1cec382823c8b5192d311&">
    
    <style>
        :root {
            --sky-top: #1a1a2e;
            --sky-mid: #16213e;
            --sky-bottom: #0f3460;
            --gold: #fccf31;
            --sunset: #f62e46;
        }

        body {
            /* Тот самый глубокий закатный градиент */
            background: linear-gradient(180deg, #020111 0%, #191621 35%, #20202c 50%, #4a304d 70%, #ffedbc 100%);
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        .container {
            text-align: center;
            z-index: 10;
            animation: fadeIn 1.5s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .card {
            background: rgba(0, 0, 0, 0.5);
            padding: 3rem;
            border-radius: 30px;
            border: 2px solid var(--gold);
            backdrop-filter: blur(15px);
            box-shadow: 0 0 50px rgba(246, 46, 70, 0.3);
            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: scale(1.02);
        }

        h1 {
            font-size: 3.5rem;
            margin: 0;
            background: linear-gradient(to bottom, var(--gold), #f39c12);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-transform: uppercase;
            letter-spacing: 5px;
            filter: drop-shadow(0 0 10px rgba(252, 207, 49, 0.5));
        }

        .status-box {
            margin-top: 20px;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }

        .online-count {
            font-weight: bold;
            color: #2ecc71;
            text-shadow: 0 0 10px rgba(46, 204, 113, 0.5);
        }

        .pulse-dot {
            width: 12px;
            height: 12px;
            background: #2ecc71;
            border-radius: 50%;
            box-shadow: 0 0 10px #2ecc71;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.5); opacity: 0.5; }
            100% { transform: scale(1); opacity: 1; }
        }

        .ip-badge {
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 20px;
            border-radius: 50px;
            display: inline-block;
            margin-top: 25px;
            cursor: pointer;
            border: 1px solid rgba(252, 207, 49, 0.3);
            transition: all 0.3s;
        }

        .ip-badge:hover {
            background: var(--gold);
            color: black;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>BurmalCraft</h1>
            <div class="status-box">
                <div class="pulse-dot"></div>
                <span>Игроков на сервере: <span class="online-count" id="count">...</span></span>
            </div>
            <div class="ip-badge" onclick="copyIP()">
                IP: <span id="ip-text">burmalcraft.sosal.today</span>
            </div>
            <p style="margin-top: 15px; color: #ccc; font-size: 0.9rem;">Версия: <span id="ver">загрузка...</span></p>
        </div>
    </div>

    <script>
        async function updateStats() {
            try {
                const res = await fetch('/api/players');
                const data = await res.json();
                document.getElementById('count').innerText = data.online + ' / ' + data.max;
                document.getElementById('ver').innerText = data.version;
            } catch {
                document.getElementById('count').innerText = "OFFLINE";
            }
        }

        function copyIP() {
            const ip = document.getElementById('ip-text').innerText;
            navigator.clipboard.writeText(ip);
            alert('IP скопирован!');
        }

        setInterval(updateStats, 5000);
        updateStats();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
