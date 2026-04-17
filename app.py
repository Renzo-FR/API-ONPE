from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/datos")
def datos():
    url = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
    
    headers = {
       'accept': '*/*',
       'accept-language': 'es-ES,es;q=0.9,en;q=0.8,de;q=0.7,vi;q=0.6,pt-BR;q=0.5,pt;q=0.4,ja;q=0.3,ko;q=0.2,zh-CN;q=0.1,zh;q=0.1',
       'content-type': 'application/json',
       'priority': 'u=1, i',
       'referer': 'https://resultadoelectoral.onpe.gob.pe/main/resumen',
       'sec-ch-ua': '"Not:A-Brand";v="99", "Opera GX";v="129", "Chromium";v="145"',
       'sec-ch-ua-mobile': '?1',
       'sec-ch-ua-platform': '"Android"',
       'sec-fetch-dest': 'empty',
       'sec-fetch-mode': 'cors',
       'sec-fetch-site': 'same-origin','accept': '*/*',
       'accept-language': 'es-ES,es;q=0.9,en;q=0.8,de;q=0.7,vi;q=0.6,pt-BR;q=0.5,pt;q=0.4,ja;q=0.3,ko;q=0.2,zh-CN;q=0.1,zh;q=0.1',
       'content-type': 'application/json',
       'priority': 'u=1, i',
       'referer': 'https://resultadoelectoral.onpe.gob.pe/main/resumen',
       'sec-ch-ua': '"Not:A-Brand";v="99", "Opera GX";v="129", "Chromium";v="145"',
       'sec-ch-ua-mobile': '?1',
       'sec-ch-ua-platform': '"Android"',
       'sec-fetch-dest': 'empty',
       'sec-fetch-mode': 'cors',
       'sec-fetch-site': 'same-origin',
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