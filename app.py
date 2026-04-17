
from flask import Flask, jsonify
from playwright.sync_api import sync_playwright
import threading
import time

app = Flask(__name__)

# =========================
# 🧠 CACHE GLOBAL
# =========================
cache = {
    "data": [],
    "last_update": 0,
    "status": "iniciando"
}

URL = "https://resultadoelectoral.onpe.gob.pe/main/resumen"

OBJETIVO = [
    "KEIKO SOFIA FUJIMORI HIGUCHI",
    "RAFAEL BERNARDO LÓPEZ ALIAGA CAZORLA"
]

# =========================
# 🚀 SCRAPER PLAYWRIGHT
# =========================
def actualizar_cache():
    global cache

    while True:
        try:
            cache["status"] = "actualizando"

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                page.goto(URL, wait_until="networkidle")

                response = page.wait_for_response(
                    lambda r: "participantes" in r.url
                )

                data = response.json().get("data", [])

                filtrados = [
                    {
                        "nombre": c["nombreCandidato"],
                        "votos": c["totalVotosValidos"],
                        "porcentaje": c["porcentajeVotosValidos"]
                    }
                    for c in data if c["nombreCandidato"] in OBJETIVO
                ]

                cache["data"] = filtrados
                cache["last_update"] = time.time()
                cache["status"] = "ok"

                browser.close()

                print("✔ cache actualizado")

        except Exception as e:
            cache["status"] = f"error: {str(e)}"
            print("error:", e)

        # 🔥 refresco cada 3 minutos
        time.sleep(180)

# =========================
# 🌐 ENDPOINTS FLASK
# =========================
@app.route("/")
def home():
    return "API ONPE activa"

@app.route("/datos")
def datos():
    return jsonify(cache)

@app.route("/estado")
def estado():
    return jsonify({
        "status": cache["status"],
        "last_update": cache["last_update"]
    })

# =========================
# 🚀 START SERVER
# =========================
if __name__ == "__main__":
    thread = threading.Thread(target=actualizar_cache)
    thread.daemon = True
    thread.start()

    app.run(host="0.0.0.0", port=10000)