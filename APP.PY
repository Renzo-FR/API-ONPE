from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/datos")
def datos():
    url = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/main/resumen"
    }

    response = requests.get(url, headers=headers)

    if "html" in response.text.lower():
        return jsonify({"error": "bloqueado por ONPE"})

    data = response.json()["data"]

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