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
            --sky-bottom: #f62e46;
            --gold: #fccf31;
        }

        body {
            background: linear-gradient(180deg, #020111 0%, #191621 40%, #4a304d 100%);
            color: white;
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }

        .card {
            background: rgba(0, 0, 0, 0.6);
            padding: 2rem;
            border-radius: 20px;
            border: 2px solid var(--gold);
            text-align: center;
            backdrop-filter: blur(10px);
            box-shadow: 0 0 30px rgba(252, 207, 49, 0.2);
            animation: spawn 0.8s cubic-bezier(0.17, 0.89, 0.32, 1.49);
        }

        @keyframes spawn {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        h1 { color: var(--gold); margin-bottom: 0.5rem; }
        .online-box { font-size: 1.5rem; margin: 1rem 0; }
        .dot {
            height: 12px; width: 12px;
            background-color: #2ecc71;
            border-radius: 50%;
            display: inline-block;
            margin-right: 10px;
            box-shadow: 0 0 10px #2ecc71;
            animation: blink 1.5s infinite;
        }

        @keyframes blink {
            0% { opacity: 1; }
            50% { opacity: 0.4; }
            100% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>BurmalCraft</h1>
        <p>IP: burmalcraft.sosal.today</p>
        <div class="online-box">
            <span class="dot"></span>
            Игроков на сервере: <span id="count">...</span>
        </div>
        <p style="color: #aaa;">Версия: <span id="ver">загрузка...</span></p>
    </div>

    <script>
        async function updateStats() {
            try {
                const res = await fetch('/api/players');
                const data = await res.json();
                document.getElementById('count').innerText = data.online + ' / ' + data.max;
                document.getElementById('ver').innerText = data.version;
            } catch {
                document.getElementById('count').innerText = "Ошибка";
            }
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
