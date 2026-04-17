from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "API ONPE activa"

@app.route("/datos")
def datos():

    url = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes"

    params = {
        "idEleccion": "10",
        "tipoFiltro": "eleccion"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/main/resumen"
    }

    # 👇 IMPORTANTE: aquí ya NO pongas cookies fijas
    response = requests.get(url, params=params, headers=headers, timeout=10)

    # validación segura
    if response.status_code != 200:
        return jsonify({"error": "ONPE no disponible", "status": response.status_code})

    try:
        data = response.json().get("data", [])
    except Exception:
        return jsonify({"error": "respuesta inválida de ONPE"})

    objetivo = [
        "KEIKO SOFIA FUJIMORI HIGUCHI",
        "RAFAEL BERNARDO LÓPEZ ALIAGA CAZORLA"
    ]

    filtrados = [
        {
            "nombre": c["nombreCandidato"],
            "votos": c["totalVotosValidos"],
            "porcentaje": c["porcentajeVotosValidos"]
        }
        for c in data if c["nombreCandidato"] in objetivo
    ]

    return jsonify(filtrados)


if __name__ == "__main__":
    app.run()